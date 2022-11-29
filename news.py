import requests


class News():
    def __init__(self, symbol) -> None:
        self.endpoint = "https://query1.finance.yahoo.com/v1/finance/search"
        self.params = {"q": symbol}
        self.headers = {'User-agent': 'Mozilla/5.0'}
        self.articles = []

    @classmethod
    def get_articles(cls, symbol):
        """Get valid articles for a specific stock symbol"""
        news = cls(symbol)
        resp = news.request()

        if not resp:
            return news.articles

        data = news.extract_data(resp)

        if not data:
            return news.articles

        news.create_articles(data)

        return news.articles

    def request(self):
        """Query Yahoo Finance with the symbol and return response"""
        try:
            resp = requests.get(
                self.endpoint,
                params=self.params,
                headers=self.headers)

            return resp
        except:
            print("Response is not valid.")

    def extract_data(self, resp):
        """Get data from response, if available"""
        try:
            data = resp.json()
            return data["news"]
        except:
            print("No response data.")

    def create_articles(self, data):
        """Create articles that include a title, publisher and image"""
        for item in data:
            title = item.get("title")
            publisher = item.get("publisher")
            url = item.get("link")
            thumbnail_url = self.extract_thumbnail(item)
            if title and publisher and thumbnail_url:
                article = {
                    "title": title,
                    "publisher": publisher,
                    "url": url,
                    "thumbnail_url": thumbnail_url
                }
                self.articles.append(article)

    def extract_thumbnail(self, article):
        """Ensure a thumbnail of the proper resolution is available"""
        try:
            thumbnails = article["thumbnail"]["resolutions"]
            thumbnail_url = None
            for thumbnail in thumbnails:
                if thumbnail.get("tag") == "140x140":
                    thumbnail_url = thumbnail.get("url")
                    break
            return thumbnail_url
        except:
            print("No thumbnail url.")
