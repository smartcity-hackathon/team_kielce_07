from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import requests
from math import sin, cos, sqrt, atan2, radians
'''
BUSINESSTYPE = (
('accounting',"Rachunkowość"),
('airport',"Lotnisko"),
('amusement_park',"Park rozrywki"),
('aquarium',"Akwarium"),
('art_gallery',"Galeria sztuki"),
('atm',"Bankomat"),
('bakery',"Piekarnia"),
('bank',"Bank"),
('bar',"Bar"),
('beauty_salon',"Salon urody"),
('bicycle_store',"Sklep rowerowy"),
('bowling_alley',"Kręgielnia"),
('cafe',"Kawiarnia"),
('car_dealer',"Dealer samochodowy"),
('car_rental',"Wypożyczalnia samochodów"),
('car_repair',"Auto-naprawa"),
('car_wash',"Myjnia samochodowa"),
('clothing_store',"Sklep z ubraniami"),
('dentist',"Dentysta"),
('department_store',"Dom towarowy"),
('electronics_store',"Sklep z elektroniką"),
('florist',"Kwiaciarnia"),
('funeral_home',"Dom pogrzebowy"),
('gas_station',"Stacja benzynowa"),
('gym',"Siłownia"),
('hair_care',"Fryzjer"),
('hardware_store',"Sklep z narzędziami"),
('home_goods_store',"Sklep z artykułami domowymi"),
('insurance_agency',"Agencja ubezpieczeniowa"),
('laundry',"Pralnia"),
('lawyer',"Prawnik"),
('library',"Biblioteka"),
('liquor_store',"Sklep monopolowy"),
('locksmith',"Ślusarz"),
('meal_delivery',"Jedzenie na dowóz"),
('meal_takeaway',"Jedzenie na wynos"),
('movie_theater',"Kino"),
('moving_company',"Firma przewoźnicza"),
('museum',"Muzeum"),
('night_club',"Klub nocny"),
('pet_store',"Sklep zoologiczny"),
('pharmacy',"Apteka"),
('physiotherapist',"Fizjoterapeuta"),
('plumber',"Hydraulik"),
('post_office',"Poczta"),
('restaurant',"Restauracja"),
('shoe_store',"Sklep obuwniczy"),
('store',"Sklep"),
('supermarket',"Supermarket"),
('veterinary_care',"Opieka weterynaryjna"),
('zoo',"Zoo"),
)
'''


def check_distance(coor_x, coor_y, coor_x2, coor_y2):
    """Sprawdza dystans w km po kordach"""
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

    if distance < 1.0:
        return str(round(distance,2)).split('.')[1] + " m"

    return str(round(distance,2)) + " km"

def enemies(cord_x, cord_y, typ, radius):
    """Szuka podanego typu miejsc w podanym obrębie na podstawie API Google"""
    location = str(cord_x) + ',' + str(cord_y)
    google_api_key = getattr(settings, "GOOGLE_API_KEY", None)
    api_request = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={typ}&key={google_api_key}"
    r = requests.get(api_request)
    enemies = r.json()['results']

    data = []
    for enemy in enemies:
        slow = {}
        dist = check_distance(cord_x, cord_y, enemy['geometry']['location']['lat'], enemy['geometry']['location']['lng'])
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
    """Oferta - działka/lokal inwestycyjny"""
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
    price = models.DecimalField(decimal_places=2, max_digits=20)
    # media
    electricity = models.BooleanField(default=False)
    gas = models.BooleanField(default=False)
    water = models.BooleanField(default=False)
    heating = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    #
    for_sell = models.BooleanField(default=False)
    for_rent = models.BooleanField(default=False)
    # type
    type = models.CharField(max_length=100,
                            choices=(
                                ('PARCEL', "Parcel"),
                                ('PLACE', "Place"),
                                ('GARAGE', "Garage"),
                                ('GASTRONOMY', "Gastronomy"),
                            ), )
    disabled_people_friendly = models.BooleanField(default=False)
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
                    temp_list.append(sorted(enemies(float(x), float(y), enemy_typ, enemy_radius), key=lambda x: x['distance']))
                    results.append(temp_list)
                return results
            else:
                return qs
