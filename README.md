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

2. Create a virtual environment and follow the given steps.

        cd ESG-App/backend
        python -m venv myenv
        cd myenv/Scripts
        activate

3. Install the necessary packages.

        pip install -r requirements.txt
OR

       pip install absl-py==2.1.0 amqp==5.2.0 asgiref==3.8.1 astunparse==1.6.3 attrs==23.2.0 Automat==22.10.0 beautifulsoup4==4.12.3 billiard==4.2.0 celery==5.3.6 certifi==2024.2.2 cffi==1.16.0 charset-normalizer==3.3.2 click==8.1.7 click-didyoumean==0.3.1 click-plugins==1.1.1 click-repl==0.3.0 colorama==0.4.6 constantly==23.10.4 crochet==2.1.1 cryptography==42.0.5 cssselect==1.2.0 dateparser==1.2.0 Django==5.0.3 django-celery-results==2.5.1 django-cors-headers==4.3.1 django-environ==0.11.2 djangorestframework==3.15.1 filelock==3.13.3 finnhub-python==2.4.19 flatbuffers==24.3.25 fsspec==2024.3.1 gast==0.5.4 google-pasta==0.2.0 GoogleNews==1.6.14 grpcio==1.62.1 h5py==3.10.0 huggingface-hub==0.22.1 hyperlink==21.0.0 idna==3.6 incremental==22.10.0 itemadapter==0.8.0 itemloaders==1.1.0 jmespath==1.0.1 joblib==1.3.2 keras==3.1.1 kombu==5.3.6 libclang==18.1.1 lxml==5.1.0 Markdown==3.6 markdown-it-py==3.0.0 MarkupSafe==2.1.5 mdurl==0.1.2 ml-dtypes==0.3.2 namex==0.0.7 newsapi-python==0.2.7 nltk==3.8.1 numpy==1.26.4 opt-einsum==3.3.0 optree==0.11.0 packaging==24.0 parsel==1.9.0 pip==23.2.1 prompt-toolkit==3.0.43 Protego==0.3.0 protobuf==4.25.3 pyasn1==0.6.0 pyasn1_modules==0.4.0 pycparser==2.21 PyDispatcher==2.0.7 Pygments==2.17.2 pyOpenSSL==24.1.0 python-dateutil==2.9.0.post0 python-decouple==3.8 python-dotenv==1.0.1 pytz==2024.1 PyYAML==6.0.1 queuelib==1.6.2 regex==2023.12.25 requests==2.31.0 requests-file==2.0.0 rich==13.7.1 safetensors==0.4.2 scipy==1.12.0 Scrapy==2.11.1 scrapydo==0.2.2 service-identity==24.1.0 setuptools==65.5.0 six==1.16.0 soupsieve==2.5 sqlparse==0.4.4 tensorboard==2.16.2 tensorboard-data-server==0.7.2 tensorflow==2.16.1 tensorflow-intel==2.16.1 tensorflow-io-gcs-filesystem==0.31.0 termcolor==2.4.0 tf_keras==2.16.0 tldextract==5.1.2 tokenizers==0.15.2 tqdm==4.66.2 transformers==4.39.1 Twisted==24.3.0 twisted-iocpsupport==1.0.4 typing_extensions==4.10.0 tzdata==2024.1 tzlocal==5.2 urllib3==2.2.1 vine==5.1.0 w3lib==2.1.2 wcwidth==0.2.13 Werkzeug==3.0.1 wheel==0.43.0 wrapt==1.16.0 zope.interface==6.2


4. Create a new file called `.env` in the project directory, and add the following lines to it..

        SECRET_KEY=<your-django-secret-key> in settings.py
        BASE_URL=<your-base-url>
        NEWS_API_KEY=<your-news-api-key>
        FINNHUB_API_KEY=<your-finnhub-api-key>
        

5. Start the app.

        python manage.py runserver

That's it! The app should be accessible at `http://127.0.0.1:8000`.


The app uses the News API to crawl news articles about a particular company. To use the News API, you need to sign up for an API key at https://newsapi.org/. Once you have an API key, add it to the `NEWS_API_KEY` environment variable in the `.env` file.

Note that the News API has a rate limit of 100 requests per minute. The app should not make more than 100 requests to the News API in a minute, but if it does, it will stop working until the rate limit resets.

