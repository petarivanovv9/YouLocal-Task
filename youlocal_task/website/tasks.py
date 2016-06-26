from __future__ import absolute_import

from django.conf import settings
from youlocal_task.celery import app

from celery import shared_task

from celery.decorators import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@app.task
def generate_save_all_venues_in_5km():
    print "generate_save_all_venues_in_5km"
    logger.info("generate_save_all_venues_in_5km")
    return "IT WORKS"
