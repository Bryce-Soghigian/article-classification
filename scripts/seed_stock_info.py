"""
1. Query all existing stocks in the database throw them into a hashmap 
2. Loop through all csvs and add their data to our database. 


"""





import json
import csv
import requests
from os import listdir, path


stocks = requests.get('http://0.0.0.0:8000/stock_info/stocks')
stocks = json.loads(stocks.content)
path_to_csvs = "/Users/root1/Downloads/archive/stocks"
files = listdir(path_to_csvs)

post_url = "http://0.0.0.0:8000/stock_info/stock_info"

for file in files:
    with open(path.join(path_to_csvs, file), 'rt') as csv_file:
        # we want to 1. Post the stock info to the db
        info_counter = 0
        reader = csv.reader(csv_file)
        stock_ticker = file.split(".")[0]
        if stock_ticker in stocks:
            for row in reader:
                request_body = {
                    "ticker":stock_ticker,
                    "date":row[0],
                    "open_price":row[1],
                    "low":row[3],
                    "volume":row[6],
                    "close":row[4],
                    "high":row[2]
                }
            add_stock_info = requests.post(
                post_url,
                json.dumps(request_body)
            )
            print(add_stock_info.content)
            info_counter += 1
            if info_counter % 1000 == 0:

                print(f'Added 1000 entries.')
