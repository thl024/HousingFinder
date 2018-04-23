from django.db import models

from djangotoolbox.fields import ListField


class RentalProperty(models.Model):
    # Details
    name = models.TextField()
    address = models.TextField()  # Not always available
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    offered_by = models.TextField(null=True)
    description = ListField()

    # Dates
    date_available = models.DateField()
    post_date = models.DateTimeField()  # Only applicable for certain websites

    # Costs
    rent_price = models.DecimalField(max_digits=20, decimal_places=2)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Features
    size = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    amenities = ListField(null=True)  # Interrelated with description; text parsing methods?
    tags = ListField()

    # URL Data
    listing_url = models.TextField()
