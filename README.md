# Volume Controller (Headless)

This project is a **background hand-gesture controller** for Windows (and potentially Android) that uses your webcam to detect hand poses and control system volume and media playback **without any visible UI**.

## Features

- **Increase/Decrease Volume:** Point your index finger and tilt your palm up/down.
- **Mute/Unmute:** Show a closed palm facing the webcam to toggle mute.
- **Play/Pause Media:** Show an open palm facing the webcam to toggle play/pause.
- **Runs in the background:** No window or UI is shown; works silently.

## Use Cases

- Touchless volume and media control for presentations, music, or video playback.
- Accessibility: Control your computer without touching keyboard/mouse.
- Smart home or kiosk environments.

## Project Structure

```
volume-controller
├── src
│   ├── main.py            # Entry point (headless)
│   ├── camera.py          # Webcam capture
│   ├── hand_pose.py       # Hand pose detection
│   ├── volume_control.py  # System volume control
│   ├── gesture_handler.py # Gesture logic
│   └── utils.py           # Utility functions
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd volume-controller
   ```

2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```
   python src/main.py
   ```

   The app will run in the background, using your webcam for gesture control.

## Notes

- **Windows only:** Volume and media control uses Windows APIs (`pycaw`, `keyboard`). For Android, significant adaptation is needed (see below).
- **No UI:** There is no window or display; all actions are performed in the background.
- **Webcam required:** Ensure your webcam is connected and accessible.

## Android Support

- Direct Android support is not included. To run on Android, you would need to port the logic using [Kivy](https://kivy.org/) or [Chaquopy](https://chaquo.com/chaquopy/) and adapt camera and system control APIs for Android.

## Troubleshooting

- If the app does not control volume or media, ensure you have the required permissions and that your webcam is working.
- Some media players may not respond to the play/pause key sent by the app.

## License

MIT License