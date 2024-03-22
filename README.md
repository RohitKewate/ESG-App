# ESG App Backend
Introduction
============

This is the backend of the Environment Social Governance (ESG) application. It is a Django app, using the Django REST framework, written in Python. The app uses a SQL database. It also uses the pre-trained RoBERTa model for calculating the sentiment analysis score of the news articles.

How it works
============

The app works like this:

1. If you want to find an ESG (Environmental, Social, and Governance) score of a company, search it in the frontend.

2. The frontend sends a request to the Django backend for data from the database.

3. If the company is present in the database, then it will be fetched in the frontend.

4. If not, then the company is added in the backend's database and biweekly updates will be performed on that company.

5. The biweekly analysis is done on all the companies in the database. All the spiders/crawlers are run on the News API news related to that company, giving us individual scores of all the news articles.

6. We get a compound score and save the in the database.

7. This score is calculated and an ESG score is formed for that perticular company.

8. Remember it also checks the ESG factor scores of that sector in which that perticular company belongs to for calculating the company ESG score.

How to start the app in your own server
==========================================

1. Install Python 3.8 or later.

2. Install the necessary packages.

        pip install -r requirements.txt

3. Create a new file called `.env` in the project directory, and add the following lines to it..

        SECRET_KEY=<your-django-secret-key> in settings.py
        BASE_URL=<your-base-url>
        NEWS_API_KEY=<your-news-api-key>
        FINNHUB_API_KEY=<your-finnhub-api-key>
        

4. Start the app.

        python manage.py runserver

That's it! The app should be accessible at `http://127.0.0.1:8000`.


The app uses the News API to crawl news articles about a particular company. To use the News API, you need to sign up for an API key at https://newsapi.org/. Once you have an API key, add it to the `NEWS_API_KEY` environment variable in the `.env` file.

Note that the News API has a rate limit of 100 requests per minute. The app should not make more than 100 requests to the News API in a minute, but if it does, it will stop working until the rate limit resets.

