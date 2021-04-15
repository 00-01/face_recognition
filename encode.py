import glob
import face_recognition


def db(path):

  encoded = []
  name_list = []
  error_list = []

  for i in glob.glob(path + '*.png'):
    filename = i.replace(path, '')
    name = filename.replace('.png', '')
    try:
      n = face_recognition.face_encodings(face_recognition.load_image_file(i), model='large')[0]
      encoded.append(n)
      name_list.append(name)
      print(name)
    except IndexError:
      error_list.append(name)
      print('cannot add: ', name)
  print('error_list: ', error_list)

  return encoded, name_list, error_list
