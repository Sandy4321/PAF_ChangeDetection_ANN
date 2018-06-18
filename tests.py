import csvreader as csv
import cusum_first_implementation as cusum
import evaluation as eval

def test(file_to_the_csv):
    reality = csv.csv2list(file_to_the_csv,'rtt')
    detection = cusum.cusum_var(reality)
    fact = csv.csv2list(file_to_the_csv,'cp')
    result = eval.evaluation(fact,detection)
    return result
    
    