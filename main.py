#!/usr/bin/env python3
"""
Webcam Voice Modulator with Hand Tracking
- Left hand controls pitch
- Right hand controls wet/dry mix
- Space bar to change voice modulator type
"""
import cv2
import numpy as np
import pyaudio
import threading
import queue
import sys

from hand_tracker import HandTracker
from voice_modulator import VoiceModulator
from ui_overlay import UIOverlay


class WebcamVoiceModulator:
    def __init__(self):
        # Initialize basic settings (don't create objects yet)
        self.sample_rate = 44100
        self.chunk_size = 1024
        
        # Control values
        self.pitch_value = 1.0
        self.wet_value = 0.5
        
        # Thread control
        self.running = False
        self.audio_thread = None
        
        # Components (initialized later)
        self.hand_tracker = None
        self.voice_modulator = None
        self.ui_overlay = None
        self.audio = None
        self.stream = None
        self.cap = None
        
    def map_hand_to_pitch(self, hand_pos):
        """
        Map left hand position to pitch value
        hand_pos: 0.0 (bottom) to 1.0 (top)
        Returns: pitch factor 0.5 to 2.0
        """
        if hand_pos is None:
            return self.pitch_value  # Keep current value
        # Map 0-1 to 0.5-2.0 (one octave down to one octave up)
        return 0.5 + (hand_pos * 1.5)
    
    def map_hand_to_wet(self, hand_pos):
        """
        Map right hand position to wet/dry mix
        hand_pos: 0.0 (bottom) to 1.0 (top)
        Returns: wet level 0.0 to 1.0
        """
        if hand_pos is None:
            return self.wet_value  # Keep current value
        return hand_pos
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """
        PyAudio callback for processing audio
        """
        # Convert bytes to numpy array
        audio_data = np.frombuffer(in_data, dtype=np.int16).astype(np.float32)
        audio_data = audio_data / 32768.0  # Normalize to -1.0 to 1.0
        
        # Process with voice modulator
        processed = self.voice_modulator.process(audio_data)
        
        # Convert back to int16
        output_data = (processed * 32768.0).astype(np.int16)
        
        return (output_data.tobytes(), pyaudio.paContinue)
    
    def start_audio(self):
        """Start audio stream"""
        try:
            # Open audio stream
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                output=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self.audio_callback
            )
            self.stream.start_stream()
            print("Audio stream started")
        except Exception as e:
            print(f"Error starting audio stream: {e}")
            print("Audio may not be available, continuing with video only...")
            self.stream = None
    
    def stop_audio(self):
        """Stop audio stream"""
        if hasattr(self, 'stream') and self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
    
    def run(self):
        """Main application loop"""
        try:
            # Initialize components
            print("Initializing components...")
            self.hand_tracker = HandTracker()
            self.voice_modulator = VoiceModulator(sample_rate=self.sample_rate, chunk_size=self.chunk_size)
            self.ui_overlay = UIOverlay()
            self.audio = pyaudio.PyAudio()
            print("Components initialized successfully")
            
            # Initialize camera
            print("Opening webcam...")
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open webcam")
                return
            print("Webcam opened successfully")
            
            # Start audio
            self.running = True
            self.start_audio()
            
            print("\nWebcam Voice Modulator Started")
            print("Controls:")
            print("  - Left hand (up/down): Control pitch")
            print("  - Right hand (up/down): Control wet/dry mix")
            print("  - SPACE: Change voice modulator type")
            print("  - Q or ESC: Quit\n")
            
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process hand tracking
                hand_positions, results = self.hand_tracker.process_frame(frame)
                
                # Update control values based on hand positions
                self.pitch_value = self.map_hand_to_pitch(hand_positions['left'])
                self.wet_value = self.map_hand_to_wet(hand_positions['right'])
                
                # Update voice modulator
                self.voice_modulator.set_pitch(self.pitch_value)
                self.voice_modulator.set_wet_level(self.wet_value)
                
                # Draw hand landmarks
                frame = self.hand_tracker.draw_hands(frame, results)
                
                # Draw UI overlays
                frame = self.ui_overlay.draw_control_bars(
                    frame, 
                    hand_positions['left'], 
                    hand_positions['right'],
                    self.pitch_value,
                    self.wet_value
                )
                
                frame = self.ui_overlay.draw_menu(
                    frame, 
                    self.ui_overlay.get_current_modulator()
                )
                
                # Display frame
                cv2.imshow('Webcam Voice Modulator', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # Q or ESC
                    break
                elif key == ord(' '):  # Space bar
                    new_modulator = self.ui_overlay.next_modulator()
                    self.voice_modulator.set_modulator_type(new_modulator)
                    print(f"Switched to {new_modulator} mode")
                    
        except Exception as e:
            print(f"Error during execution: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\nShutting down...")
        self.running = False
        
        # Stop audio
        self.stop_audio()
        
        # Release camera
        if self.cap is not None:
            self.cap.release()
        
        # Close windows
        cv2.destroyAllWindows()
        
        # Release hand tracker
        if self.hand_tracker is not None:
            self.hand_tracker.release()
        
        # Terminate audio
        if self.audio is not None:
            self.audio.terminate()
        
        print("Cleanup complete")


def main():
    app = WebcamVoiceModulator()
    app.run()


if __name__ == "__main__":
    main()
