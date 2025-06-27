import keyboard

def send_media_play_pause():
    """Send the media play/pause key event to the OS."""
    keyboard.send("play/pause media")

# def calculate_index_finger_position(hand_landmarks):
#     # Assuming hand_landmarks is a list of tuples representing the (x, y) positions of hand landmarks
#     # The index finger tip is typically the 8th landmark in a 21 landmark model
#     index_finger_tip = hand_landmarks[8]
#     return index_finger_tip

# def is_hand_closed(hand_landmarks):
#     # Assuming hand_landmarks is a list of tuples representing the (x, y) positions of hand landmarks
#     # Check if the distance between the thumb and the index finger is small enough to consider the hand closed
#     thumb_tip = hand_landmarks[4]
#     index_finger_base = hand_landmarks[6]
    
#     distance = ((thumb_tip[0] - index_finger_base[0]) ** 2 + (thumb_tip[1] - index_finger_base[1]) ** 2) ** 0.5
#     return distance < 50  # Threshold distance to determine if hand is closed

# def normalize_value(value, min_value, max_value):
#     # Normalize a value to a range between 0 and 1
#     return (value - min_value) / (max_value - min_value) if max_value > min_value else 0

# def map_value(value, from_min, from_max, to_min, to_max):
#     # Map a value from one range to another
#     normalized_value = normalize_value(value, from_min, from_max)
#     return to_min + (to_max - to_min) * normalized_value