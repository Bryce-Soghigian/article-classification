from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Stock(models.Model):
    ticker = models.TextField(primary_key=True, unique=True)
    security_name = models.TextField()
    market_category = models.TextField()
    asset_class = models.TextField() 
    
    def __repr__(self) -> str:
        return f'ASSET__{self.ticker}'

class StockInfo(models.Model):
    ticker = models.ForeignKey(Stock, on_delete=CASCADE)
    date = models.DateField()
    open_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    def __repr__(self) -> str:
        return f'ASSET_INFO__{self.ticker}'