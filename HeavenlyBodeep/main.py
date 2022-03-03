from dis import dis
from turtle import update
import matplotlib.pyplot as plt
import pyvjoy
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# Ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow.keras import models

# IgnoringStop ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' 

from predict_player_position import compute_player_position
from predict_grab_status import compute_grab_status
from deep_controller import update_vjoy

# For webcam input:
cap = cv2.VideoCapture(0)
# For VJoy output:
j = pyvjoy.VJoyDevice(1)

#importing model for angle correction:
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
model = models.load_model(model_path)

with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    # Compute player position, grab status and update the controller accordingly

    player_position = compute_player_position(results, discard_not_found=False)
    grab_status = compute_grab_status(results)
    update_vjoy(j, player_position, grab_status)

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())

    # mp_drawing.draw_landmarks(
    #         image,
    #         results.left_hand_landmarks,
    #         mp_holistic.HAND_CONNECTIONS,
    #         landmark_drawing_spec=mp_drawing_styles
    #         .get_default_pose_landmarks_style())

    # mp_drawing.draw_landmarks(
    #         image,
    #         results.right_hand_landmarks,
    #         mp_holistic.HAND_CONNECTIONS,
    #         landmark_drawing_spec=mp_drawing_styles
    #         .get_default_pose_landmarks_style())

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()