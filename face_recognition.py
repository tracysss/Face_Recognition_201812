# 2018-12
# Tracy Song-Brink
# Purpose: recognize a specific face in pictures 

from PIL import Image, ImageDraw
import face_recognition
import os
import sys
from datetime import datetime 
sys.path.append('D:/Users/Tracy S/AppData/Local/Programs/Python/Python36-32/Lib/site-packages')
import shutil
import pandas

def create_thumbnails(file_name):
    #print('Creating thumbnails for picture: '+ file_name)
    if file_name[-4]=='.':
        file_name_short=file_name[:len(file_name)-4]
    else:
        file_name_short=file_name[:len(file_name)-5]

    image = face_recognition.load_image_file(file_path+file_name)
    face_locations = face_recognition.face_locations(image)
    
    print("{} face(s) found in this photograph.".format(len(face_locations)))
    i=0

    for face_location in face_locations:
        i=i+1
        # Print the location of each face in this image
        top, right, bottom, left = face_location
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()
        #pil_image.save(file_path+"thumbnails/"+file_name_short+"_"+str(i)+".jpg")

def show_landmark(image):
    face_landmarks_list = face_recognition.face_landmarks(image)
    # Create a PIL imagedraw object so we can draw on the picture
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)

    for face_landmarks in face_landmarks_list:

        # Print the location of each facial feature in this image
        for facial_feature in face_landmarks.keys():
            print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

        # Let's trace out each facial feature in the image with a line!
        for facial_feature in face_landmarks.keys():
            d.line(face_landmarks[facial_feature], width=5)

    # Show the picture
    pil_image.show()

def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

def get_all_info(path):
    return Image.open(path)._getexif()

def recognize_it(file_path_test,unknown_image_file_name):
    print('trying to recognize: '+unknown_image_file_name)
    unknown_image = face_recognition.load_image_file(file_path_test+unknown_image_file_name)
    unknown_face_encoding_list = face_recognition.face_encodings(unknown_image)

    known_faces = [jonathan_face_encoding]

    ## results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    if len(unknown_face_encoding_list)>0:
        for unknown_face_encoding in unknown_face_encoding_list:
            results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
            file_path_list.append(file_path_test)
            file_name_list.append(unknown_image_file_name)
            jonathan_flag_list.append(results[0])
            others_flag_list.append(not True in results)
            if results[0]:
                shutil.copy2(file_path_test+unknown_image_file_name, file_path_test+'Jonathan/')



#generate thumbnails from original pictures
file_path='D:/Users/Tracy S/Desktop/face recognition/photos/test/'
file_names=os.listdir(file_path)
total=0
for file in file_names:
    if file.find('.')>-1:
       create_thumbnails(file)
       total=total+1
print(str(total)+' pictures processed to create thumbnails')

# initialize lists
file_name_list=[]
file_path_list=[]
jonathan_flag_list=list()
others_flag_list=list()


file_path='D:/Users/Tracy S/Desktop/face recognition/photos/Model/'
jonathan_file_name_full='Jonathan.jpg'
jonathan_image = face_recognition.load_image_file(file_path+jonathan_file_name_full)
jonathan_face_encoding = face_recognition.face_encodings(jonathan_image)[0]
#print(jonathan_face_encoding)


# Find Jonathan pictures
file_path_test='D:/Users/Tracy S/Desktop/face recognition/photos/test/thumbnails/'
total=0
file_names=os.listdir(file_path_test)
for file in file_names:
    if file.find('.jpg')>-1:
        recognize_it(file_path_test,file)
        total=total+1

print(str(total)+' pictures processed to create thumbnails')
photo_results = {'File Path': file_path_list,
                 'File Name': file_name_list,
                 'Jonathan': jonathan_flag_list,
                 'Others': others_flag_list
        }
df = pandas.DataFrame(photo_results)
df.to_csv(file_path_test+'results_'+str(datetime.now()).replace(':','-')[:19]+'.csv')




print("end of program")
print('Current Time:' + str(datetime.now())[:19])

