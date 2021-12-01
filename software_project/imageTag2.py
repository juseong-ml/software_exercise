from PIL.ExifTags import TAGS
from PIL import Image
import piexif


img_path = 'insta_images/jusep.v_1.jpg'
img = Image.open(img_path)
# info = img._getexif()

tmp = input('태그를 입력하세요 : ')

print(img.info.items())
# print(tmp)
if 'exif' not in img.info.keys():
    tag = {
        piexif.ImageIFD.XPKeywords: tmp.encode('utf-8')
    }
    exif_dict = {'tag' : tag}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, img_path)

else:
    exif_dict = piexif.load(img.info['exif'])
    exif_dict['tag'][20] = tmp.encode('utf-8')
    exif_bytes = piexif.dump(exif_dict)
    new_file = img_path
    img.save(new_file, 'jpg', exif=exif_bytes)

# new_img = Image.open(img_path)
# print(new_img.info.items())
# print(new_img.info['exif'].decode('utf-8'))