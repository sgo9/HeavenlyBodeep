import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
import pyautogui
from HeavenlyBodeep.utils import distance
from action_space import generate_movement_dict
from ImageProcessing.station_detection import station_polar_coordinates
from agent import Agent
import pyvjoy
from HeavenlyBodeep.predict_angle_correction import compute_angle_correction
import os
import json
from tensorflow.keras import models

q_path=os.path.join(os.path.dirname(__file__),"Q_tables")
style.use("ggplot")

#importing model for angle correction:
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
model = models.load_model(model_path)
j = pyvjoy.VJoyDevice(1)

HM_EPISODES = 200

epsilon = 0.9
EPS_DECAY = 0.9998  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = 20  # how often to play through env visually.
MAX_NB_MOVES=50
start_q_table = None # None or Filename

LEARNING_RATE = 0.1
DISCOUNT = 0.95

# return: {0:left_arm_move, 1: right_arm_move, 2: both_arm_move}
movement_dict = generate_movement_dict()

SIZE_theta = 72 # angle discretized in 72 buckets of 5 degrees
SIZE_rho = 16 # distance within range 200 to 1000 pixels, 50 buckets
SIZE_actions = 3 # 3 possible actions
winning_distance=200

if start_q_table is None:
    # initialize the q-table#
    q_table = {}
    for theta in range(SIZE_theta):
        for rho in range(SIZE_rho):
                q_table[theta,rho] = np.full(3,0) #TODO: define the reward value, higher than reward to allow exploration
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)

episode_rewards = []

for episode in range(HM_EPISODES):
    astronaut = Agent()
    episode_reward = 0
    distances=[]
    
    #We need to have at least 3 distances in order to be able to generate a reward
    while len(distances)!=3:
        image=pyautogui.screenshot()
        astronaut_station_distance, _=station_polar_coordinates(image)
        distances.append(astronaut_station_distance)

    for i in range(MAX_NB_MOVES): 
        obs = astronaut.get_state()
        image=pyautogui.screenshot()
        
        if np.random.random() > epsilon:
            # GET THE ACTION
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 3)
        # Take the action!
        angle_correction=compute_angle_correction(image,model)
        astronaut.do_action(action,j,angle_correction) # code the do_action function in Agent() which modifies the theta and rho
    
        #handling the reward: if the distance is smaller and the theta better, give a thumbs up
        
        astronaut_station_distance, _=station_polar_coordinates(image)
        distances.append(astronaut_station_distance)
        distances=distances[1:]
        reward=2*distances[1]-distances[0]-distances[2]



        new_obs = astronaut.get_state()  # new observation
        max_future_q = np.max(q_table[new_obs])  # max Q value for this new obs
        current_q = q_table[obs][action]

        if distances[-1]<winning_distance: 
            new_q = 10_000 #TODO: to be validate once we have a better understanding of reward scale
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        
        episode_reward += reward

        if distances[-1]<winning_distance: # TODO: define the reward stuff
            break

        
        

    #TODO before starting new epoch swim randomly
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY
    if episode%10==0:
        q_file=os.path.join(q_path,f'q_table_{episode}.pickle')
        with open(q_file, "wb") as f:
            pickle.dump(q_table, f)
    
    for i in range(15):
         action=np.random.randint(0,2)
         astronaut.do_action(action,j,angle_correction)
    

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)