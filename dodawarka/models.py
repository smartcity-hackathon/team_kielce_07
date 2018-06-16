from decimal import *
from math import atan2, cos, radians, sin, sqrt

import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

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

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if distance < 1.0:
        return str(round(distance, 2)).split('.')[1] + " m"

    return str(round(distance, 2)) + " km"


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
        dist = check_distance(cord_x, cord_y, enemy['geometry']['location']['lat'],
                              enemy['geometry']['location']['lng'])
        slow['name'] = enemy['name']
        slow['distance'] = dist
        try:
            slow['rating'] = enemy['rating']
        except KeyError:
            pass
        try:
            slow['vicinity'] = enemy['vicinity']
        except KeyError:
            pass
        data.append(slow)

    return data


class Offer(models.Model):
    """Oferta - działka/lokal inwestycyjny"""
    title = models.CharField(verbose_name="Tytuł", max_length=50)
    owner = models.ForeignKey(User,
                              verbose_name="Użytkownik",
                              on_delete=models.CASCADE,
                              related_name='offers',
                              blank=True,
                              null=True)
    # placement
    coordinates = models.CharField(verbose_name="Koordynaty", max_length=350)
    city = models.CharField(verbose_name="Miasto", max_length=50)
    address = models.CharField(verbose_name="Adres", max_length=50)
    post_code = models.CharField(verbose_name="Kod pocztowy", max_length=50)
    # pricing
    price = models.DecimalField(verbose_name="Cena", decimal_places=2, max_digits=20)
    # media
    electricity = models.BooleanField(verbose_name="Prąd", default=False)
    gas = models.BooleanField(verbose_name="Gaz", default=False)
    water = models.BooleanField(verbose_name="Woda", default=False)
    heating = models.BooleanField(verbose_name="Ogrzewanie", default=False)
    parking = models.BooleanField(verbose_name="Parking", default=False)
    gastronomy = models.BooleanField(verbose_name="Odpowiednie dla gastronomii", default=False, )
    #
    for_sell = models.BooleanField(verbose_name="Na sprzedaż", default=False)
    for_rent = models.BooleanField(verbose_name="Na wynajem", default=False)
    # type
    type = models.CharField(verbose_name="Typ", max_length=100,
                            choices=(
                                ('LOCAL', "Lokal"),
                                ('PLOT', "Działka"),
                            ), )
    disabled_people_friendly = models.BooleanField(verbose_name="Odpowiednie dla osób niepełnosprawnych", default=False)
    surface = models.DecimalField(verbose_name="Powierzchnia", max_digits=20, decimal_places=2)
    centre_distance = models.IntegerField(verbose_name="Odległość od centrum", )
    seller = models.CharField(verbose_name="Sprzedawca", max_length=100,
                              choices=(
                                  ('BUSINESS', "Firma"),
                                  ('PRIVATE', "Osoba prywatna"),
                              ), )
    rooms = models.IntegerField(verbose_name="Ilość pomieszczeń", null=True, blank=True)
    inactive = models.BooleanField(verbose_name="Nieaktywność", default=False)

    def __str__(self):
        return self.title

    def search(title='', city=None, address=None,
               post_code=None, electricity=None, gas=None,
               water=None, gastronomy=None, heating=None, for_sell=None, for_rent=None,
               type=None, disabled_people_friendly=None, surface=None,
               centre_distance=None, seller=None, rooms=None, pricemin=None,
               pricemax=None, inactive=False, parking=None, enemy_typ=None,
               enemy_radius=None):
        """
        Wyszukiwarka.
        """

        qs = Offer.objects.all()
        if title:
            qs = qs.filter(title__icontains=title)
        if pricemin:
            qs = qs.filter(price__gte=pricemin)
        if pricemax:
            qs = qs.filter(price__lte=pricemax)
        if address:
            qs = qs.filter(address__icontains=address)
        if city:
            qs = qs.filter(city__icontains=city)
        if post_code:
            qs = qs.filter(post_code=post_code)
        if centre_distance:
            qs = qs.filter(centre_distance__lte=centre_distance)
            qs = qs.filter(centre_distance__gte=centre_distance)
        if inactive:
            qs = qs.filter(inactive=True)
        ### PĘTLA DLA ODSIANYCH
        # qs = list(qs)
        results = []
        for offer in qs:
            percentage = 0
            filter_count = 0
            if surface:
                if surface > offer.surface:
                    percentage += offer.surface / surface
                    filter_count += 1
                else:
                    percentage += surface / offer.surface
                    filter_count += 1
            if rooms:
                if rooms > offer.rooms:
                    percentage += offer.rooms / rooms
                    filter_count += 1
                else:
                    percentage += Decimal(rooms) / Decimal(offer.rooms)
                    filter_count += 1
            if seller:
                if seller == offer.seller:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if electricity:
                if electricity == offer.electricity:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if gas:
                if gas == offer.gas:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if water:
                if water == offer.water:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if heating:
                if heating == offer.heating:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if for_sell:
                if for_sell == offer.for_sell:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if for_rent:
                if for_rent == offer.for_rent:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if gastronomy:
                if gastronomy == offer.gastronomy:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if parking:
                if parking == offer.parking:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1
            if disabled_people_friendly:
                if disabled_people_friendly == offer.disabled_people_friendly:
                    percentage += 1
                    filter_count += 1
                else:
                    filter_count += 1

            temp_dict = {}
            temp_dict['offer'] = offer
            if filter_count != 0:
                percentage = percentage / filter_count
                temp_dict['percentage'] = str(percentage * 100).split(".")[0] + "%"
            results.append(temp_dict)

        if enemy_typ is not None:
            for result in results:
                x = result['offer'].coordinates.split(",")[0]
                y = result['offer'].coordinates.split(",")[1]
                result['enemies'] = sorted(enemies(float(x), float(y), enemy_typ, enemy_radius),
                                           key=lambda x: x['distance'])
        try:
            return sorted(results, key=lambda x: x['percentage'], reverse=True)
        except KeyError:
            return results


class Profile(models.Model):
    """Profil użytkownika."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offers_to_compare = models.ManyToManyField(Offer)
