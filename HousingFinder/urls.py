from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from viewsets import ApartmentViewSet
from views import HousingMapView

# Create routers (for API)
router = routers.SimpleRouter()
router.register(r'apartments', ApartmentViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^housing/', HousingMapView.as_view(), name='housing-map'),
    url(r'^api/', include(router.urls))
]
