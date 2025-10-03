"""
Voice modulator with pitch shifting and wet/dry mix
Includes Anonymous-style voice effect
"""
import numpy as np
from scipy import signal
import pyaudio


class VoiceModulator:
    def __init__(self, sample_rate=44100, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.pitch_shift_factor = 1.0  # 1.0 = no change
        self.wet_level = 0.5  # 0.0 = dry, 1.0 = fully wet
        self.modulator_type = "anonymous"  # Default modulator type
        
        # Audio buffer for pitch shifting
        self.buffer = np.zeros(chunk_size * 4, dtype=np.float32)
        
    def set_pitch(self, pitch_factor):
        """
        Set pitch shift factor
        pitch_factor: 0.5 to 2.0 (0.5 = one octave down, 2.0 = one octave up)
        """
        self.pitch_shift_factor = np.clip(pitch_factor, 0.5, 2.0)
        
    def set_wet_level(self, wet):
        """
        Set wet/dry mix
        wet: 0.0 to 1.0
        """
        self.wet_level = np.clip(wet, 0.0, 1.0)
        
    def set_modulator_type(self, mod_type):
        """Set the type of voice modulator"""
        self.modulator_type = mod_type
        
    def pitch_shift(self, audio_data):
        """
        Simple pitch shifting using time stretching and resampling
        """
        if abs(self.pitch_shift_factor - 1.0) < 0.01:
            return audio_data
            
        # Simple pitch shifting using linear interpolation
        indices = np.arange(0, len(audio_data), self.pitch_shift_factor)
        indices = indices[indices < len(audio_data)].astype(np.float32)
        
        # Linear interpolation
        int_indices = indices.astype(np.int32)
        frac = indices - int_indices
        
        int_indices = np.clip(int_indices, 0, len(audio_data) - 2)
        
        shifted = (audio_data[int_indices] * (1 - frac) + 
                  audio_data[int_indices + 1] * frac)
        
        # Resize to original length
        if len(shifted) < len(audio_data):
            shifted = np.pad(shifted, (0, len(audio_data) - len(shifted)))
        else:
            shifted = shifted[:len(audio_data)]
            
        return shifted
    
    def anonymous_effect(self, audio_data):
        """
        Apply Anonymous-style voice effect
        - Lower pitch (deeper voice)
        - Add slight robotic/vocoder quality
        - Add formant shifting
        """
        # Lower the pitch significantly
        pitch_factor = 0.7  # Deeper voice
        
        # Apply pitch shift
        shifted = self.pitch_shift(audio_data)
        
        # Add slight distortion for robotic quality
        # Soft clipping
        shifted = np.tanh(shifted * 1.5)
        
        # Apply a bandpass filter for telephone-like quality
        # Design a bandpass filter (300Hz - 3000Hz)
        nyquist = self.sample_rate / 2
        low = 300 / nyquist
        high = 3000 / nyquist
        
        # Create filter
        b, a = signal.butter(4, [low, high], btype='band')
        filtered = signal.lfilter(b, a, shifted)
        
        return filtered.astype(np.float32)
    
    def process(self, audio_data):
        """
        Process audio data with current settings
        audio_data: numpy array of audio samples (float32, -1 to 1)
        """
        if self.modulator_type == "anonymous":
            # Use Anonymous effect which has its own pitch control
            processed = self.anonymous_effect(audio_data)
        else:
            # Standard pitch shifting
            processed = self.pitch_shift(audio_data)
        
        # Mix wet and dry signals
        output = (1.0 - self.wet_level) * audio_data + self.wet_level * processed
        
        return output.astype(np.float32)
