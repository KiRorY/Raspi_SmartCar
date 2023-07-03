#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#小车按键定义
key = 8

#循迹红外引脚定义
#TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1  =  3   #定义左边第一个循迹红外传感器引脚为3口
TrackSensorLeftPin2  =  5   #定义左边第二个循迹红外传感器引脚为5口
TrackSensorRightPin1 =  4   #定义右边第一个循迹红外传感器引脚为4口
TrackSensorRightPin2 =  18  #定义右边第二个循迹红外传感器引脚为18口

#超声波引脚定义
EchoPin = 0
TrigPin = 1

#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24

#舵机引脚定义
ServoPin = 23
ServoUpDownPin = 9
ServoLeftRightPin = 11
#红外避障引脚定义
AvoidSensorLeft = 12
AvoidSensorRight = 17

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#电机引脚初始化为输出模式
#按键引脚初始化为输入模式
#超声波,RGB三色灯,舵机引脚初始化
#红外避障引脚初始化
def init():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	global pwm_ENA
	global pwm_ENB
	global pwm_servo
	global pwm_LeftRightServo
	global pwm_UpDownServo
	GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
	GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
	GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
	GPIO.setup(key,GPIO.IN)
	GPIO.setup(EchoPin,GPIO.IN)
	GPIO.setup(TrigPin,GPIO.OUT)
	GPIO.setup(LED_R, GPIO.OUT)
	GPIO.setup(LED_G, GPIO.OUT)
	GPIO.setup(LED_B, GPIO.OUT)
	GPIO.setup(ServoPin, GPIO.OUT)
	GPIO.setup(AvoidSensorLeft,GPIO.IN)
	GPIO.setup(AvoidSensorRight,GPIO.IN)
	GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
	GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
	GPIO.setup(TrackSensorRightPin1,GPIO.IN)
	GPIO.setup(TrackSensorRightPin2,GPIO.IN)
	GPIO.setup(ServoUpDownPin, GPIO.OUT)
	GPIO.setup(ServoLeftRightPin, GPIO.OUT)
	#设置pwm引脚和频率为1000hz
	pwm_ENA = GPIO.PWM(ENA, 1000)
	pwm_ENB = GPIO.PWM(ENB, 1000)
	pwm_ENA.start(0)
	pwm_ENB.start(0)
	# 设置舵机的频率和起始占空比
	pwm_servo = GPIO.PWM(ServoPin, 50)
	pwm_UpDownServo = GPIO.PWM(ServoUpDownPin, 50)
	pwm_LeftRightServo = GPIO.PWM(ServoLeftRightPin, 50)
	pwm_servo.start(0)
	pwm_UpDownServo.start(0)
	pwm_LeftRightServo.start(0)
	pwm_LeftRightServo.ChangeDutyCycle(0)
	
#小车前进	
def run(leftspeed, rightspeed):
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)

#小车后退
def back(leftspeed, rightspeed):
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.HIGH)
	GPIO.output(IN3, GPIO.LOW)
	GPIO.output(IN4, GPIO.HIGH)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)
	
#小车左转	
def left(leftspeed, rightspeed):
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)

#小车右转
def right(leftspeed, rightspeed):
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.LOW)
	GPIO.output(IN4, GPIO.LOW)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)
	
#小车原地左转
def spin_left(leftspeed, rightspeed):
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.HIGH)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)

#小车原地右转
def spin_right(leftspeed, rightspeed):
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.LOW)
	GPIO.output(IN4, GPIO.HIGH)
	pwm_ENA.ChangeDutyCycle(leftspeed)
	pwm_ENB.ChangeDutyCycle(rightspeed)

#小车停止	
def brake():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)
   GPIO.output(IN4, GPIO.LOW)

#按键检测
def key_scan():
	while GPIO.input(key):
		pass
	while not GPIO.input(key):
		time.sleep(0.01)
		if not GPIO.input(key):
			time.sleep(0.01)
			while not GPIO.input(key):
				pass

