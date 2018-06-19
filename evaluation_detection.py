import os
import tools.csvreader as csv
import cusum_first_implementation as cusum
import tools.evaluation as eval
import matplotlib.pyplot as plt

def cusum_evaluation(folder):
    file_csv=os.listdir(folder)
    precision=[]
    recall=[]
    for f in file_csv:
        f="./rtt_series/real_trace_labelled/"+f
        reality = csv.csv2list(f,'rtt')
        detection = cusum.cusum_var(reality)
        fact = csv.csv2list(f,'cp')
        precision.append(eval.evaluation(fact,detection)["precision"])
        recall.append(eval.evaluation(fact,detection)["recall"])
    return precision, recall

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
         
        
