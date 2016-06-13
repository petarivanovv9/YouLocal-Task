from django.shortcuts import render, HttpResponse

from local_settings import *
import requests


# Create your views here.


def index(request):
    venues = __get_venues()
    return render(request, 'index.html', locals())


def __get_venues():
    api_request = URL + LL + RADIOUS + INTENT + CLIENT_ID + CLIENT_SECRET + V + LIMIT
    info = requests.get(api_request).json()

    venues = info['response']['venues']
    formated_venus = []

    for item in venues:
        try:
            name = item['name']
            address = item['location']['address']
            # primary_category = None
            distance = item['location']['distance']
        except:
            print("There no such fields!")

        print(name + ' -- ' + address + ' -- ' + str(distance))

        venue = {}
        venue['name'] = name.encode('utf-8')
        venue['address'] = address
        venue['distance'] = str(distance)

        formated_venus.append(venue)

    return formated_venus
