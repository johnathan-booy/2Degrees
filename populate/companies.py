"""
Retrieve stock symbols from the S&P500, NASDAQ100 and DOWJONES

Run like:

    c = Companies.populate()
"""

from bs4 import BeautifulSoup
import requests
from app import app
from database import db
from models.company import Company
from models.exchange import Exchange


class Companies():
    def __init__(self) -> None:
        self.nasdaq_url = "https://www.slickcharts.com/nasdaq100"
        self.sp500_url = "https://www.slickcharts.com/sp500"
        self.dowjones_url = "https://www.slickcharts.com/dowjones"
        self.companies = self.get_companies()

    @classmethod
    def populate(cls):
        """Compare companies to DB, and add company rows when not already included"""
        c = cls()
        for company in c.companies:

            symbol, exchange_symbol, name = company
            esg_available = True

            if not Exchange.query.filter_by(symbol=exchange_symbol).first():
                db.session.add(
                    Exchange(symbol=exchange_symbol, esg_available=False)
                )
                db.session.commit()

                # We can only query esg ratings for stock markets that are recognized by ESG Enterprise
                esg_available = False

            if not Company.query.filter_by(symbol=symbol, exchange_symbol=exchange_symbol, name=name).first():
                print("Added", company)

                db.session.add(
                    Company(
                        symbol=symbol,
                        exchange_symbol=exchange_symbol,
                        name=name,
                        esg_available=esg_available
                    )
                )

        db.session.commit()
        return c

    def extract_html(self, url):
        """Get HTML with a specified User-Agent"""
        headers = {"User-Agent": "Mozilla/5.0"}
        result = requests.get(url, headers=headers)
        return result.text

    def scrape_companies(self, url):
        """Parse stock symbols from a slickcharts url"""
        companies = []
        html = self.extract_html(url)
        doc = BeautifulSoup(html, "html.parser")
        trs = (
            doc
            .find_all("table")[0]
            .find("tbody")
            .find_all('tr')
        )

        for tr in trs:
            symbol = (
                tr
                .find_all('td')[2]
                .string
            )
            name = (
                tr
                .find_all('td')[1]
                .string
            )

            company = self.get_company_data(symbol, name)

            if company:
                companies.append(company)

        return companies

    def get_company_data(self, symbol, name):
        """Query Yahoo Finance API and return (symbol, exchange_symbol, name)"""
        symbol = symbol.upper()
        name = self.process_name(name)

        resp = requests.get(
            "https://query1.finance.yahoo.com/v1/finance/search",
            params={"q": name},
            headers={'User-agent': 'Mozilla/5.0'})

        data = resp.json()

        quotes = data.get('quotes')

        if not quotes:
            return

        for quote in quotes:

            new_symbol = quote.get("symbol")
            if not new_symbol:
                continue

            if symbol not in new_symbol:
                continue

            exchange_symbol = self.process_exchange(quote.get("exchange"))
            if not exchange_symbol:
                continue

            new_name = quote.get("longname")
            if not new_name:
                continue

            return (new_symbol, exchange_symbol, new_name)

    def get_companies(self):
        """Get stock symbols for nasdaq s&p 500 and dowjones"""
        nasdaq_100 = self.scrape_companies(self.nasdaq_url)
        sp500 = self.scrape_companies(self.sp500_url)
        dowjones = self.scrape_companies(self.dowjones_url)

        return list(set().union(nasdaq_100, sp500, dowjones))

    def process_name(self, name):
        """Remove unwanted parts from the company name"""
        strings = [
            "Class A",
            "Class B",
            "Class C",
            "Class D"
        ]

        for string in strings:
            name = name.replace(string, "")

        return name.strip()

    def process_exchange(self, exchange):
        """Take the exchange symbol from Yahoo Finance and convert it into the expected symbol for ESG Enterprise"""
        conversion = {
            "AMS": "AMS",
            "ASE": "AMEX",
            "ASX": "ASX",
            "BUE": "BCBA",
            "MCE": "BME",
            "MIL": "BIT",
            "NGM": "NASDAQ",
            "NMS": "NASDAQ",
            "NYQ": "NYSE",
            "TOR": "TSE"
            # More to add later
            #  BKK, BMV, BVMF, CPH, CVE, EBR, ELI, EPA, ETR, HKG, IDX, IST, JSE, KLSE, KOSDAQ, LON, NSE, OTCBB, OTCMKTS, SGX, SHA, SHE, STO, SWX, TADAWUL, TLV, TPE, TYO
        }
        return conversion.get(exchange, exchange)
