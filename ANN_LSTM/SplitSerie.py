
import numpy as np

np.random.seed(1337)  # for reproducibility

import csv
import os


'''
to create the fichier of series split with number_x.csv and number_y.csv
to use this fonction 1. you have to create a folder name "dataset_split"
2. you have to take all the fichier.csv to the folder "dataset_original". For example 11017.csv.
'''
length=500
path='./dataset_original'
flag=0
for (path, dirs, files) in os.walk(path):
    for filename in files:

        print(filename)
        data_rtt_test=csv_t.csv2list("./dataset_original/"+str(filename),"rtt")
        data_cp_test=csv_t.csv2list("./dataset_original/"+str(filename),"cp")
        #write data x and y in nx.csv and ny.csv
        for i in range(int(len(data_rtt_test)/length)):
            filename_x =  str(flag+i) +"x"+ ".csv"
            with open("./dataset_split/"+filename_x,'w',newline='') as f:
                writer = csv.writer(f)
                begin=i*length
                end=(i+1)*length
                for val in data_rtt_test[begin:end]:
                    # print(val)
                    writer.writerow([val])
            f.close()
            filename_y =str(flag+i) +"y"+ ".csv"
            with open("./dataset_split/"+filename_y,'w',newline='') as f:
                writer = csv.writer(f)
                begin=i*length
                end=(i+1)*length
                for val in data_cp_test[begin:end]:
                    # print(val)
                    writer.writerow([val])
            f.close()
        flag = flag+int(len(data_cp_test)/1000)