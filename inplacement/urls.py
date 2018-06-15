from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('dodawarka.urls')),
    path('admin/', admin.site.urls),
]
