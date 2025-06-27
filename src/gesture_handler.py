import time
from utils import send_media_play_pause

def draw_volume_bar(frame, volume):
    """Draw a vertical volume bar on the frame."""
    import cv2  # Local import to avoid circular dependency
    bar_x = frame.shape[1] - 60
    bar_top = 50
    bar_bottom = frame.shape[0] - 50
    bar_height = bar_bottom - bar_top
    filled = int(bar_height * (volume / 100))
    cv2.rectangle(frame, (bar_x, bar_top), (bar_x + 30, bar_bottom), (180, 180, 180), 2)
    cv2.rectangle(frame, (bar_x, bar_bottom - filled), (bar_x + 30, bar_bottom), (0, 255, 0), -1)
    cv2.putText(frame, f'{volume}%', (bar_x - 10, bar_top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

def handle_gestures(hand_pose_detector, hand_position, volume_controller, state):
    """
    Handle gesture-based actions for volume and media control.
    - Volume up/down with index finger and palm angle.
    - Mute/unmute with closed palm facing camera.
    - Play/pause with open palm facing camera.
    """
    angle, palm_normal_z = hand_pose_detector.get_palm_wrist_angle(hand_position)
    hand_closed = hand_pose_detector.is_hand_closed(hand_position)
    hand_open = hand_pose_detector.is_hand_open(hand_position)
    now = time.time()

    # Volume control
    if hand_pose_detector.is_index_finger_pointing_out(hand_position):
        if now - state['last_increase_time'] > state['cooldown']:
            if angle < 110:
                volume_controller.increase_volume()
                state['last_increase_time'] = now
            elif angle > 130:
                volume_controller.decrease_volume()
                state['last_increase_time'] = now
            state['mute_pause_toggled_this_entry'] = False

    # Mute/unmute logic
    if palm_normal_z < -0.98 and hand_closed and not state['mute_pause_toggled_this_entry']:
        if not volume_controller.is_muted():
            volume_controller.mute_volume()
        else:
            volume_controller.unmute_volume()
        state['mute_pause_toggled_this_entry'] = True

    # Play/Pause logic
    if palm_normal_z < -0.98 and hand_open and not state['mute_pause_toggled_this_entry']:
        send_media_play_pause()
        state['mute_pause_toggled_this_entry'] = True