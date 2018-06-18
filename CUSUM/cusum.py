#https://www.researchgate.net/publication/230888065_Cumulative_sum_control_chart
#formule de CUSUM
import numpy as np
import matplotlib.pyplot as plt

value1=np.random.normal(0,1,20)
value2=np.random.normal(10,1,20)
value3=np.random.normal(0,1,20)
value4=np.random.normal(10,1,20)
value5=np.random.normal(20,1,20)
value6=np.random.normal(0,1,20)
values=np.concatenate((value1,value2,value3,value4,value5,value6),axis=0)
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

