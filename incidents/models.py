from django.db import models

from users.models import User


def _get_file_path(instance, filename: str) -> str:
    return f'posts/{instance.incident.pk}/{filename}'


class Incident(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    address = models.CharField(max_length=254)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='incidents')
    is_predictive = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_incident_name(self):
        return f'the incident {self.category} at the address: {self.address} is registered'


class Category(models.Model):
    name = models.CharField(max_length=254)


class PostIncident(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='incidents')
    title = models.CharField(max_length=254)
    photo = models.FileField(upload_to=_get_file_path, blank=True, null=True)
    incident = models.ForeignKey('Incident', on_delete=models.PROTECT, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'incidents_post_incident'
