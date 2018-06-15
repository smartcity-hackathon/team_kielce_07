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
    inactive = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def search(title='', owner=None, coordinates=None, address=None,
               post_code=None, electricity=None, gas=None,
               water=None, heating=None, for_sell=None, for_rent=None,
               type=None, disabled_people_friendly=None, surface=None,
               centre_distance=None, seller=None, rooms=None,
               pricemin=None, pricemax=None, inactive=False):

        """
        Wyszukiwarka.
        """

        qs = Offer.objects.all()

        if title:
            qs = qs.filter(name__icontains=title)

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

        return qs
