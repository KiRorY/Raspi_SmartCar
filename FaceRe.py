import time
from threading import Thread
import face_recognition
import cv2
import numpy as np
import pyttsx3
import os
import datetime
from typing import List, Dict
import stti
import Car_Control
import chinese_speaker

video_capture_index = 1
def image_ini(goods):
    face_image_encodings_a = []
    face_images = []
    print("loading images")
    for name in list(goods.keys()):
        face_images.append(face_recognition.load_image_file('./images' + os.sep + name + ".jpg"))
    print("loading images finished")
    print("start images encoding")
    face_image_encodings_a = []
    for face_image in face_images:
        face_image_encodings_a.append(face_recognition.face_encodings(face_image)[0])
    print("images encoding finshed")
    return face_image_encodings_a
    
def find_face_and_buy(goods, encode, is_paused):
    global video_capture_index
    print("Func Entry")
    try:
        visited = []
        cnt = 0
        for _ in goods.keys():
            visited.append(False)
        video_capture = cv2.VideoCapture(video_capture_index)
        known_face_names = list(goods.keys())
        face_image_encodings = encode
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        starttime_in = datetime.datetime.now() #开始计时
        while True:
            nowtime_o = datetime.datetime.now()
            if (nowtime_o-starttime_in).seconds >= 6:
                video_capture.release()
                #Car_Control.brake()  #小车停止
                is_paused[0] = True
                angle = 60
                Car_Control.leftrightservo_appointed_detection(angle)
                time.sleep(0.2)
                for i in range(4):
                    time.sleep(0.2)
                    video_capture = cv2.VideoCapture(video_capture_index)
                    ret, frame = video_capture.read()
                    angle += 15
                    Car_Control.leftrightservo_appointed_detection(angle)
                    time.sleep(0.1)
                    cv2.imwrite("./Image/1/" + str(i) + ".jpg", frame)
                    video_capture.release()
                    Car_Control.pwm_LeftRightServo.ChangeDutyCycle(0)
                time.sleep(0.3)
                Car_Control.leftrightservo_appointed_detection(90)
                time.sleep(0.5)
                is_paused[0] = False
                stti.stitch()
                video_capture = cv2.VideoCapture(video_capture_index)
                starttime_in = datetime.datetime.now()
            #继续图像识别
            ret, frame = video_capture.read()
            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(face_image_encodings, face_encoding)
                    name: str = "Unknown"
                    face_distances = face_recognition.face_distance(face_image_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print("find person")
                        if not visited[best_match_index]:
                            # 可以用来添加要执行的代码
                            # 当前逻辑为第一次识别到人脸时发送购买请求，当所有购买请求完成时，播报语言任务完成
                            print("I got you " + name)
                            visited[best_match_index] = True
                            say_hello_and_buy(name, goods)
                            cnt += 1
                            if cnt == len(goods):
                                time.sleep(1.5)
                                print("All finished")
                                goal_get()
                                # LED灯以0.5秒的速度进行循环，亮五秒
                                LEDThread = Thread(target=Car_Control.ColorLED, args=(0.2, 5))
                                LEDThread.setDaemon(True)
                                LEDThread.start()
                    face_names.append(name)
            process_this_frame = not process_this_frame
            """
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('Video', frame)
            """
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        video_capture.release()


def say_hello_and_buy(name: str, goods):
    hello = '早上好呀!'
    query = '请给我'
    '''
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 1.0)
    engine.setProperty('voice')
    '''

    goods_sentence = ''
    for good in goods[name]:
        goods_sentence += good
    chinese_speaker.speak(hello + name + query + goods_sentence)


def goal_get():
    chinese_speaker.speak("我滴任务完成辣!")


def goal_miss():
    chinese_speaker.speak("报告!二楼没有拿下!")


# print("load finshed")
# goods_dict = {'黄凌博': ['一斤', '梨']}
# Car_Control.init()
# print("Init finshed")

# find_face_and_buy(goods_dict)
# Car_Controlpwm_ENA.stop()
# Car_Control.pwm_ENB.stop()
# GPIO.cleanup()
