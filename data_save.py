from glob import glob
import face_recognition
from db import access_db

client, db, col, error_col = access_db()
result = col.find()
error_col = db['error']

path = 'new/'
ext = '.jpg'
for i in glob(path + '*' + ext):
  filename = i.replace(path, '')
  name = filename.replace(ext, '')
  try:
    id = face_recognition.face_encodings(face_recognition.load_image_file(i), model='large')[0]
    data = {'name': name, 'id': id.tolist()}
    col.insert_one(data)
    print(name)
  except IndexError:
    error_col.insert_one({'name': name})
    print('cannot add: ', name)

client.close()
print('finished')