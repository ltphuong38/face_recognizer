import cv2
import numpy as np
import sqlite3
import os
# import sqlite3
#Thiết lập các biến
#Thiết lập biến cam dùng để sử dụng lấy ảnh
cam = cv2.VideoCapture(0)
#Thiết lập biến detector để sử dụng tải hình ảnh của gương mặt từ ảnh đã cap được
#cv2.data.haarcascades: tên của tệp mà bộ phân loại được tải
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
sampleNum = 0

#Nhập dữ liệu và kết nối với DB
def insertOrUpdate(id, name):
    #connecting to the db
    conn =sqlite3.connect("data.db")
    #check if id already exists
    query = "SELECT * FROM people WHERE ID=" + str(id)
    #trả lại dữ liệu theo hàng
    cursor = conn.execute(query)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if (isRecordExist==1):
        print('Ton tai id')
        inputA()
        #query="UPDATE User SET Name="+str(name)+" WHERE ID="+id
    else:
        query="INSERT INTO people(ID, Name) VALUES("+str(id)+",'"+str(name)+"')"
    conn.execute(query)
    conn.commit()
    conn.close()
def inputA ():
    id = input('Enter user id: ')
    name = input('Enter name: ')
    insertOrUpdate(id, name)
    return id
id1 = inputA()
while(True):

    #Chụp từng khung hình
    ret, img = cam.read()

    # Lật ảnh cho đỡ bị ngược
    img = cv2.flip(img,1)

    # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
    #img.shape =(h, w, d)
    centerH = img.shape[0] // 2;
    centerW = img.shape[1] // 2;
    sizeboxW = 300;
    sizeboxH = 400;
    cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (41, 41, 41), 3)

    # Đưa ảnh về ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Nhận diện khuôn mặt
    faces = detector.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5)

    for (x, y, w, h) in faces:
        # Vẽ hình chữ nhật quanh mặt nhận được
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # print(os.path)
        # if not os.path.exists('dataSet'):
        #    os.makedirs('dataSet')
        sampleNum = sampleNum + 1
        #Ghi dữ liệu khuôn mặt vào thư mục dataSet
        cv2.imwrite('dataSet/User.' + str(id1) +"." +str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

    #Hiển thị kết quả khung hình
    cv2.imshow('TEST', img)
    # Check xem có bấm q hoặc trên 100 ảnh sample thì thoát
    if (cv2.waitKey(1) & 0xFF == ord('q')):     
        break
    elif sampleNum > 100:
        break

#Release the capture
cam.release()
cv2.destroyAllWindows()
