from django.core.management import call_command

from celery import shared_task
from celery.utils.log import get_task_logger


@shared_task
def crawl_properties():
    call_command('crawl')
    logger = get_task_logger(__name__)
    logger.info("Properties scraped")
