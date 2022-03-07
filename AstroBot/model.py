import os
from tensorflow.keras import models
from tensorflow.keras import Sequential, layers
from tensorflow.keras import optimizers

def model_linear(path_model):
    '''Define model if no model pre-trained else upload model'''
    if False==True:
        #TODO instanciate model
        adam_opt = optimizers.Adam(learning_rate=0.01, beta_1=0.9, beta_2=0.999)
        model = Sequential()
        model.add(layers.Dense(8, input_dim=2, activation='relu'))
        model.add(layers.Dense(4, activation='relu')) #with input_dim=nb of features
        model.add(layers.Dense(3, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=adam_opt, metrics=['accuracy']) #TODO validate metrics
    else:
        model=models.load_model(path_model)
    return model







