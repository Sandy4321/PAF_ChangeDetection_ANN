import os
import csvreader as csv
import cusum_first_implementation as cusum
import evaluation as eval
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
        
        
