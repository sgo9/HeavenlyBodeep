import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
import pyautogui
import pyvjoy
import os
import json
from tensorflow.keras import models

from AstroBot.agent import Agent
from AstroBot.dummy_bot import dummy_decision
from ImageProcessing.chevron_detection import chevron_angle
from HeavenlyBodeep.predict_angle_correction import compute_angle_correction
from ImageProcessing.station_detection import station_polar_coordinates
from AstroBot.action_space import generate_movement_dict

q_path = os.path.join(os.path.dirname(__file__),"Q_tables")

#importing model for angle correction:
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'model.h5')
model = models.load_model(model_path)
j = pyvjoy.VJoyDevice(1)

# return: {0:left_arm_move, 1: right_arm_move, 2: both_arm_move}
movement_dict = generate_movement_dict()

HM_EPISODES = 200

epsilon = 0.9
EPS_DECAY = 0.9998  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = 20  # how often to play through env visually.
MAX_NB_MOVES = 50
start_q_table = 'q_table_ep0.pickle' # None or Filename
start_q_table_path = os.path.join(os.path.dirname(__file__),'Q_tables',start_q_table)

LEARNING_RATE = 0.1
DISCOUNT = 0.95

SIZE_theta_astro = 72 # angle discretized in 72 buckets of 5 degrees
SIZE_theta_station = 72 # angle discretized in 72 buckets of 5 degrees
SIZE_actions = 3 # 3 possible actions
winning_distance = 200

# theta_astro_range = [theta_astro*5*np.pi/180 for theta_astro in range(SIZE_theta_astro)]
# theta_station_range = [theta_station*5*np.pi/180 for theta_station in range(SIZE_theta_station)]
theta_delta=[theta_station*5*np.pi/180 for theta_station in range(SIZE_theta_station)]

if start_q_table is None:
    # initialize the q-table#
    q_table = {}
    for theta_astro in theta_delta:
        #for theta_station in theta_station_range:
        q_table[theta_astro] = np.full(3,0)
else:
    with open(start_q_table_path, "r+b") as f:
        q_table = pickle.load(f)

# start the training
episode_rewards = []
astronaut = Agent()
for episode in range(HM_EPISODES):

    
    episode_reward = 0
    distances = []
    initial_loop = True
    
    #We need to have at least 3 distances in order to be able to generate a reward
    while len(distances) != 3:
        image = pyautogui.screenshot()
        astronaut_station_distance, _ = station_polar_coordinates(image)
        if astronaut_station_distance:
            distances.append(astronaut_station_distance)
        else:
            distances.append(0)
    
    for i in range(MAX_NB_MOVES):
        new_image = pyautogui.screenshot()
        new_astronaut_station_distance, new_astronaut_station_angle = station_polar_coordinates(new_image)
        new_angle_astro = compute_angle_correction(new_image,model)
        if new_astronaut_station_distance:
            if initial_loop:
                obs = np.random.choice(theta_delta)
                new_angle_astro=np.random.choice(theta_delta)
                initial_loop = False
            else:
                obs = new_obs
            
            random=False
            if np.random.random() > epsilon:
                # GET THE ACTION
                action = np.argmax(q_table[obs])
            else:
                random=True
                action = np.random.randint(0, 3)
            # Take the action!
            
            astronaut.do_action(action,j,new_angle_astro) # code the do_action function in Agent() which modifies the theta and rho
        
            #handling the reward: if the distance is smaller and the theta better, give a thumbs up
            

            astronaut.astronaut_station_distance=new_astronaut_station_distance
            astronaut.astronaut_station_angle=new_astronaut_station_angle

            if new_astronaut_station_distance:
                distances.append(new_astronaut_station_distance)
            else:
                distances.append(0)

            distances = distances[1:]
            #reward = 2*distances[1]-distances[0]-distances[2]
            reward=-distances[0]


            if not new_astronaut_station_angle:
                new_astronaut_station_angle = np.random.choice(theta_delta)

            tmp_obs = (new_angle_astro*np.pi/180+2*np.pi)%(2*np.pi)-(new_astronaut_station_angle*np.pi/180+2*np.pi)%(2*np.pi) # new observation
            tmp_obs=tmp_obs/5
            if tmp_obs!= None:
                index_delta= (np.abs(np.array(theta_delta)-tmp_obs)).argmin()
                new_obs = theta_delta[index_delta]
            else:
                pass
            max_future_q = np.max(q_table[new_obs])  # max Q value for this new obs
            current_q = q_table[obs][action]

            if distances[-1] < winning_distance: 
                new_q = 10_000 #TODO: to be validated once we have a better understanding of reward scale
            else:
                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
            
            q_table[obs][action]=new_q

            episode_reward += reward

            if distances[-1] < winning_distance: 
                break
            print(f'episode:{episode}, move:{i}, distance:{distances[-1]}, old_q:{round(current_q)}, new_Q:{round(new_q)}, reward:{reward}, random:{random}')
        
        else:
            chevron=chevron_angle(new_image)
            if chevron:
                astronaut.chevron_angle = chevron
            action=dummy_decision(astronaut.astronaut_station_distance,astronaut.astronaut_station_angle,astronaut.chevron_angle, new_angle_astro)
            astronaut.do_action(action,j,new_angle_astro)
            print('no distance - dummy bot move')

    # before starting new epoch swim randomly
    
    completion_training=np.array(list(q_table.values()))
    completion_training=(np.count_nonzero(completion_training)/np.size(completion_training))*100
    print(f'q_table completion:{completion_training}%')
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY
    if episode%10==0:
        q_file=os.path.join(q_path,f'q_table_ep{start_q_table}.pickle')
        with open(q_file, "w+b") as f:
            pickle.dump(q_table, f)
    
    for i in range(30):
        new_image = pyautogui.screenshot()
        new_astronaut_station_distance, new_astronaut_station_angle = station_polar_coordinates(new_image)
        new_angle_astro = compute_angle_correction(new_image,model)
        if new_astronaut_station_distance:
            action=np.random.randint(0,2)
            astronaut.do_action(action,j,new_angle_astro)
            print('station too close - random move')
        else:
            print('station too close - but random move interrupted')
            chevron=chevron_angle(new_image)
            if chevron:
                astronaut.chevron_angle = chevron
            action=dummy_decision(astronaut.astronaut_station_distance,astronaut.astronaut_station_angle, astronaut.chevron_angle, new_angle_astro)
            astronaut.do_action(action,j,new_angle_astro)
    

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

style.use("ggplot")

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)