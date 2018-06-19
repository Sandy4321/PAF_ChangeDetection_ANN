import pandas
import timetools as tt
import numpy as np

"""Parameters of the function could be 
file_to_the_csv = './rtt_series/11017.csv'
column = 'rtt' #rtt or cp 
"""

#Read
def csv2list(filename, column):
    #Read the csv file
    trace = pandas.read_csv(filename, sep=';', decimal=',')
    y = trace[column]
    y = y.as_matrix()
    y = y.astype(np.float)
    return y

#Write
def list2csv(filename, lists, columns):
    dataFrame = pandas.DataFrame(lists, columns = columns)
    dataFrame.to_csv(filename, index = False, sep = ';', decimal = ',')

list2csv('test.csv', [[0, 1], [2, 3]], ["rr", "cc"])
