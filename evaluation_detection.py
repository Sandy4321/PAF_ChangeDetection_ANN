import os
import csvio
import cusum_first_implementation as cusum
import evaluation as eval
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
evaluationDataSet("./rtt_series/real_trace_labelled")
        
        
