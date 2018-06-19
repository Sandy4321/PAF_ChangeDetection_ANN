"""Example function to get the evaluation of a result"""

import tools.csvio as csv
import cusum_first_implementation as cusum
import tools.evaluation as eval
#import baysiancpdetection as baycpd


def test(file_to_the_csv):
    reality = csv.csv2list(file_to_the_csv,'rtt')
    detection = cusum.cusum_var(reality)
    #detection = baycpd.baysiancpt(reality)
    fact = csv.csv2list(file_to_the_csv,'cp')
    result = eval.evaluation(fact,detection)
    return result
print(test("rtt_series/11017.csv"))  
    
