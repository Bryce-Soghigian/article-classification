from django.http import request
from django.urls import path

from . import views

urlpatterns = [
    path('stocks', views.StockResourceManager.as_view(), name='stock_info_controller'),
    path('stock_info', views.StockInfoResourceManager.as_view(), name='stock_info_controller')
]