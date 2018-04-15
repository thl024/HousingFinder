from django.views.generic.list import ListView

from models import Apartment

from db import get_db

class HousingMapView(ListView):

    model = Apartment
    template_name = 'housing_map.html'

    def get_queryset(self):
        apartments = Apartment.objects.all()
        print(apartments)
        return apartments