from django.shortcuts import render, redirect

from local_settings import *
import requests
import datetime

from pymongo import MongoClient

client = MongoClient()
db = client.mydb


def index(request):
    venues = __get_venues_in_radius()
    #print db.collection_names(include_system_collections=False)
    print db.venues.count()
    return render(request, 'index.html', locals())


def save_venues(request):
    venues = db.venues
    print(request.POST.lists())
    print(request.POST.lists()[-1][-1])

    for i in request.POST.lists()[-1][-1]:
        try:
            print 'qshaaa'
            venue = __get_venue_by_id(i)
            print 'opaa'
            venue['_id'] = venue['id']
            patka = {'_id': venue['id']}
            del venue['id']
            venue['date'] = datetime.datetime.utcnow()
            print venue
            venue_id = venues.update(patka, venue, upsert=True)
            print venue_id
        except:
            continue


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
        print 'GRESHKAAA'
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
