from django.shortcuts import render, redirect

from local_settings import *
import requests


# Create your views here.


def index(request):
    venues = __get_venues_in_radius()
    return render(request, 'index.html', locals())


def save_venues(request):
    #print(request.POST.items())
    print('blqblqblq')
    # print(request.POST.values())
    print('blqblqblq')
    print(request.POST.lists())
    print(request.POST.lists()[-1][-1])
    print('da mu ebesh')
    for i, j in enumerate(request.POST.lists()[-1][-1]):
        print i
        print j
        print 30 * '-'
        print __get_venue_by_id(j)
        print __get_venue_by_id(j)['name']
    # print(request.POST.lists()[-1][-1][])
    # print(request.POST.lists()[-1][-1])

    print('qsha')

    return redirect('index')

def __get_venues_in_radius():
    api_request = URL + 'search' + '?' + LL + RADIOUS + INTENT + '&' + CLIENT_ID + '&' + CLIENT_SECRET + V + LIMIT
    info = requests.get(api_request).json()
    if requests.get(api_request).status_code != 200:
        return None
    venues = info['response']['venues']
    formated_venues = []

    for item in venues:
        try:
            id = item['id']
            name = item['name']
            address = item['location']['address']
            # primary_category = None
            distance = item['location']['distance']
        except:
            print("There no such fields!")

        print(id + ' -- ' + name + ' -- ' + address + ' -- ' + str(distance))

        venue = {}
        venue['id'] = id
        venue['name'] = name
        venue['address'] = address
        venue['distance'] = distance

        formated_venues.append(venue)

    return formated_venues


def __get_venue_by_id(id_venue):
    api_request = URL + id_venue + '?' + CLIENT_ID + '&' + CLIENT_SECRET + V + '&' + LL

    print api_request

    info = requests.get(api_request).json()
    if requests.get(api_request).status_code != 200:
        return None
    raw_venue = info['response']['venue']

    try:
        id = raw_venue['id']
        name = raw_venue['name']
        address = raw_venue['location']['address']
        # primary_category = None
        distance = raw_venue['location']['distance']
    except:
        print("There no such fields!")

    print(id + ' -- ' + name + ' -- ' + address + ' -- ' + str(distance))

    venue = {}
    venue['id'] = id
    venue['name'] = name
    venue['address'] = address
    venue['distance'] = distance

    return venue
