import math

class GestureProcessor:
    def __init__(self, pinch_threshold=30):
        """
        Initialize the processor with configurable thresholds.
        """
        self.pinch_threshold = pinch_threshold
        self.middle_pinch_threshold = pinch_threshold + 10 # Middle finger is usually a bit farther from the thumb

    def get_distance(self, p1, p2):
        """
        Calculates the Euclidean distance between two points.
        :param p1: Dictionary containing 'x' and 'y' of point 1.
        :param p2: Dictionary containing 'x' and 'y' of point 2.
        :return: Float representing the pixel distance.
        """
        distance = math.sqrt((p2['x'] - p1['x']) ** 2 + (p2['y'] - p1['y']) ** 2)

        return distance

    def is_pinching(self, lm_list, target_finger_id=8, threshold=None):
        """
        Determines if the thumb (4) and a specific finger tip are pinched.
        :param lm_list: The full list of 21 landmarks.
        :param target_finger_id: The ID of the finger tip to check (8=Index, 12=Middle).
        :param threshold: Custom threshold for pinching detection.
        :return: Boolean (True if distance < threshold)
        """
        thumb_tip = lm_list[4]
        target_tip = lm_list[target_finger_id]

        curr_dist = self.get_distance(thumb_tip, target_tip)

        if threshold is not None:
            return curr_dist < threshold
        return curr_dist < self.pinch_threshold
    
    def index_pinched(self, lm_list):
        """
        Convenience method to check if the thumb and index finger are pinching.
        :param lm_list: The full list of 21 landmarks.
        :return: Boolean (True if thumb and index are pinching)
        """
        return self.is_pinching(lm_list, target_finger_id=8)
    
    def middle_pinched(self, lm_list):
        """
        Convenience method to check if the thumb and middle finger are pinching.
        :param lm_list: The full list of 21 landmarks.
        :return: Boolean (True if thumb and middle are pinching)
        """
        return self.is_pinching(lm_list, target_finger_id=12, threshold=self.middle_pinch_threshold)

    def get_fingers_up(self, lm_list):
        """
        Checks which of the 4 main fingers are extended.
        (Ignoring the thumb for now, as its geometry is sideways).
        :param lm_list: The full list of 21 landmarks.
        :return: A list of 4 integers/booleans (e.g., [1, 1, 0, 0] means Index & Middle are up).
        """
        fingers_status = []

        tip_ids = [8, 12, 16, 20] # Index, Middle, Ring, Pinky
        joint_ids = [6, 10, 14, 18] # The joint right before the tip for each finger

        for finger in range(4):
            curr_tip_id = tip_ids[finger]
            curr_joint_id = joint_ids[finger]
            if lm_list[curr_tip_id]['y'] < lm_list[curr_joint_id]['y']:
                fingers_status.append(1) # Finger is up
            else:
                fingers_status.append(0) # Finger is down
        
        return fingers_status
    
    def hand_open(self, lm_list):
        """
        Simple logic to determine if the hand is open (all fingers up).
        :param lm_list: The full list of 21 landmarks.
        :return: Boolean (True if all fingers are up)
        """
        fingers = self.get_fingers_up(lm_list)
        return sum(fingers) == 4