from rest_framework import viewsets

from models import RentalProperty
from serializers import RentalPropertySerializer


class RentalPropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RentalProperty.objects.all()
    serializer_class = RentalPropertySerializer
