
import os

import ANNprediction as ap
import matplotlib.pyplot as plt

precision=[]
recall=[]
key_list=[]
value_list=[]
path_original = "rtt_series/valid_data/"
for (path_original, dirs, files) in os.walk(path_original):
    for file in files:
        model = ap.load_model("detectWithNeuroNetWithPreTreat")
        a =ap.single_test(model,fileName=path_original+file)
        precision.append(a['precision'])
        print("precision is : ",precision)
        recall.append(a['recall'])
        print("recall is : ",recall)

'''
'''
plt.figure()
ax1=plt.subplot(211)
ax2=plt.subplot(212)
plt.sca(ax1)
plt.hist( precision,color='r')
plt.title('distribution of precision ')
plt.xlabel('precision')
plt.ylabel('amount')
plt.sca(ax2)
plt.hist( recall)
plt.title('distribution of recall ')
plt.xlabel('recall')
plt.ylabel('amount')
plt.show()