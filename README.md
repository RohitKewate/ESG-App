# ESG App Backend

Introduction
============

This is the backend of the Environment Social Governance (ESG) application. It is a Django app, using the Django REST framework, written in Python. The app uses a SQL database. It also uses the pre-trained RoBERTa model for calculating the sentiment analysis score of the news articles.

ESG Score Finder App
Welcome to the ESG Score Finder App! This application helps you find the Environmental, Social, and Governance (ESG) scores of companies. Here's how it works:

How to use
===========

Search for a Company: Start by searching for a company in the frontend of the app.

Database Check: The app checks if the company is already in our database.
- If the company is found, its ESG score is fetched and displayed in the frontend.
- If the company is not found, it's added to our database.
  
Biweekly Updates: For new companies, we perform biweekly updates.
- We use spiders/crawlers to analyze news related to the company from the News API.
- Each news article is scored individually, and a compound score is calculated.
- This compound score is saved in our database.

ESG Score Calculation: The app calculates the ESG score for the company based on the compound score and the ESG factor scores of the sector the company belongs to.

How to works
=============

Frontend: The user interface where you search for companies.

Backend: The Django server that handles requests, updates the database, and performs the biweekly analysis.

Database: Stores all the companies and their ESG scores.

Spiders/Crawlers: Tools that analyze news articles related to companies.

News API: Provides news articles for analysis.

Benefits
=============

Easy to Use: Simply search for a company to find its ESG score.

Up-to-Date Information: Companies are updated biweekly, ensuring the scores are current.

Comprehensive Analysis: The app considers both the company's individual performance and the sector's ESG factors.

Getting Started
===============

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

