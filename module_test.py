import cv2
import time
# import keyboard
# import sys
import subprocess
import mediapipe as mp

from hand_module import HandDetector
from directkeys import space_pressed
from directkeys import arrow_left_pressed, arrow_right_pressed
from directkeys import arrow_up_pressed, arrow_down_pressed
from directkeys import PressKey, ReleaseKey


# Define a callback function to handle the key press event
# def on_space_pressed(event):
#     if event.name == 'space':
#         print('Space key pressed')

space_key_pressed = space_pressed
left_key_pressed = arrow_left_pressed
right_key_pressed = arrow_right_pressed
up_key_pressed = arrow_up_pressed
down_key_pressed = arrow_down_pressed
time.sleep(2.0)
current_key_pressed = set()

isPaused = True

cap = cv2.VideoCapture(0)
handDetector = HandDetector()

# subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
# subprocess.run(["python", "./game/Pacman_Complete/run.py"])

while True:
    success, image = cap.read()

    if not success:
        break

    keyPressed = False
    spacePressed = False
    arrowLeftPressed = False
    arrowRightPressed = False
    arrowUpPressed = False
    arrowDownPressed = False

    key_count = 0
    key_pressed = 0

    image = handDetector.find_hands(image)
    land_mark_list = handDetector.find_position(image, draw=False)
    fingers_up, thumb_direct, index_direct = handDetector.fingers_up()

    if fingers_up != None:
        max_fingers_up = fingers_up.count(1)
        status = 'Pause' if isPaused else 'Resume'
        cv2.putText(image, f'Fingers up: {str(max_fingers_up)}', (100, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(image, f'Game: {status}', (150, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)

    # print(fingers_up)
    # print(land_mark_list)
    # keyboard.on_press_key('space', on_space_pressed)

    if fingers_up == [1,1,1,1,1] and not isPaused:
        isPaused = True
        PressKey(space_key_pressed)
        time.sleep(0.1)
        spacePressed = True
        current_key_pressed.add(space_key_pressed)
        key_pressed = space_key_pressed
        keyPressed = True
        key_count += 1

    if fingers_up == [0,0,0,0,0] and isPaused:
        isPaused = False
        PressKey(space_key_pressed)
        time.sleep(0.1)
        spacePressed = True
        current_key_pressed.add(space_key_pressed)
        key_pressed = space_key_pressed
        keyPressed = True
        key_count += 1

    if fingers_up == [1,0,0,0,0] and thumb_direct == 'left' and index_direct == '':
        cv2.putText(image, 'Action: go left', (100, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        PressKey(left_key_pressed)
        time.sleep(0.1)
        arrowLeftPressed = True
        current_key_pressed.add(left_key_pressed)
        key_pressed = left_key_pressed
        keyPressed = True
        key_count += 1

    if fingers_up == [1,0,0,0,0] and thumb_direct == 'right' and index_direct == '':
        cv2.putText(image, 'Action: go right', (100, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        PressKey(right_key_pressed)
        time.sleep(0.1)
        arrowRightPressed = True
        current_key_pressed.add(right_key_pressed)
        key_pressed = right_key_pressed
        keyPressed = True
        key_count += 1

    if fingers_up == [0,1,0,0,0] and index_direct == 'up' and thumb_direct == '':
        cv2.putText(image, 'Action: go up', (100, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        PressKey(up_key_pressed)
        time.sleep(0.1)
        arrowUpPressed = True
        current_key_pressed.add(up_key_pressed)
        key_pressed = up_key_pressed
        keyPressed = True
        key_count += 1

    if fingers_up == [0,0,1,1,1] and index_direct == 'down' and thumb_direct == '':
        cv2.putText(image, 'Action: go down', (100, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
        PressKey(down_key_pressed)
        time.sleep(0.1)
        arrowDownPressed = True
        current_key_pressed.add(down_key_pressed)
        key_pressed = down_key_pressed
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
