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
    coordinates = models.TextField(default='20.658282278106647, 50.88448318784885')
    address = models.CharField(max_length=50, default=' ')
    post_code = models.CharField(max_length=50, default=' ')
    # pricing
    price = models.IntegerField(default=0)
    # media
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    #
    for_sell = models.BooleanField(default=True)
    for_rent = models.BooleanField(default=False)
    # type
    type = models.CharField(max_length=100,
                            choices = (
                                        ('PARCEL', "Parcel"),
                                        ('PLACE', "Place"),
                                        ('GARAGE', "Garage"),
                                        ('GASTRONOMY', "Gastronomy"),
                                        ('PARKING', "Parking"),
                                        ),
                            default='PARCEL')
    disabled_people_friendly = models.BooleanField(default=False)
    surface = models.IntegerField(default=0)
    centre_distance = models.IntegerField(default=0)
    seller = models.CharField(max_length=50, default=' ')
    rooms = models.IntegerField(default=1)
