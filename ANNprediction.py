from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import numpy as np
import tools.csvio as csvio
import tools.evaluation as eval
import os 

# load json and create model
json_file = open('noPosition.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("noPosition.h5")
print("Loaded model from disk")

'''
# Test for an input
#test = np.array([189.21973,189.105955,189.0866,189.19152,189.18938,189.21477,189.363065,189.060735,189.018825,189.497595,189.460615,194.76307,196.72467,189.280095,189.014585,189.02478,189.03338,189.087215,88.99757,189.041955])
#test = csvio.csv2list("rtt_series/real_trace_labelled/11119.csv", "rtt")
fileName = 'rtt_series/valid_data/5008.csv'
test = csvio.csv2list(fileName, "rtt", sep=';', decimal='.')
testLen = len(test)
min_test = min(test)
for i in range(len(test)):
    test[i] = test[i] - min_test

test = test.reshape(1,testLen,1)
temp = loaded_model.predict(test)
temp = temp.reshape(testLen)
print("temp =")
print(temp)
res = np.zeros(testLen)
for i in range(testLen):
	if temp[i] >= 0.5:
		res[i] = 1
cp = csvio.csv2list(fileName, "cp", sep=';', decimal='.')
print("cp =")
print(cp)
print(sum(cp))
print("res =")
print(res)
print(sum(res))
'''
# evaluate loaded model on test data
folderName = './rtt_series/valid_data'
SAMPLE_LEN = 100

file_csv = os.listdir(folderName)
N_SAMPLE = len(file_csv)
X = np.array([])
Y = np.array([])
for f in file_csv:
    fileName = folderName + '/' + f
    test = csvio.csv2list(fileName, "rtt", sep=';', decimal='.')
    cp = csvio.csv2list(fileName, "cp", sep=';', decimal='.')
    X = np.concatenate([X, test])
    Y = np.concatenate([Y, cp])    
X = X.reshape(N_SAMPLE, SAMPLE_LEN, 1)
Y = Y.reshape(N_SAMPLE, SAMPLE_LEN, 1)
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
score = loaded_model.evaluate(X, Y, verbose=1)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


'''
folderName = './rtt_series/artificial_dataset'
file_csv = os.listdir(folderName)
precision = []
recall = []
for f in file_csv:
    fileName = folderName + '/' + f
    test = csvio.csv2list(fileName, "trace", sep=',', decimal='.')
    cp = csvio.csv2list(fileName, "cpt", sep=',', decimal='.')
    testLen = len(test)
    test = test.reshape(1,testLen,1)
    temp = loaded_model.predict(test)
    temp = temp.reshape(testLen)
    res = np.zeros(testLen)

    for i in range(testLen):
        if temp[i] >= 0.5:
            res[i] = 1
    temp = []
    for i in range(len(res)):
        if(res[i] == 1):
            temp.append(i)
    res = temp
    temp = []
    for i in range(len(cp)):
        if(cp[i] - 1 < 0.001):
            temp.append(i)
    cp = temp

    temp = eval.evaluation_window_adp(cp, res, 2)
    precision.append(temp["precision"])
    recall.append(temp["recall"])
csvio.list2csv('./results/resultNeuroNet_w.csv', [file_csv, precision, recall], ['fileName', 'precision', 'recall'])
'''
