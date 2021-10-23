from django.db import models
from django.db.models.deletion import PROTECT
from ..stock_info.models import Stock
# Create your models here.

class NewsArticle(models.Model):
    article_id = models.AutoField(primary_key=True)
    ticker = models.ForeignKey(Stock,on_delete=PROTECT)
    timestamp = models.DateTimeField()
    article_content = models.TextField()
    article_title = models.TextField()
    article_origin = models.TextField()