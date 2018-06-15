from django.http import HttpResponse
from django.template import loader

from .models import Offer


def index(request):
    offers = Offer.objects.all()
    template = loader.get_template('dodawarka/index.html')
    context = {
        'offers': offers,
    }
    return HttpResponse(template.render(context, request))
