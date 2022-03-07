import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time

from action_space import generate_movement_dict
from agent import Agent

style.use("ggplot")

HM_EPISODES = 200

epsilon = 0.9
EPS_DECAY = 0.9998  # Every episode will be epsilon*EPS_DECAY
SHOW_EVERY = 20  # how often to play through env visually.

start_q_table = None # None or Filename

LEARNING_RATE = 0.1
DISCOUNT = 0.95

# return: {0:left_arm_move, 1: right_arm_move, 2: both_arm_move}
movement_dict = generate_movement_dict()

SIZE_theta = 72 # angle discretized in 72 buckets of 5 degrees
SIZE_rho = 16 # distance within range 200 to 1000 pixels, 50 buckets
SIZE_actions = 3 # 3 possible actions

if start_q_table is None:
    # initialize the q-table#
    q_table = {}
    for theta in range(SIZE_theta):
        for rho in range(SIZE_rho):
                q_table[theta,rho] = np.full(3,value_higher_than_reward) #TODO: define the reward value, higher than reward to allow exploration

# else:
#     with open(start_q_table, "rb") as f:
#         q_table = pickle.load(f)

episode_rewards = []

for episode in range(HM_EPISODES):
    astronaut = Agent()
    episode_reward = 0
    for i in range(200):
        obs = astronaut.get_state()

        if np.random.random() > epsilon:
            # GET THE ACTION
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 3)
        # Take the action!
        astronaut.do_action(action) # TODO: code the do_action function in Agent() which modifies the theta and rho
    
        #TODO: handling the reward: if the distance is smaller and the theta better, give a thumbs up

        new_obs = astronaut.get_state()  # new observation
        max_future_q = np.max(q_table[new_obs])  # max Q value for this new obs
        current_q = q_table[obs][action]

        if reward == winning_REWARD: # TODO: define the reward stuff
            new_q = winning_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        
        episode_reward += reward

        if reward == winning_REWARD or reward == losing_REWARD: # TODO: define the reward stuff
            break

        episode_rewards.append(episode_reward)
        epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,))/SHOW_EVERY, mode='valid')

plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"Reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)