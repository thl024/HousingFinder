from rest_framework import viewsets

from serializers import ApartmentSerializer
from models import Apartment

class ApartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
