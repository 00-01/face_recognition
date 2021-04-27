import pymongo


def access_db():
    client = pymongo.MongoClient()
    db = client['face_id']
    col = db['id']
    error_col = db['error']

    return client, db, col, error_col