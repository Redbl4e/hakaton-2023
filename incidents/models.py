from django.db import models


class Incident(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=254)
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="incidents")
    is_predictive = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_incident_name(self):
        return f"the incident {self.category} at the address: {self.address} is registered"


class Category(models.Model):
    name = models.CharField(max_length=254)
