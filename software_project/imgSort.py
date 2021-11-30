from PIL import Image
from PIL.ExifTags import TAGS
import os
import shutil

#사진 정보를 읽어오는 함수
def get_img_info(file_name):
    img_set = {}
    img = Image.open(file_name)
    info = img._getexif()
    if info == None:
        return None
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        img_set[decoded] = value

    return img_set['DateTime']

