import numpy as np
"""
Author: Divine Goshea 
Docs: Mediapipe
This python file contains the logic to define gestures using google's mediapipe hand tracking model 
- Takes frame from drone camera & classifies gesture every two seconds
- Identifies 21 points of intereset on hand 
"""
class GestureClassifier:
    def __init__(self):
        """
        Initializes landmark indices for fingertip and DIP joints for use in classification.
        """
        self.fingerTips = [4, 8, 12, 16, 20]
        self.fingerDips = [3, 7, 11, 15, 19]
        self.thumbTip = 4
        self.thumbDip = 3
    
    def fingerUp(self, lm, tipNum, dipNum):
        """
        Determines if a finger is up based on y-coordinates of the tip and dip.

        Args:
            lm: List of landmarks
            tipNum: Index of the fingertip
            dipNum: Index of the DIP joint

        Returns:
            True if finger is up, else False
        """
        return lm[tipNum].y < lm[dipNum].y
    
    def thumbOut(self, lm, tipNum, dipNum):
        """
        Helper to check if thumb is pointing outward.

        Returns:
            True if thumb is straight, else False
        """
        return lm[tipNum].y == lm[dipNum].y
    
    def classify(self, lm):
        """
        Classifies hand gesture from 21 landmarks.

        Params:
            lm: List of hand landmarks.

        Returns:
            String representing the detected gesture or "No gesture"
        """
        if lm is None or len(lm) != 21: #sorry if you have irregular hands
            return None
        
        fingers = []
        for tip, dip in zip(self.fingerTips, self.fingerDips):
            fingers.append(self.fingerUp(lm, tip, dip))

        #Map fingers to up or down to simplify gesture map
        thumb, index, middle, ring, pinky = fingers
       
        #Gestures 
        if all(fingers): #fingers = [t,t,t,t,t]
            return "open"
        elif not any(fingers): #fingers = [f,f,f,f,f]
            return "fist"
        elif thumb and not any(fingers[1:]):
            return "thumbsUp"
        elif index and not thumb and not ring and not middle and not pinky:
            return "one"
        elif index and middle and not ring and not pinky:
            return "peace"
        elif thumb and pinky and not ring and not index and not middle: 
            return "sahdude"
        elif thumb and middle and not ring and not pinky and not index:
            return "FU"
        elif index and middle and ring and pinky and not thumb:
            return "four"
        elif pinky and not thumb and not ring and not index:
            return "l"
        else: 
            return "No gesture"
