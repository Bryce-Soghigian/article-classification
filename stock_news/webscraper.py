from os import getcwd
import requests

from bs4 import BeautifulSoup
from django.core.exceptions import BadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from stock_news.models import NewsArticle
from ..stock_info.models import Stock
class Article:

    def __init__(self, ticker=None, date=None, article_title=None, article_content=None, origin_link=None):
        self.ticker = ticker
        self.date = date
        self.article_title = article_title
        self.article_content = article_content
        self.origin_link =origin_link

class NasdaqWebscraper:
    """
    Class the encapsulates the logic for the webscraper that scapes
    data from nasdaq.com
    """
    def __init__(self) -> None:
        self.tickers = []
        self.article_home = []
        self.articles = []
        self.stocks = {}
    
    def _fetch_all_stock_home_pages(self):
        """
        Retreive all of the homepages of the stock articles.
        """

        for ticker in self.tickers:
            uri = f'https://www.nasdaq.com/market-activity/stocks/{ticker}/news-headlines'
            request = requests.get(uri)
            if request.status_code == 200:
                self.article_home.append(uri)


    def _save_page_content_to_file(self, pageContent,file_name):
        """
        Save file content to a file so that beautiful soup can load it.
        """
        with open(f'{file_name}','wt') as file:
            for line in pageContent:
                file.write(str(line))
        
        return f'{getcwd}/{file_name}'

    def _get_article_links_from_nasdaq(self, article_url):
        """
        We want to retrieve all of the links to articles for a given stock so we can webscrape them.
        """
        nasdaq_articles = requests.get(article_url)
        scraper = BeautifulSoup(nasdaq_articles.content, "html.parser")
        links = scraper.findAll(href=True)
        # https://www.nasdaq.com/articles/3-ways-fords-electric-vehicle-strategy-may-be-perfectly-timed-2021-10-16
        for link in links:
            process_link = link.split("/")
            if process_link[3] == 'articles':
                new_artcle = Article(
                    origin_link = link,
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
    def _add_all_articles_to_db(self):
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
        1. Get all desired tickers from db
        2. go through and get all the articles for each stock ticker
        3. Scrape all articles that are in self.articles.
        4. Add all articles to the database.
        """
        try:
            stocks = Stock.objects.all()
        except Stock.DoesNotExist:
            raise BadRequest('Missing stock objects from db')

        # 1. Get all stock tickers we will scrape.
        for stock in stocks:
            self.stocks[stock.ticker] = stock
            self.tickers.append(stock.ticker)
        
        self._fetch_all_stock_home_pages()


        for homepage in self.article_home:
            self._get_article_links_from_nasdaq(article_url=homepage)
        

        for article in self.articles:
            self._scrape_article_from_nasdaq(article_obj=article)

        self._add_all_articles_to_db()