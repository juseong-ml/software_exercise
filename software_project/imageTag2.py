from PIL.ExifTags import TAGS
from PIL import Image

img = Image.open('images/junghwa_001.jpg')
info = img._getexif()
img.close()

tagLable = {}

for tag, value in info.items():
    decoded = TAGS.get(tag,tag)
    tagLable[decoded] = value

print(tagLable)