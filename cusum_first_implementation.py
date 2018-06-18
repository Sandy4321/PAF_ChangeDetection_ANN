import numpy as np
from matplotlib import pyplot as plt

#Method of Liang
def cusum_var(y):
    #https://www.researchgate.net/publication/230888065_Cumulative_sum_control_chart
    
    values = y
    change = [0 for i in range(len(values))]
    Ci_plus=[0 for i  in range(len(values))]
    Ci_moins=[0 for i  in range(len(values))]
    
    u0=y[0]
    var=np.var(values)
    H=5*np.sqrt(var)
    k=5*np.sqrt(var)/2
    
    
    for i in range(len(values)-1):
        Ci_plus[i+1]=np.max( [0,values[i+1]-(u0+k)+Ci_plus[i]])
        Ci_moins[i+1]=np.max([0,(u0-k)-values[i+1]+Ci_moins[i]])
        if ((Ci_plus[i+1]>H)or(Ci_moins[i+1]>H)):
            Ci_plus[i+1]=0
            Ci_moins[i+1]=0
            change[i+1]=1
            u0=values[i+1]
        else:
            change[i+1]=0
    plt.plot(values,'r',change,'o')
    plt.show()
    return change



#Method of Alberto -- the first one. We can forget it but we may use it to test the evaluation.
def cusum_simple(values): #Values are the values of the time-serie we are studying.
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
    return changes