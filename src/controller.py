import subprocess
import time

class MediaController:
    def __init__(self, cooldown=1.0):
        """
        Initializes the controller with a debounce timer.
        :param cooldown: Seconds to wait before allowing another action.
        """
        self.cooldown = cooldown
        self.last_action_time = 0

    def _can_trigger(self):
        """
        Internal helper method to check the debounce timer.
        :return: Boolean (True if enough time has passed since last action).
        """
        curr_time = time.time()
        if (curr_time - self.last_action_time) > self.cooldown:
            self.last_action_time = curr_time
            return True
        return False

    def play_pause(self):
        """Simulates the Play/Pause media key."""
        if self._can_trigger():
            script = 'tell application "Spotify" to playpause'
            subprocess.run(['osascript', '-e', script])
        pass

    def skip_track(self):
        """Simulates the Next Track media key."""
        if self._can_trigger():
            script = f"tell application \"System Events\" to key code 98"
            subprocess.run(['osascript', '-e', script])
        pass

    def set_volume(self, level):
        """
        Sets the macOS system volume.
        :param level: Float or Int between 0 and 100.
        """
        clean_level = max(0, min(100, int(level)))
        
        script = f"set volume output volume {clean_level}"
        subprocess.Popen(['osascript', '-e', script], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)