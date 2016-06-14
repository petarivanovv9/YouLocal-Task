from django.shortcuts import render, redirect, HttpResponse

from local_settings import *
import requests


# Create your views here.


def index(request):
    venues = __get_venues()
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
    # print(request.POST.lists()[-1][-1][])
    # print(request.POST.lists()[-1][-1])

    print('blqblqblq')
    # print(request.POST.dict())

    #print(dir(request.POST['venues[]']))
    # print(request.POST.get('venues[]'))
    # print(request.POST.get('venues[]'))
    print('qsha')

    return redirect('index')

def __get_venues():
    api_request = URL + LL + RADIOUS + INTENT + CLIENT_ID + CLIENT_SECRET + V + LIMIT
    info = requests.get(api_request).json()

    venues = info['response']['venues']
    formated_venus = []

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

        formated_venus.append(venue)

    return formated_venus
