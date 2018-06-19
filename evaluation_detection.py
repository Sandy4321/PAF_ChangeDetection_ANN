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
        reality = csv.csv2list(f,'rtt')
        
        detectionB = baycpd.baysiancpt(reality)
        detectionC = cusum.cusum_var(reality)

        fact = csv.csv2list(f,'cp')

        temp = eval.evaluation(fact,detectionB)
        precisionB.append(temp["precision"])
        recallB.append(temp["recall"])

        temp =  eval.evaluation(fact,detectionC)
        precisionC.append(temp["precision"])
        recallC.append(temp["recall"])
    csv.list2csv('./results/resultBaysian.csv', [file_csv, precisionB, recallB], ['fileName', 'precision', 'recall'])
    csv.list2csv('./results/resultCUSUM.csv', [file_csv, precisionC, recallC], ['fileName', 'precision', 'recall'])

def cdf_precision_cusum():
    precision=csv.csv2list('./results/resultCUSUM.csv','precision')
    cdf=[float(k+1)/len(precision) for k in range(len(precision))]
    precision.sort()
    plt.plot(precision,cdf)
    plt.xlabel("precision")
    plt.ylabel("cdf")
    plt.title("cdf of precision for cusum method")
    plt.show()
    return

def cdf_recall_cusum():
    recall=csv.csv2list('./results/resultCUSUM.csv','recall')
    cdf=[float(k+1)/len(recall) for k in range(len(recall))]
    recall.sort()
    plt.plot(recall,cdf)
    plt.xlabel("recall")
    plt.ylabel("cdf")
    plt.title("cdf of recall for cusum method")
    plt.show()
    return

def cdf_precision_baysian():
    precision=csv.csv2list('./results/resultBaysian.csv','precision')
    cdf=[float(k+1)/len(precision) for k in range(len(precision))]
    precision.sort()
    plt.plot(precision,cdf)
    plt.xlabel("precision")
    plt.ylabel("cdf")
    plt.title("cdf of precision for cusum method")
    plt.show()
    return

def cdf_recall_baysian():
    recall=csv.csv2list('./results/resultBaysian.csv','recall')
    cdf=[float(k+1)/len(recall) for k in range(len(recall))]
    recall.sort()
    plt.plot(recall,cdf)
    plt.xlabel("recall")
    plt.ylabel("cdf")
    plt.title("cdf of recall for cusum method")
    plt.show()
    return

#evaluationDataSet("./rtt_series/real_trace_labelled")
        
        
