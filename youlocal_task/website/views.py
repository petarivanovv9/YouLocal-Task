from django.shortcuts import render, HttpResponse

from local_settings import *
import requests


# Create your views here.


def index(request):
    #raw_venues = __get_venues()
    return render(request, 'index.html', locals())


def __get_venues():
    api_request = URL + LL + RADIOUS + INTENT + CLIENT_ID + CLIENT_SECRET + V + LIMIT
    info = requests.get(api_request).json()
    return info
