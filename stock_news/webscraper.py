from os import getcwd
import requests

from bs4 import BeautifulSoup
from django.core.exceptions import BadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from stock_news.models import NewsArticle
from stock_info.models import Stock

constants = {
    'yahoo_url': 'https://finance.yahoo.com/quote'
}

class Article:

    def __init__(self, ticker=None, date=None, article_title=None, article_content=None, origin_link=None):
        self.ticker = ticker
        self.date = date
        self.article_title = article_title
        self.article_content = article_content
        self.origin_link =origin_link


class BaseWebScrapper:

    def __init__(self):
        self.articles = []
        self.stocks = self._get_stocks()
        self.tickers = []
        self.homepage = []
        self.sites = []


    def get_stocks(self):
        """
        Gets all stocks in our db
        """
        existing = {}
        try:
            stocks = Stock.objects.all()
        except Stock.DoesNotExist:
            raise BadRequest('Missing stock objects from db')
        print('Successfully Retrieved All Stocks...')
        # 1. Get all stock tickers we will scrape.
        for stock in stocks:
            existing[stock.ticker] = stock
            if stock.ticker != "Symbol":
                self.tickers.append(stock.ticker)

        return existing

    def gather_homepages_to_scrape(self, base_url):
        """
        Given a base url this method will go through all of the stocks and give you a list of sites that contain stocks.

        Example Webscraper.gather_sites_to_scrape(https://finance.yahoo.com/quote/)
        we then check all sites .
        """

        if not self.tickers:
            raise BadRequest('Server Error with gathering stocks from db.')


        for ticker in self.tickers:
            request = requests.get(f'{base_url}/{ticker}')
            if request.status_code == 200:
                self.homepage.append(f'{base_url}/{ticker}')

    def add_articles_to_db(self):
        """
        Adds all of the articles we gathered to the database.
        """
        for article in self.articles:
            new_news = NewsArticle(
                ticker=self.stocks[article.ticker],
                timestamp=article.date,
                article_content=article.article_content,
                article_title=article.article_title,
                article_origin=article.origin_link
            )
            new_news.save()

    def main(self):
        """
        Main webscraper function where we can execute all of our methods.
        """
        raise NotImplementedError

class YahooWebScraper(BaseWebScrapper):
    """
    Class that encapsulates the logic for scrapping news from yahoo finance.
    """
    def __init__(self):
        super(BaseWebScrapper).__init__()
        self.article_links = []
    def main(self):
        """
        1. Scrape all aritcles we can scrape
        2. add those article urls to a deque
        3. One by one parse those articles and add them to a database
        """
        self.gather_homepages_to_scrape(self, base_url=constants.yahoo_url)

        for page in self.homepage:
            self.gather_articles(page)

class NasdaqWebscraper(BaseWebScrapper):
    """
    Class the encapsulates the logic for the webscraper that scapes
    data from nasdaq.com
    """
    def __init__(self) -> None:
        super(BaseWebScrapper).__init__()
        self.article_home = []
        self.articles = []

    def _get_article_links_from_nasdaq(self, article_url):
        """
        We want to retrieve all of the links to articles for a given stock so we can webscrape them.
        """
        nasdaq_articles = requests.get(article_url)
        scraper = BeautifulSoup(nasdaq_articles.content, "html.parser")

        links = scraper.findAll(href=True)
        print(links)
        # https://www.nasdaq.com/articles/3-ways-fords-electric-vehicle-strategy-may-be-perfectly-timed-2021-10-16
        for link in links:
            process_link = link.split("/")
            if process_link[3] == 'articles':
                new_artcle = Article(
                    origin_link=link,
                    article_title=process_link[4]
                )
                self.articles.append(new_artcle)
    
    def _scrape_article_from_nasdaq(self,article_obj):
        """
        Scrape content and add to database.

        1. Fetch the article and soup it
        2. Parse the article

        """
        article = requests.get(article_obj.origin_url)
        scraper = BeautifulSoup(article.content, "html.parser")
        article_content = scraper.find_all('div', attrs={'class':'body__content'})
        article_date = scraper.find_all('time', attrs={'class':'timestamp__date'})

        article_obj.article_content = article_content
        article_obj.date = article_date

    @method_decorator(csrf_exempt, name='dispatch')
    def _add_all_articles_to_db(self) -> object:
        """
        Pretty self explanatory bruh.
        """
        for article in self.articles:
            new_news = NewsArticle(
                ticker=self.stocks[article.ticker],
                timestamp=article.date,
                article_content=article.article_content,
                article_title=article.article_title,
                article_origin=article.origin_link
            )
            new_news.save()

    def main(self):
        """
        Main function of the webscraper that executes all of our private methods.
        """
        print('==================Initializing Nasdaq Webscraper==============================')


        print('fetching home pages for stocks in self.stocks')
        self._fetch_all_stock_home_pages()

        for homepage in self.article_home:
            print(f'Processing {homepage}...')
            # Get main for each stock
            self._get_article_links_from_nasdaq(article_url=homepage)

        for article in self.articles:
            print(f'Processing article {article.origin_link}')
            # Scrape all articles for each stock.
            self._scrape_article_from_nasdaq(article_obj=article)

        self._add_all_articles_to_db()

def web_scraper_factory(scraper_type):
    """
    Factory Function for generating WebScrapers.
    """
    if scraper_type == "":
        raise BadRequest('Missing a scraper type')
    elif scraper_type == 'nasdaq':
        return NasdaqWebscraper()
    elif scraper_type == "yahoo":
        return YahooWebScraper()
    else:
        raise Exception('Scrapper Does Not Exist')

