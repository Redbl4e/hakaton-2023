from django.db.models import Func, FloatField
from firebase_admin.messaging import Message
from geopy.distance import geodesic

from incidents.models import Incident
from users.models import Coordinate


def send_push_notification_to_users(incident: Incident):
    incident_coordinates = (incident.latitude, incident.longitude)
    all_devices = Coordinate.objects.all()
    for device in all_devices:
        user_coordinates = (device.latitude, device.longitude)
        distance = geodesic(user_coordinates, incident_coordinates).kilometers
        if distance <= 1:
            device.send_message(Message(
                data={"title": "Новый инцидент в вашем районе",
                      "body": f"Адрес инцидента: {incident.address}"}))
