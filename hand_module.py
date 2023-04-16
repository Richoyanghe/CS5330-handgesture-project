import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, hands_to_track=1,
                 detection_confidence=0.5,
                 tracking_confidence=0.5) -> None:

        self.mode = mode
        self.hands_to_track = hands_to_track
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(
            static_image_mode = self.mode,
            max_num_hands = self.hands_to_track,
            min_detection_confidence = self.detection_confidence,
            min_tracking_confidence = self.tracking_confidence
        )

        self.mp_drawing_utils = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.tips_id_list = [4, 8, 12, 16, 20]


    def find_hands(self, image, draw=True):
        self.result = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if self.result.multi_hand_landmarks and draw:
            for hand_landmark in self.result.multi_hand_landmarks:
                self.mp_drawing_utils.draw_landmarks(
                    image,
                    hand_landmark,
                    self.mp_hand.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )

        return image


    def find_position(self, image, hand_index=0, draw=True):
        self.land_mark_list = []

        if self.result.multi_hand_landmarks:
            interest_hand = self.result.multi_hand_landmarks[hand_index]

            for id, landmark in enumerate(interest_hand.landmark):

              h, w, c = image.shape

              cx, cy = int(landmark.x*w), int(landmark.y*h)

              self.land_mark_list.append([id, cx, cy])

              if draw:
                  cv2.circle(image, (cx, cy), 10, (250, 0, 0), cv2.FILLED)

        return self.land_mark_list


    def fingers_up(self):
        if len(self.land_mark_list) != 0:
            fingers_counter = []

            # Check for left or right hand
            if self.land_mark_list[0][1] > self.land_mark_list[1][1]:
                leftOrRight = 'left'
            else:
                leftOrRight = 'right'

            # Check for thumb tip
            left_thumb_up = leftOrRight == 'left' and self.land_mark_list[self.tips_id_list[0]][1] < self.land_mark_list[self.tips_id_list[0]-1][1]
            right_thumb_up = leftOrRight == 'right' and self.land_mark_list[self.tips_id_list[0]][1] > self.land_mark_list[self.tips_id_list[0]-1][1]

            if left_thumb_up or right_thumb_up:
                fingers_counter.append(1)
            else:
                fingers_counter.append(0)

            # Check for other fingers tip
            for i in range(1, 5):
                tip_id = self.tips_id_list[i]
                if self.land_mark_list[tip_id][2] < self.land_mark_list[tip_id-2][2]:
                    fingers_counter.append(1)
                else:
                    fingers_counter.append(0)

            return fingers_counter

        return None
