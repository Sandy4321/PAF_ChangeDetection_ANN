import numpy as np
from matplotlib import pyplot as plt

def cusum(values): #Values are the values of the time-serie we are studying.
    S=0
    average =  np.average(values) #average of the time-serie
    changes = [0 for i in range(len(values))] #Position of the changes.
    cusum = []
    for i in range(len(values)):
        cusum.append(S)
        S = S + values[i]-average #The cumulative sum.
        if(abs(S) > 5): #I took 5 as a criteria of a cusum too different from zero but it is highly subjective. How do we choose this criteria ?
            changes[i] = 1
        else:
            changes[i] = 0
    
    index = [i for i in range(len(values))]
    
    plt.plot(index,cusum,label='Cusum')
    plt.plot(index,changes,'o',label='Position of the changes')
    plt.show()
    return