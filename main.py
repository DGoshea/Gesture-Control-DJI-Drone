# main.py - The program entry point
from drone_controller import DroneController
from gesture_detector import GestureDetector
from camera_manager import CameraManager
from feedback_system import FeedbackSystem
from gesture_mapping import map_gesture_to_command  # Import the mapping function

def main():
    # Initialize components
    camera = CameraManager()
    detector = GestureDetector()
    drone = DroneController()
    feedback = FeedbackSystem()
    
    # System setup
    #if not <setup logic> 
        print("Error initializing drone and camera")
        return
    
    # Calibration
    #Logic for calibrating hand size
    
    # Main processing loop
    try:
        while True:
            #How to process drone commands ??

            #Quit processing commands
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Shutdown drone, camera, and cv
        drone.land()
        camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
