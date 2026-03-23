import cv2
import time
from camera import Camera
from detector import HandDetector
from processor import GestureProcessor
from controller import MediaController

def main():
    # Initialize our objects
    cam = Camera()
    detector = HandDetector()
    processor = GestureProcessor()
    media = MediaController()
    
    p_time = 0 # To calculate FPS
    previous_vol = -1 # To prevent redundant volume commands
    
    print("HandSense Engine Starting... Press 'q' to quit.")

    while True:
        # 1. Get Frame
        frame = cam.get_frame()
        if frame is None: break

        # 2. Detect Hands & Draw Landmarks
        frame = detector.find_hands(frame)
        lm_list = detector.get_position(frame)

        # 3. Simple Logic Test: If index finger (8) is detected, draw a circle on it
        if lm_list:
            index_finger = lm_list[8]
            cv2.circle(frame, (index_finger['x'], index_finger['y']), 15, (255, 0, 255), cv2.FILLED)

        if lm_list:
            # 1. Middle Pinch = Play/Pause
            if processor.middle_pinched(lm_list):
                cv2.putText(frame, "PLAY/PAUSE", (50, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                media.play_pause()

            # 2. Index Pinch = Volume
            elif processor.index_pinched(lm_list):
                y_coord = lm_list[8]['y'] 
                y_min, y_max = 200, 500
                
                if y_coord < y_min: y_coord = y_min
                if y_coord > y_max: y_coord = y_max
                
                range_y = y_max - y_min
                vol_percentage = 100 - (((y_coord - y_min) / range_y) * 100)
                
                # ONLY talk to the OS if the volume changed by more than 2%
                if abs(vol_percentage - previous_vol) > 2:
                    media.set_volume(vol_percentage)
                    previous_vol = vol_percentage # Update the state
                
                cv2.putText(frame, f"VOL: {int(vol_percentage)}%", (50, 150), 
                            cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 3)

        # 4. Calculate & Display FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        # 5. Show Window
        cv2.imshow("HandSense Remote v1.0", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()