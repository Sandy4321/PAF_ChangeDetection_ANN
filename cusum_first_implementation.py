import numpy as np
from matplotlib import pyplot as plt
import pandas
import timetools as tt


#Read the csv file
trace = pandas.read_csv('11017.csv', sep=';', decimal=',')
try:
    x = [tt.string_to_datetime(i) for i in trace['epoch']]
except TypeError:
    x = [tt.epoch_to_datetime(i) for i in trace['epoch']]
y = trace['rtt']
y = y.as_matrix()
y = y.astype(np.float)

#Method of Liang
def cusum_Liang(y):
    #https://www.researchgate.net/publication/230888065_Cumulative_sum_control_chart
    '''
    value1=np.random.normal(0,1,20)
    value2=np.random.normal(10,1,20)
    value3=np.random.normal(0,1,20)
    value4=np.random.normal(10,1,20)
    value5=np.random.normal(20,1,20)
    value6=np.random.normal(0,1,20)
    values=np.concatenate((value1,value2,value3,value4,value5,value6),axis=0)
    '''
    values = y
    change = [0 for i in range(len(values))]
    Ci_plus=[0 for i  in range(len(values))]
    Ci_moins=[0 for i  in range(len(values))]
    
    u0=0
    taux=np.var(value1)
    print("taux is : "+str(taux))
    H=5*taux
    k=5*taux/2
    
    
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
    print("change is" , change)
    plt.plot(values,'r',change,'o')
    plt.show()

#Method of Alberto
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
cusum_Liang(y)