def ColorLED(wait_time: float, lighting_time: float):
	# 循环显示7种不同的颜色
	times = lighting_time / wait_time / 7
	cnt = 0
	# 设置RGB三色灯为BCM编码方式
	# RGB三色灯设置为输出模式
	GPIO.setup(LED_R, GPIO.OUT)
	GPIO.setup(LED_G, GPIO.OUT)
	GPIO.setup(LED_B, GPIO.OUT)
	while cnt <= round(times):
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		time.sleep(wait_time)
		GPIO.output(LED_R, GPIO.LOW)
		GPIO.output(LED_G, GPIO.HIGH)
		GPIO.output(LED_B, GPIO.LOW)
		time.sleep(wait_time)
		GPIO.output(LED_R, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.HIGH)
		time.sleep(wait_time)
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_G, GPIO.HIGH)
		GPIO.output(LED_B, GPIO.LOW)
		time.sleep(wait_time)
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.HIGH)
		time.sleep(wait_time)
		GPIO.output(LED_R, GPIO.LOW)
		GPIO.output(LED_G, GPIO.HIGH)
		GPIO.output(LED_B, GPIO.HIGH)
		time.sleep(wait_time)
		GPIO.output(LED_R, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
		time.sleep(wait_time)
		cnt += 1			


#超声波函数
'''
def Distance_test():
	GPIO.output(TrigPin,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TrigPin,GPIO.LOW)
	while not GPIO.input(EchoPin):
		pass
	t1 = time.time()
	while GPIO.input(EchoPin):
		pass
	t2 = time.time()
	print "distance is %d " % (((t2 - t1)* 340 / 2) * 100)
	time.sleep(0.01)
	return ((t2 - t1)* 340 / 2) * 100
'''
def Distance():
	GPIO.output(TrigPin,GPIO.LOW)
	time.sleep(0.000002)
	GPIO.output(TrigPin,GPIO.HIGH)
	time.sleep(0.000015)
	GPIO.output(TrigPin,GPIO.LOW)
	t3 = time.time()
	while not GPIO.input(EchoPin):
		t4 = time.time()
		if (t4 - t3) > 0.03 :
			return -1
	t1 = time.time()
	while GPIO.input(EchoPin):
		t5 = time.time()
		if(t5 - t1) > 0.03 :
			return -1
	t2 = time.time()
#    print "distance is %d " % (((t2 - t1)* 340 / 2) * 100)
	return ((t2 - t1)* 340 / 2) * 100

def Distance_test():
	num = 0
	ultrasonic = []
	while num < 5:
			distance = Distance()
			while int(distance) == -1 :
				distance = Distance()
				print("Tdistance is %f"%(distance) )
			while (int(distance) >= 500 or int(distance) == 0) :
				distance = Distance()
				print("Edistance is %f"%(distance) )
			ultrasonic.append(distance)
			num = num + 1
			time.sleep(0.01)
	print (ultrasonic)
	distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3])/3
	print("distance is %f"%(distance) )
	return distance


	
#舵机旋转到指定角度
#前舵机旋转到指定角度
def servo_appointed_detection(pos):
	for i in range(18):
		pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)


#摄像头舵机左右旋转到指定角度
def leftrightservo_appointed_detection(pos):
	for i in range(1):
		pwm_LeftRightServo.ChangeDutyCycle(2.5 + 10 * pos/180)
		time.sleep(0.02)							#等待20ms周期结束
	#pwm_LeftRightServo.ChangeDutyCycle(0)	#归零信号

	#摄像头舵机上下旋转到指定角度
def updownservo_appointed_detection(pos):
	for i in range(1):
		pwm_UpDownServo.ChangeDutyCycle(2.5 + 10 * pos/180)
		time.sleep(0.02)							#等待20ms周期结束
	#pwm_UpDownServo.ChangeDutyCycle(0)	#归零信号

