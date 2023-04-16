import cv2
import time
import keyboard
import mediapipe as mp

from hand_module import HandDetector
from directkeys import space_pressed
from directkeys import PressKey, ReleaseKey

# Define a callback function to handle the key press event
def on_space_pressed(event):
    if event.name == 'space':
        print('Space key pressed')

space_key_pressed = space_pressed
time.sleep(2.0)
current_key_pressed = set()

cap = cv2.VideoCapture(0)
handDetector = HandDetector()

while True:
    success, image = cap.read()

    if not success:
        break

    keyPressed = False
    spacePressed = False
    key_count = 0
    key_pressed = 0

    image = handDetector.find_hands(image)
    land_mark_list = handDetector.find_position(image, draw=False)
    fingers_up = handDetector.fingers_up()

    if fingers_up != None:
        max_fingers_up = fingers_up.count(1)
        cv2.putText(image, f'Fingers up: {str(max_fingers_up)}', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

    # print(fingers_up)
    # print(land_mark_list)
    keyboard.on_press_key('space', on_space_pressed)

    if fingers_up == [0,0,0,0,0]:
        PressKey(space_key_pressed)
        spacePressed = True
        current_key_pressed.add(space_key_pressed)
        key_pressed = space_key_pressed
        keyPressed = True
        key_count += 1

    if not keyPressed and len(current_key_pressed) != 0:
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()
    elif key_count == 1 and len(current_key_pressed) == 2:
        for key in current_key_pressed:
            if key_pressed != key:
                ReleaseKey(key)
        current_key_pressed = set()
        for key in current_key_pressed:
            ReleaseKey(key)
        current_key_pressed = set()

    cv2.imshow('image', image)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
