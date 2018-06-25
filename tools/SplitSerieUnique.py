import numpy as np
import tools.csvio as csv_t
import csv
import os
import sys
'''
Run only once
to create the fichier of series split with number_x.csv and number_y.csv
to use this fonction 1. you have to create a folder name "dataset_split"
2. you have to take all the fichier.csv to the folder "dataset_original". For example 11017.csv.
'''

length=500
path_original='./tools/dataset_original/'
path_generate="./dataset_split/"
flag=0
for (path_original, dirs, files) in os.walk(path_original):
    for filename in files:

        print(filename)
        data_rtt_test=csv_t.csv2list(path_original+str(filename),"rtt")
        data_cp_test=csv_t.csv2list(path_original+str(filename),"cp")
        #write data x and y in nx.csv and ny.csv

        for i in range(int(len(data_rtt_test)/length)):
            val_cp = []
            val_rtt = []
            header=["rtt","cp"]
            filename_x =  str(flag+i) +"xy"+ ".csv"
            with open(path_generate+filename_x,'wt') as f:
                writer = csv.writer(f)
                begin=i*length
                end=(i+1)*length
                for val in data_rtt_test[begin:end]:
                    val_rtt.append(val)
                for val in data_cp_test[begin:end]:
                    val_cp.append(val)
                val=[val_rtt,val_cp]
                filename=path_generate+filename_x
                print(filename)
                csv_t.list2csv(filename,val,["rtt","cp"])
            f.close()

        flag = flag+int(len(data_cp_test)/1000)
