from __future__ import absolute_import

from django.conf import settings
from youlocal_task.celery import app

from .local_settings import *

import requests
import datetime

from celery.decorators import task

# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

from pymongo import MongoClient


client = MongoClient()
db = client.mydb


@app.task
def generate_save_all_venues_in_5km():
    venues_db = db.venues
    api_request = URL + 'search' + '?' + LL + RADIOUS_5KM + INTENT + '&' + CLIENT_ID + '&' + CLIENT_SECRET + V
    info = requests.get(api_request).json()
    if requests.get(api_request).status_code != 200:
        return None
    venues = info['response']['venues']

    for item in venues:
        try:
            id = item['id']
            name = item['name']
            contact = item['contact']
            location = item['location']
            categories = item['categories']
            verified = item['verified']
        except Exception as exc:
            # print("There no such fields!")
            pass
        venue = {}
        venue['_id'] = id
        venue['name'] = name
        venue['contact'] = contact
        venue['location'] = location
        venue['categories'] = categories
        venue['verified'] = verified
        venue['date'] = str(datetime.datetime.utcnow())
        new_venue_id = {'_id': venue['_id']}
        venues_db.update(new_venue_id, venue, upsert=True)
