
import random


class Agent:

    def __init__(self,model):
        self.n_moves=0
        self.epsilon=0 #randomness
        self.model=model #ToDo create class model
        #self.trainer=QTrainer(self.model,lr=LR,gamma=self.gamma) 
        pass

    def get_state(self,distance,angle):

        return np.array([distance,angle])

    def get_action(self,state):
        #random moves:tradeoff exploration/exploitation
        self.epsilon=20-self.n_moves
        if random.randint(0,200)<self.epsilon:
            move=random.randint(0,2)
        else:
            prediction = self.model(state)
            move=model.argmax(prediction).item()
        return move

        return

    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done))#popleft if maxmemory is reach

    def train_long_memory(self):
        pass

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
    