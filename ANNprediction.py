'''
Based on the trained model, predict and validate with the validation data set
The first function is to load the model with json and h5 file
Then predict with one single test or evaluate with the whole validation data set
'''
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import numpy as np
import tools.csvio as csvio
import tools.evaluation as eval
import os


def load_model(modelName):
    # load json and create model
    json_file = open('%s.json' % modelName, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("%s.h5" % modelName)
    print("Loaded model from disk")
    return loaded_model


def single_test(loaded_model, fileName='rtt_series/valid_data/5008.csv'):
    # Test for an input
    #test = np.array([189.21973,189.105955,189.0866,189.19152,189.18938,189.21477,189.363065,189.060735,189.018825,189.497595,189.460615,194.76307,196.72467,189.280095,189.014585,189.02478,189.03338,189.087215,88.99757,189.041955])
    #test = csvio.csv2list("rtt_series/real_trace_labelled/11119.csv", "rtt")
    test = csvio.csv2list(fileName, "rtt", sep=';', decimal='.')
    testLen = len(test)
    min_test = min(test)

    # Pre-Treatment
    for i in range(len(test)):
        test[i] = test[i] - min_test
    test = test.reshape(1, testLen, 1)

    # Prediction
    temp = loaded_model.predict(test)
    temp = temp.reshape(testLen)
    #print("temp =")
    #print(temp)
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


def model_evaluate(loaded_model, folderName='./rtt_series/valid_data'):
    # evaluate loaded model on test data
    SAMPLE_LEN = 100
    file_csv = os.listdir(folderName)
    N_SAMPLE = len(file_csv)
    X = np.array([])
    Y = np.array([])
    for f in file_csv:
        fileName = folderName + '/' + f
        test = csvio.csv2list(fileName, "rtt", sep=';', decimal='.')
        cp = csvio.csv2list(fileName, "cp", sep=';', decimal='.')

        # Pre-Treatment
        min_test = min(test)
        for i in range(len(test)):
            test[i] = test[i] - min_test

        X = np.concatenate([X, test])
        Y = np.concatenate([Y, cp])
    X = X.reshape(N_SAMPLE, SAMPLE_LEN, 1)
    Y = Y.reshape(N_SAMPLE, SAMPLE_LEN, 1)
    loaded_model.compile(loss='binary_crossentropy',
                         optimizer='adam', metrics=['accuracy'])
    score = loaded_model.evaluate(X, Y, verbose=1)
    print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))


def model_evaluate2precision_recall(loaded_model, folderName='./rtt_series/valid_data', resultName='./results/resultNeuroNet_w.csv'):
    # generate precision and recall for every test file
    file_csv = os.listdir(folderName)
    precision = []
    recall = []
    for f in file_csv:
        fileName = folderName + '/' + f
        test = csvio.csv2list(fileName, "rtt", sep=';', decimal='.')
        cp = csvio.csv2list(fileName, "cp", sep=';', decimal='.')

        # Pre-Treatment
        min_test = min(test)
        for i in range(len(test)):
            test[i] = test[i] - min_test

        testLen = len(test)
        test = test.reshape(1, testLen, 1)
        temp = loaded_model.predict(test)
        temp = temp.reshape(testLen)
        res = np.zeros(testLen)

        for i in range(testLen):
            if temp[i] >= 0.5:
                res[i] = 1
        ''' Binary to index
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
        '''
        cp = cp.astype(int)
        res = res.astype(int)
        
        print('res=')
        print(res)
        print('cp=')
        print(cp)
        #temp = eval.evaluation(cp, res)
        #precision.append(temp["precision"])
        #recall.append(temp["recall"])
    #csvio.list2csv(resultName, [file_csv, precision, recall], ['fileName', 'precision', 'recall'])
    print("Prediction & Recall saved.")


model = load_model("detectWithNeuroNetWithPreTreat")
single_test(model)
model_evaluate(model)
#model_evaluate2precision_recall(model, resultName='./results/resultNeuroNet.csv')
