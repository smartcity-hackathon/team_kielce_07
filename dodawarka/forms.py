from django import forms
from .models import Offer
from material import *

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("city","electricity","gas","water","heating","parking","gastronomy","for_sell","for_rent","type","disabled_people_friendly","surface","centre_distance","seller","rooms",)


class PricesForm(OfferForm):
    pricemin = forms.DecimalField(label="Cena minimalna")
    pricemax = forms.DecimalField(label="Cena maksymalna")
    class Meta(OfferForm.Meta):
        fields = OfferForm.Meta.fields + ('pricemin', "pricemax")