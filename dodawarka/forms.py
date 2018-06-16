from django import forms

from .models import Offer

BUSINESSTYPE = (
    ('accounting', "Rachunkowość"),
    ('airport', "Lotnisko"),
    ('amusement_park', "Park rozrywki"),
    ('aquarium', "Akwarium"),
    ('art_gallery', "Galeria sztuki"),
    ('atm', "Bankomat"),
    ('bakery', "Piekarnia"),
    ('bank', "Bank"),
    ('bar', "Bar"),
    ('beauty_salon', "Salon urody"),
    ('bicycle_store', "Sklep rowerowy"),
    ('bowling_alley', "Kręgielnia"),
    ('cafe', "Kawiarnia"),
    ('car_dealer', "Dealer samochodowy"),
    ('car_rental', "Wypożyczalnia samochodów"),
    ('car_repair', "Auto-naprawa"),
    ('car_wash', "Myjnia samochodowa"),
    ('clothing_store', "Sklep z ubraniami"),
    ('dentist', "Dentysta"),
    ('department_store', "Dom towarowy"),
    ('electronics_store', "Sklep z elektroniką"),
    ('florist', "Kwiaciarnia"),
    ('funeral_home', "Dom pogrzebowy"),
    ('gas_station', "Stacja benzynowa"),
    ('gym', "Siłownia"),
    ('hair_care', "Fryzjer"),
    ('hardware_store', "Sklep z narzędziami"),
    ('home_goods_store', "Sklep z artykułami domowymi"),
    ('insurance_agency', "Agencja ubezpieczeniowa"),
    ('laundry', "Pralnia"),
    ('lawyer', "Prawnik"),
    ('library', "Biblioteka"),
    ('liquor_store', "Sklep monopolowy"),
    ('locksmith', "Ślusarz"),
    ('meal_delivery', "Jedzenie na dowóz"),
    ('meal_takeaway', "Jedzenie na wynos"),
    ('movie_theater', "Kino"),
    ('moving_company', "Firma przewoźnicza"),
    ('museum', "Muzeum"),
    ('night_club', "Klub nocny"),
    ('pet_store', "Sklep zoologiczny"),
    ('pharmacy', "Apteka"),
    ('physiotherapist', "Fizjoterapeuta"),
    ('plumber', "Hydraulik"),
    ('post_office', "Poczta"),
    ('restaurant', "Restauracja"),
    ('shoe_store', "Sklep obuwniczy"),
    ('store', "Sklep"),
    ('supermarket', "Supermarket"),
    ('veterinary_care', "Opieka weterynaryjna"),
    ('zoo', "Zoo"),
)


class OfferForm(forms.ModelForm):
    pricemin = forms.DecimalField(label="Cena minimalna (zł)")
    pricemax = forms.DecimalField(label="Cena maksymalna (zł)")
    enemy_typ = forms.ChoiceField(label="Wybierz branżę do sprawdzenia", choices=BUSINESSTYPE)
    enemy_radius = forms.IntegerField(label="Promień sprawdzania obiektów (m)")

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['electricity'].required = False
        self.fields['gas'].required = False
        self.fields['water'].required = False
        self.fields['heating'].required = False
        self.fields['parking'].required = False
        self.fields['gastronomy'].required = False
        self.fields['for_sell'].required = False
        self.fields['for_rent'].required = False
        self.fields['type'].required = False
        self.fields['disabled_people_friendly'].required = False
        self.fields['surface'].required = False
        self.fields['centre_distance'].required = False
        self.fields['seller'].required = False
        self.fields['rooms'].required = False
        self.fields['pricemin'].required = False
        self.fields['pricemax'].required = False
        self.fields['enemy_typ'].required = False
        self.fields['enemy_radius'].required = False

    class Meta:
        model = Offer
        fields = (
            "city", "electricity", "gas", "water", "heating", "parking", "gastronomy", "for_sell", "for_rent", "type",
            "disabled_people_friendly", "surface", "centre_distance", "seller", "rooms",)
