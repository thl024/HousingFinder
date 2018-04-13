from django.views.generic.list import ListView

from models import Apartment

class HousingMapView(ListView):

	model = Apartment
	template_name = 'housing_map.html'

	# def get_query_set(self):
	# 	return Apartment.objects.all()