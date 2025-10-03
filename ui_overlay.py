"""
UI overlay for displaying controls and menu
"""
import cv2
import numpy as np


class UIOverlay:
    def __init__(self):
        self.modulator_options = ["anonymous", "pitch_shift", "normal"]
        self.current_modulator_index = 0
        
    def draw_control_bars(self, frame, left_hand_pos, right_hand_pos, pitch_value, wet_value):
        """
        Draw control bars showing hand positions and current values
        """
        height, width = frame.shape[:2]
        
        # Draw semi-transparent background for controls
        overlay = frame.copy()
        
        # Left side - Pitch control
        bar_width = 40
        bar_height = 300
        bar_x_left = 50
        bar_y = height - bar_height - 50
        
        # Draw pitch bar background
        cv2.rectangle(overlay, (bar_x_left, bar_y), 
                     (bar_x_left + bar_width, bar_y + bar_height), 
                     (50, 50, 50), -1)
        
        # Draw pitch fill
        if left_hand_pos is not None:
            fill_height = int(bar_height * left_hand_pos)
            cv2.rectangle(overlay, 
                         (bar_x_left, bar_y + bar_height - fill_height), 
                         (bar_x_left + bar_width, bar_y + bar_height), 
                         (0, 255, 100), -1)
        
        # Draw pitch border
        cv2.rectangle(overlay, (bar_x_left, bar_y), 
                     (bar_x_left + bar_width, bar_y + bar_height), 
                     (255, 255, 255), 2)
        
        # Pitch label
        cv2.putText(overlay, "PITCH", (bar_x_left - 10, bar_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(overlay, f"{pitch_value:.2f}x", (bar_x_left - 10, bar_y + bar_height + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Right side - Wet/Dry control
        bar_x_right = width - bar_x_left - bar_width
        
        # Draw wet bar background
        cv2.rectangle(overlay, (bar_x_right, bar_y), 
                     (bar_x_right + bar_width, bar_y + bar_height), 
                     (50, 50, 50), -1)
        
        # Draw wet fill
        if right_hand_pos is not None:
            fill_height = int(bar_height * right_hand_pos)
            cv2.rectangle(overlay, 
                         (bar_x_right, bar_y + bar_height - fill_height), 
                         (bar_x_right + bar_width, bar_y + bar_height), 
                         (255, 100, 0), -1)
        
        # Draw wet border
        cv2.rectangle(overlay, (bar_x_right, bar_y), 
                     (bar_x_right + bar_width, bar_y + bar_height), 
                     (255, 255, 255), 2)
        
        # Wet label
        cv2.putText(overlay, "WET/DRY", (bar_x_right - 20, bar_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(overlay, f"{int(wet_value * 100)}%", (bar_x_right, bar_y + bar_height + 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Blend overlay with original frame
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        return frame
    
    def draw_menu(self, frame, current_modulator):
        """
        Draw modulator selection menu
        """
        height, width = frame.shape[:2]
        
        # Menu background
        menu_height = 150
        menu_width = 400
        menu_x = (width - menu_width) // 2
        menu_y = 30
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (menu_x, menu_y), 
                     (menu_x + menu_width, menu_y + menu_height), 
                     (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Border
        cv2.rectangle(frame, (menu_x, menu_y), 
                     (menu_x + menu_width, menu_y + menu_height), 
                     (255, 255, 255), 2)
        
        # Title
        cv2.putText(frame, "VOICE MODULATOR", (menu_x + 70, menu_y + 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Options
        y_offset = menu_y + 70
        for i, option in enumerate(self.modulator_options):
            color = (0, 255, 0) if option == current_modulator else (200, 200, 200)
            prefix = "▶ " if option == current_modulator else "  "
            text = f"{prefix}{option.upper().replace('_', ' ')}"
            cv2.putText(frame, text, (menu_x + 30, y_offset + i * 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Instructions
        instructions = "Press SPACE to change mode | Q to quit"
        cv2.putText(frame, instructions, (menu_x + 20, menu_y + menu_height - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
        
        return frame
    
    def next_modulator(self):
        """Cycle to next modulator option"""
        self.current_modulator_index = (self.current_modulator_index + 1) % len(self.modulator_options)
        return self.modulator_options[self.current_modulator_index]
    
    def get_current_modulator(self):
        """Get current modulator type"""
        return self.modulator_options[self.current_modulator_index]
