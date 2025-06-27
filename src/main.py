import time
import mediapipe as mp

from camera import Camera
from hand_pose import HandPoseDetector
from volume_control import VolumeController
from gesture_handler import handle_gestures

def main():
    """Main application loop (headless, no UI)."""
    camera = Camera()
    hand_pose_detector = HandPoseDetector()
    volume_controller = VolumeController()
    mp_draw = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    camera.start_capture()

    state = {
        'last_increase_time': 0,
        'cooldown': 0.2,
        'mute_pause_toggled_this_entry': False,
        'hand_present': False
    }

    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                break

            hand_position = hand_pose_detector.detect_hand(frame)

            if hand_position is not None:
                if not state['hand_present']:
                    state['mute_pause_toggled_this_entry'] = False
                    state['hand_present'] = True
                    time.sleep(0.2)  # Allow time for hand detection stabilization

                # No drawing or UI
                handle_gestures(hand_pose_detector, hand_position, volume_controller, state)
            else:
                state['hand_present'] = False

            # Sleep a bit to reduce CPU usage
            time.sleep(0.01)
    finally:
        camera.release()

if __name__ == "__main__":
    main()