#舵机旋转超声波测距避障，led根据车的状态显示相应的颜色
def servo_color_carstate():
	#开红灯
	GPIO.output(LED_R, GPIO.HIGH)
	GPIO.output(LED_G, GPIO.LOW)
	GPIO.output(LED_B, GPIO.LOW)
	# back(20, 20)
	# time.sleep(0.08)
	brake()
	servo_appointed_detection(60)
	time.sleep(0.8)
	rightdistance = Distance_test()
  

	servo_appointed_detection(120)
	time.sleep(0.8)
	leftdistance = Distance_test()

	#舵机旋转到90度，即前方，测距
	servo_appointed_detection(90)
	time.sleep(0.8)
	frontdistance = Distance_test()
 
	if leftdistance < 30 and rightdistance < 30 and frontdistance < 30:
		#亮品红色，掉头
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.HIGH)
		spin_right(85, 85)
		time.sleep(0.58)
	elif leftdistance >= 30:
		#亮蓝色
		GPIO.output(LED_R, GPIO.LOW)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.HIGH)
		spin_left(15, 15)
		time.sleep(0.5)
		run(15,15)
		time.sleep(2)
		spin_right(55, 55)
		time.sleep(0.4)
		run(10,10)

		# if TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False:#若是左侧两个传感器接触到轨迹线时
		# 	spin_right(10, 10)#进行左转（短时间）调整运动方向，回归正常轨迹
		# 	time.sleep(0.10)
		return
	elif leftdistance <= rightdistance:
		#亮品红色，向右转
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.HIGH)
		spin_right(25,25)
		time.sleep(0.5)
		run(15,15)
		time.sleep(2)
		spin_left(40,40)
		time.sleep(0.4)
		run(10,10)
		# if TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False:#若是左侧两个传感器接触到轨迹线时
		# 	spin_right(10, 10)#进行左转（短时间）调整运动方向，回归正常轨迹
		# 	time.sleep(0.10)
		return
#延时2s	
time.sleep(2)

def tracking(runspeedRight,runspeedLeft,status):
	TrackSensorLeftValue1 = GPIO.input(TrackSensorLeftPin1)
	TrackSensorLeftValue2 = GPIO.input(TrackSensorLeftPin2)
	TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
	TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
	
	distance = Distance()
	po = True
	if 3 < distance < 30:
		k = 0
		for k in range(15):
			distance = Distance()
			if	distance > 35:
				po = False
		if po == True:
			#brake()
			print("stop!")
			servo_color_carstate()
			GPIO.output(LED_R, GPIO.HIGH)
			GPIO.output(LED_G, GPIO.LOW)
			GPIO.output(LED_B, GPIO.LOW)
			return
	GPIO.output(LED_R, GPIO.LOW)
	GPIO.output(LED_G, GPIO.HIGH)
	GPIO.output(LED_B, GPIO.LOW)
	#run(10,10)
	if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False:
		spin_right(30, 30)
		time.sleep(0.08)
		return 1
	elif TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or TrackSensorRightValue2 == False):
		spin_left(30, 30)
		time.sleep(0.08)
		return 2
	elif not TrackSensorLeftValue1:
		spin_left(20, 20)
		return 3
	elif not TrackSensorRightValue2:
		spin_right(20, 20)
		return 4
	elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
		left(0, 25)
		return 5
	elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
		right(25, 0)
		return 6
	elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
		run(runspeedLeft,runspeedRight)
		return 7
	elif TrackSensorLeftValue1 and TrackSensorLeftValue2 and TrackSensorRightValue1 and TrackSensorRightValue2:
		if status == 1:
			spin_right(30, 30)
			time.sleep(0.08)
		elif status == 2:
			spin_left(30, 30)
			time.sleep(0.08)
		elif status == 3:
			spin_left(20, 20)
		elif status == 4:
			spin_right(20, 20)
		elif status == 5:
			left(0, 25)
		elif status ==6:
			right(25, 0)
		elif status == 7:
			run(runspeedLeft,runspeedRight)
		return status
def servo_avoid():
	distance = Distance()
	if distance < 35:
		for _ in range(5):
			time.sleep(0.01)
			distance += Distance()
		if distance <= (35*6):
			servo_color_carstate()
		GPIO.output(LED_R, GPIO.HIGH)
		GPIO.output(LED_G, GPIO.LOW)
		GPIO.output(LED_B, GPIO.LOW)
	GPIO.output(LED_R, GPIO.LOW)
	GPIO.output(LED_G, GPIO.HIGH)
	GPIO.output(LED_B, GPIO.LOW)


