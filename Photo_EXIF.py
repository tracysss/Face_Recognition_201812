from PIL import Image, ImageDraw
import os
import sys
from datetime import datetime 
import shutil
import pandas


print(datetime.now())

# initialize lists
file_path_list=list()
file_name_list=list()
lat=list()
long=list()
taken_date_full=list()
taken_date=list()
taken_time=list()
width=list()
height=list()
model1=list()
brand2=list()
model2=list()
alt=list()


def get_exif(file_name):
    file_path_list.append(file_path)
    file_name_list.append(file_name)
    path=file_path+file_name

    exif=Image.open(path)._getexif()
    if not exif is None:
        if 36867 in exif:
            taken_date_full.append(exif[36867])
            taken_date.append(exif[36867][:10])
            taken_time.append(exif[36867][11:])
        else:
            taken_date_full.append('')
            taken_date.append('')
            taken_time.append('')

        if 40963 in exif: 
            width.append(exif[40963])
        else:
            width.append('')

        if 40962 in exif: 
            height.append(exif[40962])
        else:
            height.append('')

        if 42036 in exif: 
            model1.append(exif[42036])
        else:
            model1.append('')

        if 271 in exif: 
            brand2.append(exif[271])
        else:
            brand2.append('')

        if 272 in exif: 
            model2.append(exif[272])
        else:
            model2.append('')

        if 34853 in exif:
            if 2 in exif[34853]:
                lat.append(exif[34853][2])
            else:
                lat.append('')
            if 4 in exif[34853]:
                long.append(exif[34853][4])
            else:
                long.append('')
            if 6 in exif[34853]:
                alt.append(exif[34853][6])
            else:
                alt.append('')
        else:
            lat.append('')
            long.append('')
            alt.append('')
    else:
        taken_date_full.append('')
        taken_date.append('')
        taken_time.append('')
        width.append('')
        height.append('')
        model1.append('')
        brand2.append('')
        model2.append('')
        lat.append('')
        long.append('')
        alt.append('')


file_path="D:/Users/Tracy S/Desktop/face recognition/photos/"
file_names=os.listdir(file_path)
total=0
for file in file_names:
    if file.find('.jpg')>-1 or file.find('.jpeg')>-1 or file.find('.JPG')>-1:
       get_exif(file)
       total=total+1
print('file path:'+file_path)
print(str(total)+' pictures processed to create exif')

photo_exif= {'File Path': file_path_list,
             'File Name': file_name_list,
             'Latitude': lat,
             'Longitude': long,
             'Altitude': alt,
             'Date Time': taken_date_full,
             'Date': taken_date,
             'Time': taken_time,
             'Width': width,
             'Height': height,
             'Brand': brand2,
             'Model1': model1,
             'Model2': model2
        }
df = pandas.DataFrame(photo_exif)
file_path="D:/Users/Tracy S/Desktop/face recognition/photos/"
df.to_csv(file_path+'exif_'+str(datetime.now()).replace(':','-')[:19]+'.csv')





print('Current Time:' + str(datetime.now())[:19])
print("end of program")
