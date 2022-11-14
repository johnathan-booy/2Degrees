"""
Retrieve stock symbols from the S&P500, NASDAQ100 and DOWJONES

Run like:

    stock_symbols = StockSymbols.populate()
"""

from bs4 import BeautifulSoup
import requests
from app import app
from database import db
from models.company import Company


class StockSymbols():
    def __init__(self) -> None:
        self.nasdaq_url = "https://www.slickcharts.com/nasdaq100"
        self.sp500_url = "https://www.slickcharts.com/sp500"
        self.dowjones_url = "https://www.slickcharts.com/dowjones"
        self.symbols = self.collect_symbols()

    @classmethod
    def populate(cls):
        """Compare symbols to DB, and add company rows when not already included"""
        stock_symbols = cls()
        for symbol in stock_symbols.symbols:
            if not Company.query.filter_by(symbol=symbol).all():
                db.session.add(Company(symbol=symbol))
            db.session.commit()
        return stock_symbols

    def extract_html(self, url):
        """Get HTML with a specified User-Agent"""
        headers = {"User-Agent": "Mozilla/5.0"}
        result = requests.get(url, headers=headers)
        return result.text

    def scrape_symbols(self, url):
        """Parse stock symbols from a slickcharts url"""
        symbols = []
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
            symbols.append(symbol)

        return symbols

    def collect_symbols(self):
        """Get stock symbols for nasdaq s&p 500 and dowjones"""
        nasdaq_100 = self.scrape_symbols(self.nasdaq_url)
        sp500 = self.scrape_symbols(self.sp500_url)
        dowjones = self.scrape_symbols(self.dowjones_url)
        return list(set().union(nasdaq_100, sp500, dowjones))
