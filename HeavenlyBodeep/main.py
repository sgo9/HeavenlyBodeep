import numpy as np
import os
import pyvjoy
import cv2
import mediapipe as mp
import pyautogui
import pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Ignoring tensorflow loading warnings (CUDA)
from tensorflow.keras import models
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' # IgnoringStop ignoring tensorflow loading warnings (CUDA)

from HeavenlyBodeep.utils import mode_selection
from HeavenlyBodeep.predict_player_position import compute_player_position
from HeavenlyBodeep.predict_grab_status import compute_grab_status
from HeavenlyBodeep.predict_angle_correction import compute_angle_correction
from HeavenlyBodeep.deep_controller import update_vjoy
from ImageProcessing.station_detection import station_polar_coordinates
from ImageProcessing.chevron_detection import chevron_angle
from AstroBot.agent import Agent
from AstroBot.dummy_bot import dummy_decision

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

cap = cv2.VideoCapture(0) # For webcam input:
j = pyvjoy.VJoyDevice(1) # For VJoy output:

path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'x360ce.exe')
os.startfile(path)

mode_selection = mode_selection() # without camera correction, auto camera reset or camera correction prediction

if mode_selection == 3: # predict angle correction mpde

  #importing model for angle correction:
  model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
  model = models.load_model(model_path)

#AstroBot Inititalization
astronaut=Agent()
astrobot_isactive=False
station_distance_memory = 0
station_angle_memory = 0
toggle_angle_memory = 0

# SIZE_theta_astro = 72 # angle discretized in 72 buckets of 5 degrees
# SIZE_theta_station = 72 # angle discretized in 72 buckets of 5 degrees
# theta_astro_range = [theta_astro*5*np.pi/180 for theta_astro in range(SIZE_theta_astro)]
# theta_station_range = [theta_station*5*np.pi/180 for theta_station in range(SIZE_theta_station)]

#TODO once pickle file available uncomment file below
#start_q_table ='q_table_ep0.pickle' # None or Filename
#start_q_table_path = os.path.join(os.path.dirname(__file__),'Q_tables',start_q_table)
# with open(start_q_table_path, "r+b") as f:
#   q_table = pickle.load(f)


with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue # if loading a video, use 'break' instead of 'continue'

    # To improve performance, optionally mark the image as not writeable
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    # Compute player position, grab status and update the controller accordingly
    player_position = compute_player_position(results, discard_not_found=False)
    grab_status = compute_grab_status(results)
    
    astrobot_isactive = player_position.get('astro_bot', False)

    if astrobot_isactive and mode_selection == 3:
      
      image_game = pyautogui.screenshot() #take screenshot

      #From screenshot get angle of astronaut
      angle_correction = compute_angle_correction(image_game, model)

      #From screenshot get station distance and angle
      astronaut.astronaut_station_distance, astronaut.astronaut_station_angle = station_polar_coordinates(image_game)
      if astronaut.astronaut_station_distance is not None:
        astrobot_isactive = astronaut.astronaut_station_distance > 300
      
      #From screenshot get chevron angle, if chevron angle not detected
      toggle_angle = chevron_angle(image_game)
      if toggle_angle:
          astronaut.chevron_angle = toggle_angle

      action=dummy_decision(astronaut.astronaut_station_distance,astronaut.astronaut_station_angle,astronaut.chevron_angle, angle_correction)
      astronaut.do_action(action,j,angle_correction)

    else:
      if mode_selection == 3: # predict angle correction mode
        image_game = pyautogui.screenshot()
        angle_correction = compute_angle_correction(image_game, model)
      else:
        angle_correction = 0 # do not compute angle correction

      if mode_selection == 2: # reset angle correction
        update_vjoy(j, player_position, grab_status, angle_correction, camera_auto_rotation=True)
      else:
        update_vjoy(j, player_position, grab_status, angle_correction, camera_auto_rotation=False)
   
    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_holistic.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles
        .get_default_pose_landmarks_style())

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()