from django.shortcuts import render, redirect

from local_settings import *
import requests
import datetime

from pymongo import MongoClient, DESCENDING

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from .tasks import generate_save_all_venues_in_5km

import json


client = MongoClient()
db = client.mydb


def index(request):
    venues = __get_venues_in_radius()
    # print db.collection_names(include_system_collections=False)
    print db.venues.count()
    return render(request, 'index.html', locals())


def save_venues(request):
    # generate_save_all_venues_in_5km.delay()

    # print generate_save_all_venues_in_5km.delay().get()

    venues = db.venues
    # print(request.POST.lists())
    # print(request.POST.lists()[-1][-1])
    for i in request.POST.lists()[-1][-1]:
        try:
            venue = __get_venue_by_id(i)
            venue['_id'] = venue['id']
            new_venue_id = {'_id': venue['id']}
            del venue['id']
            venue['date'] = str(datetime.datetime.utcnow())
            venues.update(new_venue_id, venue, upsert=True)
        except:
            continue

    # b = generate_save_all_venues_in_5km.AsyncResult(a)
    # b.get()

    return redirect('index')

def __get_venues_in_radius():
    api_request = URL + 'search' + '?' + LL + RADIOUS + INTENT + '&' + CLIENT_ID + '&' + CLIENT_SECRET + V
    info = requests.get(api_request).json()
    if requests.get(api_request).status_code != 200:
        return None
    venues = info['response']['venues']
    formated_venues = []

    for item in venues:
        try:
            id = item['id']
            name = item['name']
            primary_category = item['categories'][0]['primary']
            distance = item['location']['distance']
            address = item['location']['address']
        except Exception as exc:
            address = ''
            # print("There no such fields!")
        venue = {}
        venue['id'] = id
        venue['name'] = name
        venue['address'] = address
        venue['primary_category'] = primary_category
        venue['distance'] = distance

        formated_venues.append(venue)

    return formated_venues


def __get_venue_by_id(id_venue):
    api_request = URL + id_venue + '?' + CLIENT_ID + '&' + CLIENT_SECRET + V + '&' + LL
    info = requests.get(api_request).json()
    if requests.get(api_request).status_code != 200:
        return None
    raw_venue = info['response']['venue']
    try:
        id = raw_venue['id']
        name = raw_venue['name']
        primary_category = raw_venue['categories'][0]['primary']
        distance = raw_venue['location']['distance']
        address = raw_venue['location']['address']
    except Exception as exc:
        address = ''
        # print("There no such fields!")
    # print(id + ' -- ' + name + ' -- ' + address + ' -- ' + str(distance))
    venue = {}
    venue['id'] = id
    venue['name'] = name
    venue['address'] = address
    venue['primary_category'] = primary_category
    venue['distance'] = distance

    return venue


@api_view(['GET'])
def get_venues_in_5km_desc(request):
    raw_venues = db.venues.find({'distance' : {'$lt': 5000}}).sort([
        ('distance', DESCENDING),
    ])
    venues = []
    for i in raw_venues:
        venues.append(i)
    data = {
        'venues': venues,
    }
    return Response(data, status=status.HTTP_200_OK)
