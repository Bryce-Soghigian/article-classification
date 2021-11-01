from django.urls import path

from . import views

urlpatterns = [
    path('news', views.StockNewsResourceManager.as_view(), name='stock_news_controller'),
]