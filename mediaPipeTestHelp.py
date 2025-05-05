import mediapipe as mp

# Finger tip landmark indexes in MediaPipe
FINGER_TIPS = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
THUMB_TIP = 4

def fingers_up(hand_landmarks):
    """
    Checks which fingers are up using MediaPipe landmarks.
    Returns a tuple: (list of 4 booleans for fingers, bool for thumb)
    """
    finger_states = []

    for tip_id in FINGER_TIPS:
        is_up = hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y
        finger_states.append(is_up)

    thumb_is_up = hand_landmarks.landmark[THUMB_TIP].x > hand_landmarks.landmark[THUMB_TIP - 2].x
    return finger_states, thumb_is_up

def detect_gesture(fingers, thumb):
    """
    Returns a string for the detected gesture.
    """
    if fingers.count(True) == 0 and not thumb:
        return "Fist"
    elif fingers.count(True) == 4 and thumb:
        return "Open Hand"
    elif fingers.count(True) == 4 and not thumb:
        return "Four"
    elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:
        return "Peace"
    elif not any(fingers) and thumb:
        return "Thumbs Up"
    elif not fingers[0] and not fingers[1] and not fingers[2] and fingers[3] and thumb:
        return "WAZZUUUUUUUP"
    elif not fingers[0] and not fingers[2] and not fingers[3] and thumb and fingers[1]:
        return "FU"
    else:
        return "No gesture"
