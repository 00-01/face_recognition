import sys
from PIL import Image
from io import BytesIO
from db import access_db


_, _, col, error_col = access_db()
find = {'name':'00'}

def show_photo():
    n = col.find(find)
    for i in n:
        a = i['photo']
        stream = BytesIO(a)
        image = Image.open(stream).convert("RGBA")
        stream.close()
        image.show()

show_photo()