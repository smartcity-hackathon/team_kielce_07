from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .forms import OfferForm
from .models import Offer


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OfferForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # form.save()
            result = Offer.search(city=form.cleaned_data.get('city'),
                                  electricity=form.cleaned_data.get('electricity'),
                                  gas=form.cleaned_data.get('gas'),
                                  water=form.cleaned_data.get('water'),
                                  heating=form.cleaned_data.get('heating'),
                                  parking=form.cleaned_data.get('parking'),
                                  gastronomy=form.cleaned_data.get('gastronomy'),
                                  for_sell=form.cleaned_data.get('for_sell'),
                                  for_rent=form.cleaned_data.get('for_rent'),
                                  type=form.cleaned_data.get('type'),
                                  disabled_people_friendly=form.cleaned_data.get('disabled_people_friendly'),
                                  surface=form.cleaned_data.get('surface'),
                                  centre_distance=form.cleaned_data.get('centre_distance'),
                                  seller=form.cleaned_data.get('seller'),
                                  rooms=form.cleaned_data.get('rooms'),
                                  enemy_typ=form.cleaned_data.get('enemy_typ'),
                                  enemy_radius=form.cleaned_data.get('enemy_radius'),
                                  pricemin=form.cleaned_data.get('pricemin'),
                                  pricemax=form.cleaned_data.get('pricemax'),
                                  )
            return render(request, 'dodawarka/search_results.html', {'result': result, })
    # if a GET (or any other method) we'll create a blank form
    else:
        form = OfferForm()
    return render(request, 'dodawarka/index.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    # else:
    #     form = UserCreationForm()
    # return render(request, 'signup.html', {'form': form})
