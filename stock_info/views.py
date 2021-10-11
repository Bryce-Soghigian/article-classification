import json
from django.http import HttpResponse
from django import views, http
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest
from .models import Stock, StockInfo


class StockResourceManager(views.View):
    """
    Managment of Stock Model class. 
    """
    def get(self, request: http.HttpRequest) -> http.HttpResponse:
        """
        Get all of the stock tickers
        """

        stocks = Stock.objects.all()
        if len(stocks) == 0:
            return http.HttpResponse('Database does not have any stocks seeded.')
        else:
            stock_map = {}

            for stock in stocks:
                stock_map[stock.ticker] = True

            return http.JsonResponse(
                stock_map,
            )


class StockInfoResourceManager(views.View):
    """
    Managment class for the stock info model.
    """
    def post(self, request:HttpRequest) -> HttpResponse:
        
        try:
            stock_info = json.loads(request.body)
        except json.JSONDecodeError:
            return http.HttpResponseBadRequest(
                'Invalid json'
            )
        
        try:
            stock = Stock.objects.get(ticker=stock_info.ticker)
        except Stock.DoesNotExist:
            return HttpResponseBadRequest(f'{stock_info.ticker} does not exist in db')

        try:
            new_entry = StockInfo(
                ticker=stock, 
                date=stock_info.date,
                open_price=stock_info.open_price,
                low=stock_info.low,
                volume=stock_info.volume,
                close=stock_info.close,
                high= stock_info.high,
            )
            new_entry.save()
        except ValueError:
            return HttpResponseBadRequest('Please check to see that your request body is valid.')
        



