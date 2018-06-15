from django.http import HttpResponse


def index(request):
    return HttpResponse("Hejka. Jesteś w viewsach.")
