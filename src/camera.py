import cv2
import sys

class Camera:
    def __init__(self, device_id=0, width=1920, height=1080):
        """
        Initialises the MacBook Camera.
        :param device_id: 0 is usually the built-in FaceTime HD camera.
        :param width: Horizontal resolution.
        :param height: Vertical resolution.
        """
        self.cap = cv2.VideoCapture(device_id)
        
        # Set hardware properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        if not self.cap.isOpened():
            print("Error: Could not open camera. Check privacy settings in System Settings.")
            sys.exit()

    def get_frame(self):
        """
        Captures a frame and applies necessary preprocessing.
        """
        success, frame = self.cap.read()
        if not success:
            return None
        
        # MIRROR EFFECT: Flip horizontally (1) 
        # Provides a more intuitive user experience
        frame = cv2.flip(frame, 1)
        
        return frame

    def release(self):
        """Properly closes the hardware resource."""
        self.cap.release()

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("Testing Camera Module... Press 'q' to stop.")
    my_cam = Camera()
    
    while True:
        img = my_cam.get_frame()
        if img is not None:
            cv2.imshow("Camera Test - Press Q to Quit", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    my_cam.release()
    cv2.destroyAllWindows()