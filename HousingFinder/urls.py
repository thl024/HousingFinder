from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from views import RentalPropertyMapView
from viewsets import RentalPropertyViewSet

# Create routers (for API)
router = routers.SimpleRouter()
router.register(r'RentalProperties', RentalPropertyViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rental-property$', RentalPropertyMapView.as_view(), name='rental-property-map'),
    url(r'^api/', include(router.urls))
]
