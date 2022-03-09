from black import main
import matplotlib.pyplot as plt
import pyvjoy
import cv2
import mediapipe as mp
import os
import pyautogui
from datetime import date, datetime
import pickle
from AstroBot.agent import Agent
import numpy as np
from ImageProcessing.station_detection import station_polar_coordinates
from predict_player_position import compute_player_position
from predict_grab_status import compute_grab_status
from deep_controller_class import DeepController
from predict_angle_correction import compute_angle_correction
from tensorflow.keras import models




mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

# Ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


# IgnoringStop ignoring tensorflow loading warnings (CUDA)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' 



# For webcam input:
cap = cv2.VideoCapture(0)
# For VJoy output:
j = pyvjoy.VJoyDevice(1)

def mode_selection():
    """Start deep controller"""
    print('\nWelcome to deep controller.\n')

    mode_details = """
    Select camera correction mode:
    1 - no camera correction
    2 - camera correction in game (X control)
    3 - camera correction with angle prediction model

    """

    mode_selection = 0
    while mode_selection not in [1,2,3]:
        mode_selection = int(input(mode_details))

    return mode_selection

mode_selection = mode_selection()

if mode_selection == 3: # predict angle correction mpde

  #importing model for angle correction:
  model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
  model = models.load_model(model_path)

gamepad=DeepController()

#AstroBot Inititalization
astrobot_isactive=False

SIZE_theta_astro = 72 # angle discretized in 72 buckets of 5 degrees
SIZE_theta_station = 72 # angle discretized in 72 buckets of 5 degrees
theta_astro_range = [theta_astro*5*np.pi/180 for theta_astro in range(SIZE_theta_astro)]
theta_station_range = [theta_station*5*np.pi/180 for theta_station in range(SIZE_theta_station)]
astronaut=Agent()
#TODO once pickle file available uncomment file below
#start_q_table ='q_table_ep0.pickle' # None or Filename
#start_q_table_path = os.path.join(os.path.dirname(__file__),'Q_tables',start_q_table)
# with open(start_q_table_path, "r+b") as f:
#   q_table = pickle.load(f)


with mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as holistic:
  while cap.isOpened():
    #print(gamepad.right_hand_coordinate_y,gamepad.right_hand_coordinate_x,gamepad.left_hand_coordinate_y,gamepad.left_hand_coordinate_x)
    #print(datetime.now().second) # TODO print timestamp for dev, remove for prod

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
    
    if player_position.get('astro_bot', False):
        astrobot_isactive=True

    if astrobot_isactive:
      #Take screenshot
      image_game = pyautogui.screenshot()
      #From screenshot get angle of station if no angle then random value
      astronaut_station_distance, astronaut_station_angle = station_polar_coordinates(image_game)
      if not astronaut_station_angle:
        astronaut_station_angle = np.random.choice(theta_station_range)
      else:
        astronaut.astronaut_station_angle=astronaut_station_angle
      #From screenshot get angle of astronaut
      angle_correction = compute_angle_correction(image_game, model)

      #From those angles retreive closest discrete value in angle_range
      tmp_obs = (angle_correction/5*np.pi/180,astronaut_station_angle/5*np.pi/180)
      index_astro = (np.abs(np.array(theta_astro_range)-tmp_obs[0])).argmin()
      index_station = (np.abs(np.array(theta_station_range)-tmp_obs[1])).argmin()
      obs = (theta_astro_range[index_astro],theta_station_range[index_station])

      #Get best action from q_table
      action = np.argmax(q_table[obs])
      astronaut.do_action(action,j,angle_correction)
      
      
      #If station is no_longer visible then deactivate astrobot
      if not astronaut_station_distance or astronaut_station_distance<=250:
        astrobot_isactive=False
      else:
        astronaut.astronaut_station_distance=astronaut_station_distance

    else:
      if mode_selection == 3: # predict angle correction mode
        image_game = pyautogui.screenshot()
        angle_correction = compute_angle_correction(image_game, model)
      else:
        angle_correction = 0 # do not compute angle correction

      if mode_selection == 2: # reset angle correction
        gamepad.update_vjoy(player_position, grab_status, angle_correction, camera_auto_rotation=True)
      else:
        gamepad.update_vjoy(player_position, grab_status, angle_correction, camera_auto_rotation=False)
        

   
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
