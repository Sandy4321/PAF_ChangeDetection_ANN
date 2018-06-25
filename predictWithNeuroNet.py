from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import numpy as np
import tools.csvio as csvio

# load json and create model
json_file = open('detectWithNeuroNet.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("detectWithNeuroNet.h5")
print("Loaded model from disk")

# Test for an input
test = np.array([189.21973,189.105955,189.0866,189.19152,189.18938,189.21477,189.363065,189.060735,189.018825,189.497595,189.460615,194.76307,196.72467,189.280095,189.014585,189.02478,189.03338,189.087215,88.99757,189.041955])
#test = csvio.csv2list("rtt_series/dataset_split/20xy.csv", "rtt")
testLen = len(test)
test = test.reshape(1,testLen,1)
temp = loaded_model.predict(test)
temp = temp.reshape(testLen)
print(temp)
res = np.zeros(testLen)
for i in range(testLen):
	if temp[i] >= 0.5:
		res[i] = 1
#print([0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0])
print(res)
print(sum(res))

'''
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
'''