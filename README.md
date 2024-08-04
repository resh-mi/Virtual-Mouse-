# Virtual-Mouse-
The code provided is a Python script that implements a virtual mouse using hand gestures detected by a webcam. It uses the MediaPipe library to track hand movements and PyAutoGUI to simulate mouse actions.

## Features
- **Mouse Movement**: Control the mouse pointer using your index finger tip.
- **Zooming**: Zoom in and out by pinching (changing the distance between your thumb and index finger).
- **Scrolling**: Scroll up and down based on vertical hand movements.
- **Clicking**: Simulate a mouse click when the index and middle finger tips are close together.
- **Sensitivity Adjustment**: Adjust the sensitivity of mouse movements using keyboard shortcuts.

## Prerequisites
- Python 3.x
- OpenCV
- MediaPipe
- PyAutoGUI
- Tkinter (usually included with Python)

## Installation
1. Install the required packages using pip:

   ```bash
   pip install opencv-python mediapipe pyautogui
Usage
Run the script:

bash
Copy code
python prac.py
GUI Interface:

Click "Start Gesture Control" to begin gesture detection.
Click "Stop Gesture Control" to end the session.
Gesture Controls:

Move your hand to control the mouse pointer.
Pinch (thumb and index finger) to zoom in or out.
Move your hand up or down to scroll.
Tap (index and middle fingers together) to click.
Keyboard Controls:

Press q to quit the application.
Press z to increase mouse sensitivity.
Press x to decrease mouse sensitivity.
Important Notes
Ensure your webcam is properly connected and functional.
Adjust the sensitivity scale for mouse movement if needed for more responsive control.
Example Output
The program will open a window displaying the webcam feed with hand landmarks drawn. It will track gestures in real time and move the mouse accordingly.

Troubleshooting
If gestures are not detected correctly, try adjusting the lighting conditions and ensure your hand is clearly visible to the camera.
Make sure all dependencies are correctly installed and import paths are set.
Sample Code
Here is a snippet of the main loop handling gesture detection and control:

python
Copy code
while running:
    ret, frame = cap.read()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Logic for gesture detection and mouse control
            ...
