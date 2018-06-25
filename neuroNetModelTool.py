import numpy as np
import time
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import matplotlib.pyplot as plt

def save_trained_model(model,fn="model"):
    """save to file the trained model
    """
    # serialize model to JSON
    model_json = model.to_json()
    with open("%s.json"%fn, "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("%s.h5"%fn)

def plot_leanring_curv(rec, fn='model'):
    """history of model fit
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for k in rec.history.keys():
        ax.plot(rec.history[k])
    ax.set_xlabel('epoch')
    ax.legend(rec.history.keys(), loc='upper left')
    fig.set_size_inches(10,8)
    plt.savefig("%s_learning_curve.pdf"%fn, format='pdf')
    plt.close()




