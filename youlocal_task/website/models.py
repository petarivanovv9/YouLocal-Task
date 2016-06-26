from django.db import models

from djangotoolbox.fields import DictField, ListField, EmbeddedModelField

from django_mongodb_engine.contrib import MongoDBManager


class Location(models.Model):
    # address = models.CharField()
    # crossStreet = models.CharField()
    # lat = models.FloatField()
    # lng = models.FloatField()
    # distance = models.FloatField()
    # postalCode = models.CharField()
    # cc = models.CharField(),
    # city = models.CharField()
    # state = models.CharField()
    # country = models.CharField()
    # formattedAddress = ListField()
    pass


class Category(models.Model):
    pass


class Venue(models.Model):
    _id = models.CharField(max_length=255, unique=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    contact = DictField()
    location = DictField()
    # location = EmbeddedModelField(Location)
    categories = ListField()
    verified = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    objects = MongoDBManager()
