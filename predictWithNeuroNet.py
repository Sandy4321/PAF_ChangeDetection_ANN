from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import numpy as np

# load json and create model
json_file = open('detectWithNeuroNet.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("detectWithNeuroNet.h5")
print("Loaded model from disk")

# Test for an input
test = np.array([121,121,121,121,132,132,132,132,132,132,88,88,88,88,88,88,88])
test = test.reshape(1,len(test),1)
temp = loaded_model.predict(test)
temp = temp.reshape(17)
res = np.zeros(len(temp))
for i in range(len(temp)):
	if temp[i] >= 0.5:
		res[i] = 1
print([0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0])
print(res)

'''
# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
'''