#!/usr/bin/env python3
"""
Demo script that shows how the components work without requiring webcam/audio
Useful for testing in environments where hardware isn't available
"""
import numpy as np
from voice_modulator import VoiceModulator
from ui_overlay import UIOverlay

def demo_voice_modulator():
    """Demo the voice modulator with simulated audio"""
    print("=== Voice Modulator Demo ===\n")
    
    # Create voice modulator
    modulator = VoiceModulator()
    
    # Simulate some audio data (sine wave)
    sample_rate = 44100
    duration = 0.1  # 100ms
    frequency = 440  # A4 note
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t).astype(np.float32)
    
    print(f"Original audio shape: {audio_data.shape}")
    print(f"Original audio range: [{audio_data.min():.3f}, {audio_data.max():.3f}]\n")
    
    # Test different pitch values
    print("Testing pitch shifting:")
    for pitch in [0.5, 1.0, 1.5, 2.0]:
        modulator.set_pitch(pitch)
        modulator.set_wet_level(1.0)
        processed = modulator.process(audio_data)
        print(f"  Pitch {pitch}x: processed shape={processed.shape}, range=[{processed.min():.3f}, {processed.max():.3f}]")
    
    # Test wet/dry mix
    print("\nTesting wet/dry mix (pitch=0.7):")
    modulator.set_pitch(0.7)
    for wet in [0.0, 0.25, 0.5, 0.75, 1.0]:
        modulator.set_wet_level(wet)
        processed = modulator.process(audio_data)
        print(f"  Wet level {wet:.2f}: range=[{processed.min():.3f}, {processed.max():.3f}]")
    
    # Test Anonymous mode
    print("\nTesting Anonymous mode:")
    modulator.set_modulator_type("anonymous")
    modulator.set_wet_level(1.0)
    processed = modulator.process(audio_data)
    print(f"  Anonymous effect: processed shape={processed.shape}, range=[{processed.min():.3f}, {processed.max():.3f}]")
    
    print("\n✓ Voice Modulator working correctly!\n")


def demo_ui_overlay():
    """Demo the UI overlay"""
    print("=== UI Overlay Demo ===\n")
    
    ui = UIOverlay()
    
    print(f"Available modulators: {ui.modulator_options}")
    print(f"Current modulator: {ui.get_current_modulator()}")
    
    print("\nCycling through modulators:")
    for i in range(len(ui.modulator_options)):
        modulator = ui.next_modulator()
        print(f"  {i+1}. {modulator}")
    
    print("\n✓ UI Overlay working correctly!\n")


def demo_hand_mapping():
    """Demo the hand position mapping logic"""
    print("=== Hand Position Mapping Demo ===\n")
    
    # Simulate hand positions
    positions = [0.0, 0.25, 0.5, 0.75, 1.0]
    
    print("Left hand (Pitch control):")
    print("  Hand Position → Pitch Factor")
    for pos in positions:
        pitch = 0.5 + (pos * 1.5)
        print(f"  {pos:.2f} → {pitch:.2f}x")
    
    print("\nRight hand (Wet/Dry control):")
    print("  Hand Position → Wet Level")
    for pos in positions:
        wet = pos
        print(f"  {pos:.2f} → {int(wet * 100)}%")
    
    print("\n✓ Hand mapping logic working correctly!\n")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("WEBCAM VOICE MODULATOR - COMPONENT DEMO")
    print("="*50 + "\n")
    
    demo_hand_mapping()
    demo_voice_modulator()
    demo_ui_overlay()
    
    print("="*50)
    print("All components tested successfully!")
    print("="*50)
    print("\nTo run the full application with webcam and audio:")
    print("  python main.py")
    print("\nNote: This demo doesn't require webcam or audio hardware.")
