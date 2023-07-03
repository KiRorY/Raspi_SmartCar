import os

def speak(sentence:str):
    os.system("python3 /home/pi/Desktop/yy/bin/zhspeak.py " + sentence)
