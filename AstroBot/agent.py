from time import sleep
import numpy as np
from HeavenlyBodeep.deep_controller import update_vjoy
from AstroBot.action_space import generate_movement_dict


class Agent:

    def __init__(self):
        # self.n_moves=0
        # self.epsilon=0 #randomness
        # self.model=model #ToDo create class model
        self.move_dict = generate_movement_dict(1)
        self.astronaut_station_distance=0
        self.astronaut_station_angle=0
        self.chevron_angle=-1
        #self.trainer=QTrainer(self.model,lr=LR,gamma=self.gamma) 
        pass

    def get_state(self,distance,angle):

        return np.array([distance,angle])

    # def get_action(self,state):
    #     #random moves:tradeoff exploration/exploitation
    #     self.epsilon=20-self.n_moves
    #     if random.randint(0,200)<self.epsilon:
    #         move=random.randint(0,2)
    #     else:
    #         prediction = self.model(state)
    #         move=self.model.argmax(prediction).item()
    #     return move
    
    def do_action(self,action,j,angle_correction):
        for player_position in self.move_dict[action]:
            update_vjoy(j, player_position, {}, angle_correction)
            sleep(0.1)

    # def remember(self,state,action,reward,next_state,done):
    #     self.memory.append((state,action,reward,next_state,done))#popleft if maxmemory is reach

    # def train_long_memory(self):
    #     pass

    # def train_short_memory(self,state,action,reward,next_state,done):
    #     self.trainer.train_step(state,action,reward,next_state,done)
    
