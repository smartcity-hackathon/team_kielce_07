from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import requests
from math import sin, cos, sqrt, atan2, radians


def check_distance(coor_x, coor_y, coor_x2, coor_y2):
    R = 6373.0

    lat1 = radians(coor_x)
    lon1 = radians(coor_y)
    lat2 = radians(coor_x2)
    lon2 = radians(coor_y2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return round(distance,2)

def enemies(cord_x, cord_y, typ, radius):
    location = str(cord_x) + ',' + str(cord_y)
    google_api_key = getattr(settings, "GOOGLE_API_KEY", None)
    api_request = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={typ}&key={google_api_key}"
    r = requests.get(api_request)
    enemies = r.json()['results']

    data = []
    for enemy in enemies:
        slow = {}
        dist = check_distance(cord_x, cord_y, enemies[1]['geometry']['location']['lat'], enemies[1]['geometry']['location']['lng'])
        slow['name'] = enemy['name']
        slow['distance'] = dist
        try:
            slow['rating'] = enemy['rating']
        except KeyError:
            pass
        slow['vicinity'] = enemy['vicinity']
        data.append(slow)

    return data

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
                            choices=(
                                ('PARCEL', "Parcel"),
                                ('PLACE', "Place"),
                                ('GARAGE', "Garage"),
                                ('GASTRONOMY', "Gastronomy"),
                                ('PARKING', "Parking"),
                            ), )
    disabled_people_friendly = models.BooleanField()
    surface = models.IntegerField()
    centre_distance = models.IntegerField()
    seller = models.CharField(max_length=50)
    rooms = models.IntegerField()
    inactive = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def search(title='', owner=None, coordinates=None, address=None,
                   post_code=None, electricity=None, gas=None,
                   water=None, heating=None, for_sell=None, for_rent=None,
                   type=None, disabled_people_friendly=None, surface=None,
                   centre_distance=None, seller=None, rooms=None,
                   pricemin=None, pricemax=None, inactive=False,
                   enemy_typ=None, enemy_radius=None):
            """
            Wyszukiwarka.
            """
            qs = Offer.objects.all()
            if title:
                qs = qs.filter(title__icontains=title)
            if owner:
                qs = qs.filter(owner=owner)
            if pricemin:
                qs = qs.filter(price__gte=pricemin)
            if pricemax:
                qs = qs.filter(price__lte=pricemax)
            if address:
                qs = qs.filter(address__icontains=address)
            if coordinates:
                qs = qs.filter(coordinates=coordinates)
            if post_code:
                qs = qs.filter(post_code=post_code)
            if electricity:
                qs = qs.filter(electricity=True)
            elif electricity == False:
                qs = qs.filter(electricity=False)
            if gas:
                qs = qs.filter(gas=True)
            elif gas == False:
                qs = qs.filter(gas=False)
            if water:
                qs = qs.filter(water=True)
            elif water == False:
                qs = qs.filter(water=False)
            if heating:
                qs = qs.filter(heating=True)
            elif heating == False:
                qs = qs.filter(heating=False)
            if for_sell:
                qs = qs.filter(for_sell=True)
            elif for_sell == False:
                qs = qs.filter(for_sell=False)
            if for_rent:
                qs = qs.filter(for_rent=True)
            elif for_rent == False:
                qs = qs.filter(for_rent=False)
            if disabled_people_friendly:
                qs = qs.filter(disabled_people_friendly=True)
            elif disabled_people_friendly == False:
                qs = qs.filter(disabled_people_friendly=False)
            if inactive:
                qs = qs.filter(active=False)

            qs = list(qs)
            results = []
            if enemy_typ is not None:
                for result in qs:
                    temp_list = []
                    x = result.coordinates.split(",")[0]
                    y = result.coordinates.split(",")[1]
                    temp_list.append(result)
                    temp_list.append(enemies(float(x), float(y), enemy_typ, enemy_radius))
                    results.append(temp_list)
                return results
            else:
                return qs
