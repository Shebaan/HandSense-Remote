import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        """
        Initialises the MediaPipe Hand tracking model.
        :param mode: If True, it treats every frame as a new detection (slower).
        :param max_hands: Number of hands to track.
        :param detection_con: Initial detection sensitivity (0.0 - 1.0).
        :param track_con: Tracking sensitivity (keeps the "lock" on your hand).
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            model_complexity=1,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        # Utility to draw the points on the screen for debugging
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        """Processes the image and finds landmarks."""
        # MediaPipe requires RGB images, but OpenCV captures in BGR.
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def get_position(self, img):
        """Extracts the (x, y) coordinates of all 21 landmarks."""
        lm_list = []
        if self.results.multi_hand_landmarks:
            # We are only tracking one hand (index 0)
            my_hand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(my_hand.landmark):
                # Convert normalized coordinates (0.0 - 1.0) to Pixel Coordinates
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append({"id": id, "x": cx, "y": cy})
        return lm_list