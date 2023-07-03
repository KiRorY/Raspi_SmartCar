import Car_Control
import FaceRe
import threading
import cv2
try:
	# video_capture = cv2.VideoCapture(1)
	# video_capture.release()
	print("load finshed")
	Car_Control.init()
	goods_dict = {'黄凌博': ['一斤', '梨']}
	encode = FaceRe.image_ini(goods_dict)
	print("Init finshed")
	is_paused = [False]
	t1 = threading.Thread(target=FaceRe.find_face_and_buy, args=(goods_dict,encode,is_paused))
	t1.setDaemon(True)
	status = 7
	print ("READY!")
	Car_Control.key_scan()
	t1.start()
	while (True):
		if not is_paused[0]:
			status = Car_Control.tracking(20,20,status)
		else:
			Car_Control.brake()
		
except KeyboardInterrupt:
	pass
finally:
	Car_Control.pwm_ENA.stop()
	Car_Control.pwm_ENB.stop()
	Car_Control.GPIO.cleanup()

