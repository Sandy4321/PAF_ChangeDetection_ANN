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
SAMPLE_LEN = 100
N_EPOCH = 200
MTX = ['acc']
folderName = './rtt_series/artificial_dataset'
#folderName = './example'

# Read data from the folder
file_csv = os.listdir(folderName)
x = []
y = []
min_x = 1000
#SAMPLE_LEN = 0
for f in file_csv:
    f = folderName + '/' + f
    temp = csvio.csv2list(f, 'trace', sep=',', decimal='.')
    if min_x > min(temp):
    	min_x = min(temp)
    x.append(temp)
    y.append(csvio.csv2list(f, 'cpt', sep=',', decimal='.'))
# Get the biggest value of the sample length
#    if len(temp) > SAMPLE_LEN:
#        SAMPLE_LEN = len(temp)
'''
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
        data_y.extend(y[i].tolist())
        data_y.append(1)
        data_y.extend(np.zeros(SAMPLE_LEN - len(x[i]) - 1).tolist())
    else:
        data_x.extend(x[i].tolist())
        data_y.extend(y[i].tolist())
'''

# add some zeros at the end
data_x = []
data_y = []

# Pre-Treatment
for i in range(len(x)):
	for j in range(len(x[i])):
		x[i][j] -= min_x

for i in range(len(x)):
    data_x.extend(x[i].tolist())
    data_y.extend(y[i].tolist())

N_SAMPLE = len(data_x) / SAMPLE_LEN
reste = len(data_x) % SAMPLE_LEN
if(reste != 0):
	N_SAMPLE += 1
	data_x.extend(np.zeros(SAMPLE_LEN - reste))
	data_y.append(1)
	data_y.extend(np.zeros(SAMPLE_LEN - reste -1))
       
# change list to np.array
data_x = np.asarray(data_x)
data_y = np.asarray(data_y)

# Reshape the data set for the input
data_y = data_y.reshape(N_SAMPLE, SAMPLE_LEN, 1)
data_x = data_x.reshape(N_SAMPLE, SAMPLE_LEN, 1)

# prepare the model
model = Sequential()
model.add(Bidirectional(LSTM(15, return_sequences = True), input_shape = (None, 1)))
model.add(TimeDistributed(Dense(1, activation = 'sigmoid')))
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = MTX)
history = model.fit(data_x, data_y, validation_split = 0.2,
                    epochs = N_EPOCH, batch_size = SAMPLE_LEN, verbose=1)
print(model.summary())

md.save_trained_model(model, fn='detectWithNeuroNetWithPreTreat')
md.plot_leanring_curv(history, fn='detectWithNeuroNetWithPreTreat')
