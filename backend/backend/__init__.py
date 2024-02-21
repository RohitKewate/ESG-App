from __future__ import absolute_import
import scrapydo
from .celery import app as celery_app
__all__ = ('celery_app',)
scrapydo.setup()