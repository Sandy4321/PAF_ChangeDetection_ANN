import numpy as np
import os
# np.random.seed(42)
# import benchmark as bch
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed, Bidirectional
from keras.models import Sequential
import matplotlib.pyplot as plt
import tools.csvio as csvio
import neuroNetModelTool as md

# global config
#SEQ_LEN = 20
#N_SAMPLE = 1000
N_EPOCH = 500
MTX = ['acc']
folderName = './rtt_series/dataset_split'
#folderName = './example'

# Read data from the folder
file_csv = os.listdir(folderName)
x = []
y = []
SAMPLE_LEN = 0
for f in file_csv:
    f = folderName + '/' + f
    temp = csvio.csv2list(f, 'rtt')
    x.append(temp)
    y.append(csvio.csv2list(f, 'cp'))
    
#prepare data
for i in range(len(x)):
    x[i] = [x[i][j] - min(x[i]) for j in range(len(x[i]))]
    x[i] = np.asarray(x[i])
    
change = [0]*len(y)
for i in range(len(y)):
    for j in range(len(y[i])):
        if y[i][j] == 1:
            change[i] = 1

# Get the biggest value of the sample length
    if len(temp) > SAMPLE_LEN:
        SAMPLE_LEN = len(temp)
N_SAMPLE = len(x)

print('N_SAMPLE = ')
print(N_SAMPLE)

print('SAMPLE_LEN = ')
print(SAMPLE_LEN)
# 0-padding for the samples whose length is less than SAMPLE_LEN
data_x = []
data_y = []
for i in range(len(x)):
    if len(x[i]) != SAMPLE_LEN:
        data_x.extend(x[i].tolist())
        data_x.extend(np.zeros(SAMPLE_LEN - len(x[i])).tolist())
    else:
        data_x.extend(x[i].tolist())
    
# change list to np.array
data_x = np.asarray(data_x)
change = np.asarray(change)

# Reshape the data set for the input
change = change.reshape(N_SAMPLE, 1)
data_x = data_x.reshape(N_SAMPLE, SAMPLE_LEN,1)

# prepare the model
model = Sequential()
model.add(LSTM(64, return_sequences = False, input_shape = (None, 1)))
model.add(Dense(1, activation = 'sigmoid'))
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = MTX)
history = model.fit(data_x, change, validation_split = 0.2,
                    epochs = N_EPOCH, batch_size = SAMPLE_LEN, verbose=1)
print(model.summary())

md.save_trained_model(model, fn='detectWithNeuroNet')
md.plot_leanring_curv(history, fn='detectWithNeuroNet')
