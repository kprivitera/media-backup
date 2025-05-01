from database.queries import RETRIEVE_MEDIA_BY_DATE


def retrieve_media_by_date(db, month, year, user_id):
    query = RETRIEVE_MEDIA_BY_DATE
    params = (month, year, user_id)
    return db.execute_query(query, params)
