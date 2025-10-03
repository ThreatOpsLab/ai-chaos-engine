"""
Hand tracking module using MediaPipe
Detects left and right hands and extracts their positions
"""
import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def process_frame(self, frame):
        """
        Process a frame and detect hands
        Returns: dict with 'left' and 'right' hand positions (normalized 0-1)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        hand_positions = {'left': None, 'right': None}
        
        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Get hand label (Left or Right)
                hand_label = handedness.classification[0].label
                
                # Get the y-position of the wrist (index 0)
                # We'll use the average y-position of all landmarks for smoother control
                y_positions = [landmark.y for landmark in hand_landmarks.landmark]
                avg_y = sum(y_positions) / len(y_positions)
                
                # Store normalized position (0 = top, 1 = bottom)
                # We'll invert it so that raising hand increases the value
                normalized_position = 1.0 - avg_y
                
                if hand_label == 'Left':
                    hand_positions['left'] = normalized_position
                else:
                    hand_positions['right'] = normalized_position
                    
        return hand_positions, results
    
    def draw_hands(self, frame, results):
        """Draw hand landmarks on the frame"""
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        return frame
    
    def release(self):
        """Release resources"""
        self.hands.close()
