import mediapipe as mp
import numpy as np 
import cv2
from gestureClassifier import GestureClassifier

"""
Author: Divine Goshea 
Docs: Mediapipe
This python file contains the logic to detect a gesture using mediapipe's hand tracking model
"""
class HandGesture:
    def __init__(self, max_num_hands=1, detection_confidence = 0.7, tracking_confidence = 0.5):
        """
        Initializes Mediapipe Hand module and the gesture classifier.
        """
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils 
        self.classifier = GestureClassifier()

    def detect(self, image):
        """
        Processes the input image to detect hand landmarks.
        Classifies the detected hand gesture using the classifier.

        Params:
            image: A BGR image from OpenCV.

        Returns:
            Tuple: (processed image, detected gesture name or None)
        """
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        res = self.hands.process(imageRGB)
        gesture = None

        if res.multi_hand_landmarks:
            handLandmarks = res.multi_hand_landmarks[0]
            self.mpDraw.draw_landmarks(image, handLandmarks, mp.solutions.hands.HAND_CONNECTIONS)

            #Convert to list
            landmarks = handLandmarks.landmark
            gesture = self.classifier.classify(landmarks)

        return image, gesture
    

