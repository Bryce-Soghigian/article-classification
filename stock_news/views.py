from django.core.exceptions import BadRequest
from django.shortcuts import render
from django import http

from stock_news.webscraper import NasdaqWebscraper
# Create your views here.

class StockNewsResourceManager(views.View):
    """
    Manage Stock News Articles.
    """

    def post(self, request:http.HttpRequest):
        """
        Add Nasdaq News Articles to database.
        """
        try:
            scraper = NasdaqWebscraper()
            scraper.main()
        except BadRequest:
            print(scraper.article_home, "ALL HOME")
            print(scraper.articles, 'articles')
            print(scraper.tickers,'tickers')
            return http.HttpResponseBadRequest(f'Web scrapper failed')