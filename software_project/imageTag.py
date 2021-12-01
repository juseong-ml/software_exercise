from PIL import Image
import piexif

img = Image.open('images/junghwa_001.jpg')

if 'exif' not in img.info.keys(): # 이미지 파일에 exif 메타정보가 없으면 생성하고
    zeroth_ifd = {
                  # piexif.ImageIFD.Make:u"lovley",
                  piexif.ImageIFD.XResolution: (0,0),
                  piexif.ImageIFD.YResolution: (0,0),
                  piexif.ImageIFD.Software: u"piexif"
        }
    exif_idf = {piexif.ExifIFD.DateTimeOriginal:u"2021:11:27 20:30:10",
                piexif.ExifIFD.LensMake:u"LensMake",
                piexif.ExifIFD.Sharpness:65535,
                piexif.ExifIFD.LensSpecification: ((1,1), (1,1), (1,1), (1,1))}
    gps_ifd = {piexif.GPSIFD.GPSVersionID:(2,0,0,0),
               piexif.GPSIFD.GPSAltitudeRef:1,
               piexif.GPSIFD.GPSDateStamp: u"1999:99:99 99:99:99"}
    first_ifd = {piexif.ImageIFD.Make:u"junghwa",
                 piexif.ImageIFD.XResolution:(40,1),
                 piexif.ImageIFD.YResolution:(40,1),
                 piexif.ImageIFD.Software:u"piexif"
                 }
    exif_dict = {"0th" : zeroth_ifd, "Exif" : exif_idf, "GPS" : gps_ifd, "1st" : first_ifd}
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, 'images/junghwa_001.jpg')

# else: # 메타 정보가 있으면 270번 위치에 원하는 텍스트를 부여한 후, 저장한다.
#     exif_dict = piexif.load(img.info['exif'])
#     exif_dict['0th'][270] = u'lovely'
#     exif_bytes = piexif.dump(exif_dict)
#     new_file = 'images/junghwa_001.jpg'
#     img.save(new_file, 'jpg', exif=exif_bytes)
img = Image.open('images/junghwa_001.jpg')
print(img.info.items())