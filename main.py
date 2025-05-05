"""
Main Drone Control Script using Hand Gestures
Author: Divine Goshea

This script connects to a Tello drone, starts a video stream, and uses OpenCV 
with a gesture recognition model (Mediapipe + custom classifier) to detect hand gestures 
from the camera feed. Based on the detected gesture, the drone executes commands such as takeoff, 
land, flips, and directional movements.

Gestures recognized: open, peace, FU, l, thumbsUp, one, sahdude, four, fist
"""
import cv2 
import time
import threading
from djitellopy import tello
from gestures import HandGesture

frame = None

#Capture frames without disturbing the loop
def capFrame():
    global frame
    while True:
        frame = drone.get_frame_read().frame
        time.sleep(.03)

#Start the thread 
frameThread = threading.Thread(target=capFrame)
frameThread.daemon = True
frameThread.start()

#Vars for timing 
lastGesture = None
lastCommandTime = time.time()
fps = 0
frameCount = 0
start = time.time()

#Initialize tello drone  
drone = tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")
drone.streamon()

#Init gesture 
gesture_detector = HandGesture()

#Main loop 
while True:
    frame = drone.get_frame_read().frame
    if frame is None:
        continue

    rframe = cv2.resize(frame, (640,480))
    processedFrame, gesture = gesture_detector.detect(rframe)
    
    #Send commands every 5 seconds 
    if gesture and gesture != lastGesture and time.time() - lastCommandTime > 5:
        print(f"Detected gesture: {gesture}")
        if gesture == "open":
            drone.takeoff()
        elif gesture == "peace":
            drone.flip_forward()
        elif gesture == "FU":
            drone.flip_back()
        elif gesture == "l":
            drone.move_left(50)
        elif gesture == "thumbsUp":
            drone.move_right(50)
        elif gesture == "one":
            drone.move_up(50)
        elif gesture == "sahdude":
            drone.move_forward(20)
        elif gesture == "four":
            drone.move_down(20)
        elif gesture == "fist":
            #Graceful Termination 
            cv2.putText(processedFrame, f"Land Gesture Detected! Landing and terminating...", (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            print(f"Drone Battery: {drone.get_battery()}%")
            drone.land()
            drone.streamoff()
            cv2.destroyAllWindows()
        elif gesture == "No gesture":
            print(f" Drone Height: {drone.get_height()}")
            continue
        else: 
            continue

        lastGesture = gesture
        lastCommandTime = time.time()
    
    #Draw gesture text only if there is gesture 
    if gesture:
        cv2.putText(processedFrame, f"Gesture: {gesture}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #Calculate fps
    frameCount +=1 
    if time.time() - start > 1:
        fps = frameCount
        frameCount = 0
        start = time.time()
    
    #Display fps and frame
    cv2.putText(processedFrame, f"FPS: {fps}", (10,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.imshow("Drone Gesture Control Frame", processedFrame)

    #Exit control via interrupt 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Error detected 
print("Error Detected! Triggered Emergency Landing")
drone.land()
drone.streamoff()
cv2.destroyAllWindows()