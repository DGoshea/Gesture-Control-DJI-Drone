# gesture_mapping.py

def map_gesture_to_command(gesture, confidence)
    # Direct mapping for most gestures
    command_map = {
        "takeoff": "takeoff",
        "land": "land",
        "left": "left",
        "right": "right",
        "forward": "forward",
        "backward": "backward",
        "up": "up",
        "down": "down",
      "hover": "hover"
    }

    return command_map.get(gesture)
