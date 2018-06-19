import os
import tools.csvio as csv
import cusum_first_implementation as cusum
import tools.evaluation as eval
import matplotlib.pyplot as plt
import numpy as np 
import baysiancpdetection as baycpd

def evaluationDataSet(folder):
    file_csv=os.listdir(folder)
    precisionB=[]
    recallB=[]
    precisionC=[]
    recallC=[]

    for f in file_csv:
        f = folder + '/' + f
        reality = csvio.csv2list(f,'rtt')
        
        detectionB = baycpd.baysiancpt(reality)
        detectionC = cusum.cusum_var(reality)

        fact = csvio.csv2list(f,'cp')

        temp = eval.evaluation(fact,detectionB)
        precisionB.append(temp["precision"])
        recallB.append(temp["recall"])

        temp =  eval.evaluation(fact,detectionC)
        precisionC.append(temp["precision"])
        recallC.append(temp["recall"])
    csvio.list2csv('resultBaysian.csv', [file_csv, precisionB, recallB], ['fileName', 'precision', 'recall'])
    csvio.list2csv('resultCUSUM.csv', [file_csv, precisionC, recallC], ['fileName', 'precision', 'recall'])

def cdf_precision():
    precision=cusum_evaluation("./rtt_series/real_trace_labelled")[0]
    cdf=[float(k+1)/len(precision) for k in range(len(precision))]
    print cdf
    precision.sort()
    plt.plot(precision,cdf)
    plt.xlabel("precision")
    plt.ylabel("cdf")
    plt.title("cdf of precision for cusum method")
    plt.show()
    return
#evaluationDataSet("./rtt_series/real_trace_labelled")
        
        
