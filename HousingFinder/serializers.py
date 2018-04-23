from rest_framework.serializers import Serializer, CharField, DecimalField, ListField, \
    IntegerField, DateField, DateTimeField


class RentalPropertySerializer(Serializer):
    # Details
    name = CharField()
    address = CharField()  # Not always available
    latitude = DecimalField(max_digits=10, decimal_places=8)
    longitude = DecimalField(max_digits=11, decimal_places=8)
    offered_by = CharField(allow_null=True)
    description = ListField()

    # Dates
    date_available = DateField()
    post_date = DateTimeField()  # Only applicable for certain websites

    # Costs
    rent_price = DecimalField(max_digits=20, decimal_places=2)
    application_fee = DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    security_deposit = DecimalField(max_digits=10, decimal_places=2, allow_null=True)

    # Features
    size = DecimalField(max_digits=12, decimal_places=2, allow_null=True)
    bedrooms = IntegerField()
    bathrooms = IntegerField()
    amenities = ListField(allow_null=True)  # Interrelated with description; text parsing methods?
    tags = ListField()

    # URL Data
    listing_url = CharField()
