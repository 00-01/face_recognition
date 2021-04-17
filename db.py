import pymongo


def access_db():
    client = pymongo.MongoClient()
    db = client['face_id']
    col = db['id']
    error_col = db['error']
    db.col.createIndexe({'name':1, 'id':1},{unique:True})
    # db.col.createIndex({'id':1},{unique:True})
    return client, db, col, error_col

access_db()