from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('title',)
    # title = forms.CharField(label='Tytuł', max_length=50)
    # placement
    # city = forms.CharField(label='Miasto', max_length=50)
    # address = forms.CharField(label='Adres', max_length=50)
    # post_code = forms.CharField(label='Kod pocztowy', max_length=50)
    # # pricing
    # price_min = forms.DecimalField(label='Cena minimalna', decimal_places=2, max_digits=20)
    # price_max = forms.DecimalField(label='Cena maksymalna', decimal_places=2, max_digits=20)
    # # media
    # electricity = forms.BooleanField(label='Prąd',)
    # gas = forms.BooleanField(label='gaz',)
    # water = forms.BooleanField(label='Woda',)
    # heating = forms.BooleanField(label='Ogrzewanie',)
    # parking = forms.BooleanField(label='Parking',)
    # gastronomy = forms.BooleanField(label='Odpowiednie dla gastronomii',)
    # #
    # for_sell = forms.BooleanField(label='Na sprzedaż',)
    # for_rent = forms.BooleanField(label='Do wynajęcia',)
    # # type
    # # type = forms.ChoiceField(label='Typ',
    # #                         choices=(
    # #                             ('LOCAL', "Lokal"),
    # #                             ('PLOT', "Działka"),
    # #                         ), )
    # disabled_people_friendly = forms.BooleanField(label='Miejsce przyjazne dla osób niepełnosprawnych',)
    # surface = forms.DecimalField(label='Powierzchnia w m2',max_digits=20, decimal_places=2)
    # centre_distance = forms.IntegerField(label='Odległość od centrum',)
    # # seller = forms.ChoiceField(label='Sprzedawca',
    # #                           choices=(
    # #                               ('BUSINESS', "Firma"),
    # #                               ('PRIVATE', "Osoba prywatna"),
    # #                           ), )
    # rooms = forms.IntegerField(label='Ilość pomieszczeń',)