import os
import tools.csvio as csv
import cusum_first_implementation as cusum
import tools.evaluation as eval
import matplotlib.pyplot as plt
import numpy as np 
import baysiancpdetection as baycpdc #To be removed (commented) if not needed (needs R)

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
    

#Function that calculate and plot the Fn measure for both methods (n is generally 1 or 2)
def Fn_score(n):
    recallBayesian=csv.csv2list('./results/resultBaysian.csv','recall')
    precisionBayesian=csv.csv2list('./results/resultBaysian.csv','precision')
    
    Fn_bayesian=[]
    for i in range(len(recallBayesian)):
        if(recallBayesian[i] != 0 or precisionBayesian[i] != 0):
            Fn_bayesian.append((1+n*n)*(precisionBayesian[i]*recallBayesian[i])/(n*n*(precisionBayesian[i]+recallBayesian[i])))
        
        else:
            Fn_bayesian.append(0)
    
    recallCusum=csv.csv2list('./results/resultCUSUM.csv','recall')
    precisionCusum=csv.csv2list('./results/resultCUSUM.csv','precision')
    
    Fn_cusum=[]
    for i in range(len(recallCusum)):
        if(recallCusum[i] != 0 or precisionCusum[i] != 0):
            Fn_cusum.append((1+n*n)*(precisionCusum[i]*recallCusum[i])/(n*n*(precisionCusum[i]+recallCusum[i])))
        
        else:
            Fn_cusum.append(0)
    
    plt.plot(Fn_bayesian,"x",label="Bayesian method")
    plt.plot(Fn_cusum,"x",label="Cusum method")
    plt.legend()
    plt.xlabel("Index of datasets")
    plt.ylabel("Fn_measure")
    plt.title("F Score for n="+str(n)+" applied to the results of Bayesian and Cusum methods")
    plt.show()
    return

def comparison_precision():
    precisionC=csv.csv2list('./results/resultCUSUM.csv','precision')
    precisionB=csv.csv2list('./results/resultBaysian.csv','precision')
    cdf=[float(k+1)/len(precisionC) for k in range(len(precisionC))]
    precisionC.sort()
    precisionB.sort()
    plt.plot(precisionC,cdf,"r",label="precision of cusum method")
    plt.plot(precisionB,cdf,"b",label="precision of bayesian method")
    plt.legend()
    plt.xlabel("precision")
    plt.ylabel("cdf")
    plt.title("comparison of cdf (precision)")
    plt.show()
    return

def comparison_recall():
    recallC=csv.csv2list('./results/resultCUSUM.csv','recall')
    recallB=csv.csv2list('./results/resultBaysian.csv','recall')
    cdf=[float(k+1)/len(recallC) for k in range(len(recallC))]
    recallC.sort()
    recallB.sort()
    plt.plot(recallC,cdf,"r",label="recall of cusum method")
    plt.plot(recallB,cdf,"b",label="recall of bayesian method")
    plt.legend()
    plt.xlabel("recall")
    plt.ylabel("cdf")
    plt.title("comparison of cdf (recall)")
    plt.show()
    return

def recall_precision():
    precisionC=csv.csv2list('./results/resultCUSUM.csv','precision')
    precisionB=csv.csv2list('./results/resultBaysian.csv','precision')
    recallC=csv.csv2list('./results/resultCUSUM.csv','recall')
    recallB=csv.csv2list('./results/resultBaysian.csv','recall')
    plt.plot(precisionC,recallC,"rx", label="cusum method")
    plt.plot(precisionB,recallB,"bx", label="bayesian method")
    plt.legend()
    plt.xlabel("precision")
    plt.ylabel("recall")
    plt.title("scatterplot (precision,recall)")
    plt.show()
    return

#evaluationDataSet("./rtt_series/real_trace_labelled")
        
        
