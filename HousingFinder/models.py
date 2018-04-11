from django.db import models

from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField

class Apartment(models.Model):
    # Details
    name = models.TextField()
    address = models.TextField()
    offered_by = models.TextField()
    description = models.TextField()

    # Dates
    date_available = models.DateField()
    post_date = models.DateTimeField() # Only applicable for certain websites

    # Costs
    rent_price = models.DecimalField(max_digits=20, decimal_places=2)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)

    # Features
    size = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    amenities = ListField() # Interrelated with description; text parsing methods?
    tags = ListField()

    # URL Data
    listing_url = models.TextField()