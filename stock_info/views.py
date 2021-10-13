import json
from django.http import HttpResponse
from django import views, http
from django.http.request import HttpRequest
from django.http.response import HttpResponseBadRequest, JsonResponse
from .models import Stock, StockInfo
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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


@method_decorator(csrf_exempt, name='dispatch')
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
            stock = Stock.objects.get(ticker=stock_info.get('ticker'))
        except AttributeError:
            return HttpResponseBadRequest('request body does not have property ticker.')
        except Stock.DoesNotExist:
            return HttpResponseBadRequest(f'Ticker does not exist in db')

        try:
            new_entry = StockInfo(
                ticker=stock, 
                date=stock_info.get('date'),
                open_price=stock_info.get('open_price'),
                low=stock_info.get('low'),
                volume=stock_info.get('volume'),
                close=stock_info.get('close'),
                high= stock_info.get('high'),
            )
            new_entry.save()
        except StockInfo.ValidationError:
            return HttpResponseBadRequest('Please check to see that your request body is valid.')

        response_json = {
            "message":f"Successfully added {new_entry}",
            "data":str(new_entry),
        }
        return JsonResponse(response_json)
        



