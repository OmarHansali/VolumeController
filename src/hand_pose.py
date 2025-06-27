import cv2
import mediapipe as mp
import math

class HandPoseDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.results = None

    def detect_hand(self, frame):
        # Convert the frame to RGB and process with MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)
        if self.results.multi_hand_landmarks:
            return self.results.multi_hand_landmarks[0]  # Return the first detected hand
        return None

    def is_hand_closed(self, hand_landmarks):
        # Check if the tips of the fingers are below their respective MCP joints (except thumb)
        # Landmarks: 8 - index tip, 12 - middle tip, 16 - ring tip, 20 - pinky tip
        # MCP joints: 5 - index, 9 - middle, 13 - ring, 17 - pinky
        closed = True
        finger_tips = [8, 12, 16, 20]
        finger_mcp = [5, 9, 13, 17]
        for tip, mcp in zip(finger_tips, finger_mcp):
            if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y:
                closed = False
        return closed

    def is_index_finger_pointing_out(self, hand_landmarks):
        # Helper to calculate Euclidean distance
        def distance(a, b):
            return math.hypot(a.x - b.x, a.y - b.y)

        wrist = hand_landmarks.landmark[0]
        index_tip = hand_landmarks.landmark[8]
        index_pip = hand_landmarks.landmark[6]
        index_dip = hand_landmarks.landmark[7]

        # Index finger is extended if tip is farther from wrist than pip and dip
        index_tip_dist = distance(index_tip, wrist)
        index_pip_dist = distance(index_pip, wrist)
        index_dip_dist = distance(index_dip, wrist)
        index_extended = index_tip_dist > index_pip_dist and index_tip_dist > index_dip_dist

        # Other fingers are not extended (tip not farther from wrist than pip)
        other_fingers = [
            (12, 10),  # middle tip, middle pip
            (16, 14),  # ring tip, ring pip
            (20, 18)   # pinky tip, pinky pip
        ]
        others_folded = all(
            distance(hand_landmarks.landmark[tip], wrist) < distance(hand_landmarks.landmark[pip], wrist)
            for tip, pip in other_fingers
        )

        return index_extended and others_folded
    
    def get_palm_wrist_angle(self, hand_landmarks):
        wrist = hand_landmarks.landmark[0]
        index_mcp = hand_landmarks.landmark[5]
        pinky_mcp = hand_landmarks.landmark[17]

        v1 = [
            index_mcp.x - wrist.x,
            index_mcp.y - wrist.y,
            index_mcp.z - wrist.z
        ]
        v2 = [
            pinky_mcp.x - wrist.x,
            pinky_mcp.y - wrist.y,
            pinky_mcp.z - wrist.z
        ]

        # Palm normal (cross product)
        normal = [
            v1[1]*v2[2] - v1[2]*v2[1],
            v1[2]*v2[0] - v1[0]*v2[2],
            v1[0]*v2[1] - v1[1]*v2[0]
        ]

        # Normalize normal
        norm = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if norm == 0:
            return 0, 0
        normal = [n / norm for n in normal]

        # Reference vector for "up" in image coordinates (y axis negative is up)
        up = [0, -1, 0]

        # Angle between normal and up
        dot = sum([normal[i]*up[i] for i in range(3)])
        angle = math.acos(max(min(dot, 1.0), -1.0)) * 180 / math.pi
        return angle, normal[2]  # Return angle and palm normal z
    
    def is_hand_open(self, hand_landmarks):
        # All fingers are straight if tip is above pip for each finger (except thumb)
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]
        for tip, pip in zip(finger_tips, finger_pips):
            if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
                return False
        return True
    
    # def get_hand_origin(self, hand_landmarks):
    #     # Return the (x, y) position of the wrist (landmark 0)
    #     wrist = hand_landmarks.landmark[0]
    #     return (wrist.x, wrist.y)

    # def get_index_finger_position(self, hand_landmarks):
    #     # Return the (x, y) position of the index finger tip (landmark 8)
    #     index_tip = hand_landmarks.landmark[8]
    #     return (index_tip.x, index_tip.y)

    # def is_index_finger_moving_up(self, initial_position, current_position, threshold=0.02):
    #     # Compare y-coordinates (smaller y means higher in image)
    #     return current_position[1] - initial_position[1] < -threshold
    
    # def get_wrist_y(self, hand_landmarks):
    #     # Return the y position of the wrist (landmark 0)
    #     return hand_landmarks.landmark[0].y

    # def get_middle_mcp_y(self, hand_landmarks):
    #     # Return the y position of the middle finger MCP (landmark 9)
    #     return hand_landmarks.landmark[9].y