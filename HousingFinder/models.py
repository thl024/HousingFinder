from django.db import models

from djangotoolbox.fields import ListField
from djangotoolbox.fields import EmbeddedModelField

class Apartment(models.Model):
	location = models.TextField()
	price = models.TextField()
