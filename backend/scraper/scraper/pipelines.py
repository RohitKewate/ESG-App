# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from backend.api.models import EsgScore
from .items import EsgScoreItem

class EsgScorePipeline:
    def process_item(self, item, spider):
        if isinstance(item, EsgScoreItem):
            esg_score = EsgScore(company=item['company'], emission=item['emission'])
            esg_score.save()
        return item

