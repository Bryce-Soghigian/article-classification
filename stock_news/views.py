import json

from django.core.exceptions import BadRequest
from django import views
from django import http
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from stock_news.webscraper import web_scraper_factory


@method_decorator(csrf_exempt, name='dispatch')
class StockNewsResourceManager(views.View):
    """
    Manage Stock News Articles.
    """

    def post(self, request: http.HttpRequest):
        """
        Select a webscraper to use and activate its main function.
        """
        try:
            req_body = json.loads(request.body)
        except json.JSONDecodeError:
            raise BadRequest('Invalid Json')

        if not req_body.scraper_type:
            return BadRequest('Missing Scraper type field in request.')

        scraper = web_scraper_factory(req_body.scraper_type)
        scraper.main()
