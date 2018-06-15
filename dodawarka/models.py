from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='offers',
                              blank=True,
                              null=True)
    # placement
    coordinates = models.TextField()
    address = models.CharField(max_length=50)
    post_code = models.CharField(max_length=50)
    # pricing
    price = models.IntegerField()
    # media
    electricity = models.BooleanField()
    gas = models.BooleanField()
    water = models.BooleanField()
    heating = models.BooleanField()
    #
    for_sell = models.BooleanField()
    for_rent = models.BooleanField()
    # type
    type = models.CharField(max_length=100,
                            choices = (
                                        ('PARCEL', "Parcel"),
                                        ('PLACE', "Place"),
                                        ('GARAGE', "Garage"),
                                        ('GASTRONOMY', "Gastronomy"),
                                        ('PARKING', "Parking"),
                                        ),)
    disabled_people_friendly = models.BooleanField()
    surface = models.IntegerField()
    centre_distance = models.IntegerField()
    seller = models.CharField(max_length=50)
    rooms = models.IntegerField()
