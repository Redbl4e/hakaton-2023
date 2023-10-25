
def get_query_for_all_incedents_by_radius(params: dict) -> str:
    longitude = params.get("longitude")
    latitude = params.get("latitude")
    radius = params.get("radius")

    raw_query = f"""SELECT *
               FROM incidents_incident as i
               LEFT JOIN incidents_category AS c
               ON i.category_id = c.id
               WHERE (ST_DistanceSphere(
                 ST_MakePoint(i.longitude, i.latitude),
                 ST_MakePoint({longitude}, {latitude})
               ) <= {radius}) AND (i.is_active = True OR i.is_predictive = True);"""
    return raw_query
