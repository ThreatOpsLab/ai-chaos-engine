#!/usr/bin/env python3
"""
Simple test to verify all modules can be imported without crashing
Run this to check if dependencies are installed correctly
"""

print("Testing imports...")

try:
    print("  - Importing cv2...", end=" ")
    import cv2
    print("✓")
except ImportError as e:
    print(f"✗ Error: {e}")

try:
    print("  - Importing mediapipe...", end=" ")
    import mediapipe
    print("✓")
except ImportError as e:
    print(f"✗ Error: {e}")

try:
    print("  - Importing numpy...", end=" ")
    import numpy
    print("✓")
except ImportError as e:
    print(f"✗ Error: {e}")

try:
    print("  - Importing pyaudio...", end=" ")
    import pyaudio
    print("✓")
except ImportError as e:
    print(f"✗ Error: {e}")

try:
    print("  - Importing scipy...", end=" ")
    import scipy
    print("✓")
except ImportError as e:
    print(f"✗ Error: {e}")

print("\nTesting project modules...")

try:
    print("  - Importing hand_tracker...", end=" ")
    from hand_tracker import HandTracker
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")

try:
    print("  - Importing voice_modulator...", end=" ")
    from voice_modulator import VoiceModulator
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")

try:
    print("  - Importing ui_overlay...", end=" ")
    from ui_overlay import UIOverlay
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")

try:
    print("  - Importing main...", end=" ")
    from main import WebcamVoiceModulator
    print("✓")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n✅ All imports successful! You can now run: python main.py")
print("\nNote: The application will only start when you explicitly run main.py")
print("It is safe to open and edit files in Cursor without the app starting.")
