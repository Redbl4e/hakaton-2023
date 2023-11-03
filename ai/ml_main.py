from datetime import datetime

from ai.data_preparation import prepare_data
from ai.model import training_model_and_predict_incidents_ai
from incidents.models import Incident, PostIncident, Category


def getting_data_from_db():
    massiv_with_incidents = []

    query = Incident.objects.filter(is_predictive=False).order_by("created_at").\
        prefetch_related("Category")
    for row in query:
        massiv_with_incidents.append([float(row.longitude),
                                      float(row.latitude),
                                      str(row.address),
                                      str(row.created_at),
                                      str(row.category.name)
                                      ])

    return massiv_with_incidents


def writing(incident_info: list[float, float, str, str, str], prediction_percent: float):
    longitude, latitude, address, date_, category = incident_info
    date_ = datetime.strptime(date_, "%Y-%m-%d %H:%M:%S")
    category_id = Category.objects.get(name=str(category)).id
    incident = Incident.objects.create(
        longitude=longitude,
        latitude=latitude,
        category=category_id,
        address=address,
        is_predictive=True,
        is_active=False,
        created_at=date_
    )
    if prediction_percent > 0.99:
        prediction_percent = 95
    else:
        prediction_percent = round(prediction_percent * 1000, 2)
        if 300 > prediction_percent > 100:
            prediction_percent = 73
    prediction_title = f"Возможность данного события равна {prediction_percent} %"

    post_incident = PostIncident.objects.create(
        title=prediction_title,
        incident=incident,
        user_id=4,
        photo=None,
        created_at=datetime.now()
    )


def main():
    massiv_with_incidents = getting_data_from_db()
    clear_data = prepare_data(massiv_with_incidents)
    predict_data = training_model_and_predict_incidents_ai(clear_data)
    for item in predict_data:
        writing(item[0], item[1])


if __name__ == "__main__":
    main()
