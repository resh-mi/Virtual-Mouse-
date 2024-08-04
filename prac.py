import cv2
import mediapipe as mp
import pyautogui
import math
import threading
import tkinter as tk
from tkinter import ttk

# Initialize MediaPipe Hand model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Get the screen size
screen_width, screen_height = pyautogui.size()

# Initialize video capture
cap = cv2.VideoCapture(0)

# Variables to keep track of previous state for zooming and scrolling
prev_thumb_index_dist = 0
prev_y = 0
scrolling_mode = False

# Thresholds (initial values)
zoom_threshold = 0.03  # Threshold for zooming gesture
scroll_threshold = 30  # Threshold for scrolling gesture
click_distance_threshold = 0.03  # Threshold for click gesture

# Sensitivity scaling factor for mouse movement
sensitivity_scale = 0.5  # Adjust this value as needed

# Flag to control the main loop
running = False

def calculate_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    """
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def detect_zoom(thumb_tip, index_finger_tip, prev_thumb_index_dist):
    """
    Detect zooming based on the change in distance between the thumb and index finger tips.
    """
    thumb_index_dist = calculate_distance(thumb_tip, index_finger_tip)
    zoom_in = thumb_index_dist > prev_thumb_index_dist + zoom_threshold
    zoom_out = thumb_index_dist < prev_thumb_index_dist - zoom_threshold
    return zoom_in, zoom_out, thumb_index_dist

def detect_scroll(y, prev_y):
    """
    Detect scrolling based on the vertical movement of the hand.
    """
    scroll_amount = prev_y - y
    if abs(scroll_amount) > scroll_threshold:
        return int(scroll_amount / scroll_threshold)
    else:
        return 0

def gesture_control():
    global prev_thumb_index_dist, prev_y, scrolling_mode, zoom_threshold, click_distance_threshold, sensitivity_scale, running

    while running:
        # Read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a natural interaction
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        result = hands.process(rgb_frame)

        # Check if any hand is detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Extract the coordinates of the relevant landmarks
                index_finger_tip = hand_landmarks.landmark[8]
                thumb_tip = hand_landmarks.landmark[4]
                index_base = hand_landmarks.landmark[5]
                middle_finger_tip = hand_landmarks.landmark[12]

                # Calculate the distance between thumb and index finger tips
                thumb_index_dist = calculate_distance(thumb_tip, index_finger_tip)

                # Convert the normalized coordinates to pixel coordinates with sensitivity scaling
                x = int(index_finger_tip.x * frame.shape[1])
                y = int(index_finger_tip.y * frame.shape[0])
                screen_x = screen_width * (x / frame.shape[1]) * sensitivity_scale
                screen_y = screen_height * (y / frame.shape[0]) * sensitivity_scale

                # Move the mouse
                pyautogui.moveTo(screen_x, screen_y)

                # Detect zoom gesture
                zoom_in, zoom_out, thumb_index_dist = detect_zoom(thumb_tip, index_finger_tip, prev_thumb_index_dist)
                if not scrolling_mode:
                    if zoom_in:
                        pyautogui.hotkey('ctrl', '+')  # Zoom in
                    elif zoom_out:
                        pyautogui.hotkey('ctrl', '-')  # Zoom out
                prev_thumb_index_dist = thumb_index_dist

                # Detect scroll gesture
                hand_position_y = index_finger_tip.y * screen_height
                scroll_amount = detect_scroll(hand_position_y, prev_y)
                if scrolling_mode and scroll_amount != 0:
                    pyautogui.scroll(scroll_amount)

                # Toggle scrolling mode based on thumb position
                if thumb_tip.x < index_base.x:
                    scrolling_mode = True
                else:
                    scrolling_mode = False

                # Update previous y coordinate
                prev_y = hand_position_y

                # Check for click gesture based on finger proximity
                index_middle_distance = calculate_distance(index_finger_tip, middle_finger_tip)
                if index_middle_distance < click_distance_threshold:
                    pyautogui.click()  # Perform a mouse click action

                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the frame
        cv2.imshow('Virtual Mouse', frame)

        # Check for keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            running = False
            break
        elif key == ord('z'):
            sensitivity_scale += 0.1  # Increase sensitivity
        elif key == ord('x'):
            sensitivity_scale -= 0.1  # Decrease sensitivity

    # Release the video capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

def start_gesture_control():
    global running
    running = True
    gesture_thread = threading.Thread(target=gesture_control)
    gesture_thread.start()

def stop_gesture_control():
    global running
    running = False

def create_gui():
    root = tk.Tk()
    root.title("Gesture Control Interface")

    start_button = ttk.Button(root, text="Start Gesture Control", command=start_gesture_control)
    start_button.pack(pady=10)

    stop_button = ttk.Button(root, text="Stop Gesture Control", command=stop_gesture_control)
    stop_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
