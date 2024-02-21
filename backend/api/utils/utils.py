import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('vader_lexicon')

def create_esg_spider(start_urls, allowed_domains):
    class EsgSpider(CrawlSpider):
        name = "esg"
        rules = (Rule(LinkExtractor(), callback='parse_item', follow=True),)

        def __init__(self, *args, **kwargs):
            super(EsgSpider, self).__init__(*args, **kwargs)
            self.start_urls = start_urls
            self.allowed_domains = allowed_domains

        def parse_item(self, response):
            sia = SentimentIntensityAnalyzer()
            sentences = sent_tokenize(response.text)
            polarity_scores = [sia.polarity_scores(sentence) for sentence in sentences]

            yield {
                'url': response.url,
                'polarity_scores': polarity_scores
            }

    return EsgSpider
