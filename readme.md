# Project Summary

- We are building a classifier that lets us know whether or not it is worth to buy a stock based on the current momentum of that stock. 



## How can we predict the momentum of a stock

- I was thinking as a proof of concept i will build a news classifer that classifies stock articles for sentiment and decides an average trend of the stock. We will start with 10 stocks but expand to the spy 500. 

## Techstack
- Django
- Postgres
- Docker

### Steps in creating this MVP

0. Initial API Setup <Completed>
1. Create a database that stores historical stock data on our target stocks.<Completed>
2. Create a news database that stores information on stocks associated with a date
3. Write a model that classifies sentiment.
4. Create a database to store the classification_results.
5. Find a correlation(or the non-existent correlation) between stock price and a given sentiment rating for each of our models.


#### Gathering Historical Stock Data

1. Old data can be retrieved via a csv. We can add stock data via a django management command. Pass it a CSV as arg
2. Create a database model to store the CSV data
3. Build api endpoints to allow for the querying of the data in different useful ways
4. Include a view that allows us to plot the data for a stock over time with filters for 1 week 1 month 1 year and 5 years
5. Find a third party api I can use to get data updates on the given stocks. This job should run when the market closes. 
#### News Data Storage and Collection 
1. Research Existing Datasets for stock news articles.
2. If a sufficient dataset doesn't already exist we want to write a webscrapper and a reliable site to scrape data from.
3. We want to write a model to store the news articles. Should include date, stock ticker and the article.

#### Sentiment Classification

-  We want to build multiple sentiment classifers that we can train on the news data we aggregated with our webscraper and store the given sentiment for a stock on a given date. 
1. Explore Existing Sentiment Classification models and see what labels/features they prioritize, what really works in predicting sentiment.
2. This section will be expanded after I have done the research on sentiment classification.


#### Finding A Correlation between news sentiment and stock growth
1. Create a django view that plots the news sentiment and stock growth. 
2. Explore the stocks with the highest correlation between public approval and growth. Find how reliable stock growth is with Public approval on average.
