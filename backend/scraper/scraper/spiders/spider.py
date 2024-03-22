

# scraper/spiders/news_spider.py


from ..items import EsgScoreItem
from GoogleNews import GoogleNews
import finnhub
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import quote
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

import requests
from api.models import EsgScore, CompanyDetails  # Assuming ESGscore is a Django model
from nltk.sentiment import SentimentIntensityAnalyzer
from ..items import EsgScoreItem
from scipy.special import softmax
import logging

from newsapi import NewsApiClient
import requests
import json

# spiders/emission_spider.py
import scrapy
from newsapi import NewsApiClient
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification



class EmissionSpider(scrapy.Spider):
    name = 'emission'
    api_key = os.getenv("NEWS_API_KEY") 
    logger = logging.getLogger('EmissionSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["emission", "carbon emission", "CO2 emission", "greenhouse gas", "carbon footprint"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }


class InnovationSpider(scrapy.Spider):
    name = 'innovation'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('InnovationSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["innovation", "creation", "product", "disruption", "features"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }


class ResourceSpider(scrapy.Spider):
    name = 'resource'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('ResourceSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["resource utilization", "resource management", "resource allocation", "resource optimization", "efficient resource usage"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }

#SOCIAL SPIDER'S

class HumanSpider(scrapy.Spider):
    name = 'human'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('HumanSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["human right", "civil liberties", "individual freedoms", "equal rights", "social justice"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }


class ProductSpider(scrapy.Spider):
    name = 'product'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('ProductSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["product responsibility", "corporate responsibility", "sustainable products", "ethical manufacturing", "product sustainability"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }


class WorkforceSpider(scrapy.Spider):
    name = 'workforce'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('WorkforceSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["workforce", "labor force", "employee base", "staffing", "human resources"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }


class CommunitySpider(scrapy.Spider):
    name = 'community'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('CommunitySpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["community", "business network", "company ecosystem", "organizational community", "company network"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }


#GOVERNANCE SPIDER'S

class ManagementSpider(scrapy.Spider):
    name = 'management'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('ManagementSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["management", "business leadership", "company administration", "organizational  governance", "firm supervision"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }


class ShareholderSpider(scrapy.Spider):
    name = 'shareholder'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('ShareholderSpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["shareholders", "corporate investors", "company equity holders", "business stockholders", "stocks"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }

class CsrStrategySpider(scrapy.Spider):
    name = 'csr'
    api_key = os.getenv("NEWS_API_KEY")  # Replace with your News API key
    logger = logging.getLogger('CsrStrategySpider')
    newsapi = NewsApiClient(api_key=api_key)
    model = TFRobertaForSequenceClassification.from_pretrained('siebert/sentiment-roberta-large-english')
    tokenizer = RobertaTokenizerFast.from_pretrained('siebert/sentiment-roberta-large-english')

    def start_requests(self):
        company_name = getattr(self, 'company_name', None)
        keywords = ["csr strategy", "corporate social responsibility strategy", "company ethical initiatives", "business sustainability approach", "corporate citizenship plan"]
        if company_name is not None:
            # Fetch news articles for each keyword
            for keyword in keywords:
                news_items = self.newsapi.get_everything(q=f"{company_name} {keyword}")
                print(f"Found {len(news_items['articles'])} articles for company {company_name} with keyword {keyword}")
                if not news_items['articles']:
                    self.logger.warning(f"No articles found for company {company_name} with keyword {keyword}")
                    continue  # go to the next keyword
                for news_item in news_items['articles']:
                    yield scrapy.Request(url=news_item['url'], callback=self.parse_article)


    def parse_article(self, response: scrapy.http.HtmlResponse):
        text = ' '.join(response.css('p::text').getall())
        print(f"Extracted text from {response.url}: {text[:100]}...")  # print the first 100 characters
        if not text:
            self.logger.warning(f"No text found at {response.url}")
            return

        # Tokenize the text
        try:
            inputs = self.tokenizer(text, return_tensors='tf', truncation=True, padding=True)
        except Exception as e:
            print(f"Error tokenizing text: {e}")
            return

        # Get the sentiment score
        try:
            outputs = self.model(inputs)
            sentiment_scores = softmax(outputs.logits[0].numpy())
        except Exception as e:
            print(f"Error getting sentiment score: {e}")
            return

        # Compute the compound score
        try:
            if len(sentiment_scores) < 2:
                print(f"sentiment_scores has fewer than 2 elements: {sentiment_scores}")
                return
            compound_score = float(sentiment_scores[1]) if len(sentiment_scores) == 2 else float(sentiment_scores[2])
            print(f"Computed compound score: {compound_score}")
        except Exception as e:
            print(f"Error computing compound score: {e}")
            return

        # If the compound score is less than a threshold, set it to a default minimum score
        min_score = 0.01
        if compound_score < min_score:
            compound_score = min_score

        yield {
            'url': response.url,
            'score': round(compound_score, 2)  # compound score from RoBERTa, rounded to 2 decimal places
        }