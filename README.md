# Webcam Voice Modulator with Hand Tracking

A real-time voice modulator controlled by hand gestures detected through your webcam. Features an Anonymous-style voice effect to mask your voice.

## Features

- **Hand Tracking Controls**:
  - **Left Hand** (vertical position): Controls pitch (0.5x to 2.0x)
  - **Right Hand** (vertical position): Controls wet/dry mix (0% to 100%)

- **Voice Modulator Modes**:
  - **Anonymous**: Deep, robotic voice effect with bandpass filtering
  - **Pitch Shift**: Standard pitch shifting based on hand position
  - **Normal**: Bypass mode (no effect)

- **Real-time Visual Feedback**:
  - Hand landmark tracking overlay
  - Control bars showing current parameter values
  - On-screen menu for mode selection

## Requirements

- Python 3.7+
- Webcam
- Microphone and speakers/headphones
- Linux/macOS/Windows

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. On Linux, you may need to install PortAudio:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# Fedora
sudo dnf install portaudio-devel

# macOS (via Homebrew)
brew install portaudio
```

## Usage

Run the application:
```bash
python main.py
```

### Controls

- **Left Hand**: Raise or lower your left hand to control pitch
  - Higher = higher pitch (up to 2x)
  - Lower = lower pitch (down to 0.5x)

- **Right Hand**: Raise or lower your right hand to control wet/dry mix
  - Higher = more effect (100% wet)
  - Lower = less effect (0% wet, original voice)

- **Keyboard**:
  - `SPACE`: Cycle through voice modulator modes
  - `Q` or `ESC`: Quit application

## How It Works

1. **Hand Tracking**: Uses MediaPipe to detect and track hand positions in real-time
2. **Voice Processing**: Captures audio from your microphone and applies effects:
   - Pitch shifting using time-domain interpolation
   - Anonymous effect: pitch lowering + bandpass filtering + soft clipping
   - Wet/dry mixing for effect intensity control
3. **Real-time Output**: Processed audio is output to your speakers with minimal latency

## Project Structure

- `main.py`: Main application loop and integration
- `hand_tracker.py`: Hand detection and tracking using MediaPipe
- `voice_modulator.py`: Audio processing and voice effects
- `ui_overlay.py`: Visual UI elements and menu system
- `requirements.txt`: Python dependencies

## Tips

- Ensure good lighting for better hand tracking
- Keep your hands visible in the camera frame
- Use headphones to prevent audio feedback
- Start with low wet/dry mix to avoid overwhelming effects
- The Anonymous mode works best with clear speech

## Troubleshooting

### Cursor/IDE Issues

**Application crashes when opening files in Cursor:**
- This is now fixed! The app only initializes hardware when you explicitly run `python main.py`
- Files are safe to open and edit in Cursor without the app starting
- To test if everything is working: `python test_import.py`

**Testing without hardware:**
- Run `python demo_no_hardware.py` to test components without webcam/audio
- This is useful for development and testing in virtual environments

### Runtime Issues

**No audio output/input:**
- Check your system audio settings
- Ensure microphone permissions are granted
- The app will continue with video-only mode if audio fails

**Hand tracking not working:**
- Improve lighting conditions
- Ensure hands are clearly visible against a contrasting background
- Keep hands within camera frame

**Latency issues:**
- Reduce chunk size in voice_modulator.py (may increase CPU usage)
- Close other audio applications
- Use a better quality microphone/audio interface

## License

MIT License - Feel free to modify and distribute.

## Credits

- MediaPipe for hand tracking
- PyAudio for audio I/O
- OpenCV for video processing
