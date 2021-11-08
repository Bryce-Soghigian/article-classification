from django.core.exceptions import BadRequest
from django import views
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from stock_news.webscraper import NasdaqWebscraper


@method_decorator(csrf_exempt, name='dispatch')
class StockNewsResourceManager(views.View):
    """
    Manage Stock News Articles.
    """

    def post(self, request: http.HttpRequest):
        """
        Add Nasdaq News Articles to database.
        """
        try:
            scraper = NasdaqWebscraper()
            scraper.main()
        except BadRequest:
            print(scraper.article_home, "ALL HOME")
            print(scraper.articles, 'articles')
            print(scraper.tickers, 'tickers')
            return http.HttpResponseBadRequest(f'Web scrapper failed')