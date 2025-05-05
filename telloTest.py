import cv2 
import cvzone
import time
from djitellopy import tello
from gestures import HandGesture
#Define threshold for object id
thresh = 0.6
nmsThresh = 0.2

#Using SSD mobilenet weights trained on over 90 objects 
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().split('\n')

#Get config file
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'

#Get weight file
weightsPath = 'frozen_inference_graph.pb'

#Instantiate cv2 detection model 
net = cv2.dnn.DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
#Test cv2 video capture (webcam) 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4,720)

#Connect drone 
drone = tello.Tello()
drone.connect()
print("Battery {drone.get_battery()}%")
drone.streamoff()
drone.stream_on()
success, img = cap.read() #Testing video capture via webcam

#Send some commands
drone.takeoff()
drone.flip_back()
drone.flip_forward()
drone.move_left()
drone.move_right()

#Kill gracefully
drone.land()
drone.streamoff()
