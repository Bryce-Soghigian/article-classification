"""

1. Get all stocks

2. Get an array of all dates in a 6 year range


add all news entries


"""

import requests
import json


def get_stocks(request_url):
    stocks = requests.get(request_url)
    return json.loads(stocks.content)

import datetime
def generate_date_range(start_date, end_date):
    """
    1. Generate all days in a year
    """

    dates = []
    start = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    incremnt = datetime.timedelta(days=1)
    while start <= end:
        date_obj = start.date()

        dates.append(f'{date_obj.year}-{date_obj.month}-{date_obj.day}')
        start += incremnt

    return dates

date_range = generate_date_range('2021-01-01', '2021-06-01')
print(date_range)


def get_news_article_for_date(date,nxt,ticker):
    delta = "T00:00:00Z"
    date += delta
    nxt += delta
    query_url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&published_utc.lte={nxt}&published_utc.gt{date}&apiKey=BbbbfYHE0TPWpP2phpds0qC1pFb362fJ"
    #https://api.polygon.io/v2/reference/news?ticker=TSLA&published_utc=2021-04-26T00:00:00Z&limit=9&apiKey=BbbbfYHE0TPWpP2phpds0qC1pFb362fJ"
    results = requests.get(query_url)
    print(query_url)
    return json.loads(results.content)


for date in range(len(date_range)):
    obj = get_news_article_for_date(date_range[date],date_range[date+1],"TSLA")
    print(obj)