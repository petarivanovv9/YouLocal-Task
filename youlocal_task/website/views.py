from django.shortcuts import render, redirect

from .local_settings import *
import requests
import datetime

from pymongo import MongoClient, DESCENDING

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .tasks import generate_save_all_venues_in_5km

from .models import Venue

import json

from .serializers import VenueSerializer


client = MongoClient()
db = client.mydb


def index(request):
    venues = __get_venues_in_radius()
    # print db.collection_names(include_system_collections=False)

    print db.venues.count()

    # print len(Venue.objects.all())

    # serializer_v = VenueSerializer(Venue.objects.all()[0])
    # print serializer_v

    return render(request, 'index.html', locals())


def save_venues(request):
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

            # print len(Venue.objects.all())

            # Venue.objects.create(
            #     _id = venue['_id'],
            #     name = venue['name'],
            #     contact = venue['contact'],
            #     location = venue['location'],
            #     categories = venue['categories'],
            #     verified = venue['verified'],
            #     date = datetime.datetime.utcnow(),
            # ).save(force_insert=True)

            # print len(Venue.objects.all())
        except Exception as exc:
            pass

    print "BEFORE"
    print db.venues.count()

    generate_save_all_venues_in_5km()

    print "AFTER"
    print db.venues.count()

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
            # print("There no such fields!")
            pass
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
        contact = raw_venue['contact']
        location = raw_venue['location']
        categories = raw_venue['categories']
        verified = raw_venue['verified']
    except Exception as exc:
        # print("There no such fields!")
        pass
    # print(id + ' -- ' + name + ' -- ' + address + ' -- ' + str(distance))
    venue = {}
    venue['id'] = id
    venue['name'] = name
    venue['contact'] = contact
    venue['location'] = location
    venue['categories'] = categories
    venue['verified'] = verified
    return venue


@api_view(['GET'])
def get_venues_in_5km_desc(request):
    raw_venues = db.venues.find({ 'location.distance' : {'$lt': 5000}}).sort([
        ('distance', DESCENDING),
    ])
    print raw_venues.count()
    venues = []
    for i in raw_venues:
        venues.append(i)
    data = {
        'venues': venues,
    }
    return Response(data, status=status.HTTP_200_OK)
