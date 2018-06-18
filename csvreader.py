import pandas
import timetools as tt

#Parameters
file_to_the_csv = './example/11017.csv'
column = 'rtt' #rtt or cp 


#Read the csv file
trace = pandas.read_csv(file_to_the_csv, sep=';', decimal=',')
try:
    x = [tt.string_to_datetime(i) for i in trace['epoch']]
except TypeError:
    x = [tt.epoch_to_datetime(i) for i in trace['epoch']]
y = trace[column]
y = y.as_matrix()
y = y.astype(np.float)