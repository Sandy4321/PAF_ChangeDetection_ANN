import changedetect as cpt
import numpy as np

#This function is to apply the algorithm of Baysian
def baysiancpt(values):
	detectionIndex = cpt.cpt_np(values)
	detectionBinairy = np.zeros(len(values))
	for p in detectionIndex:
		detectionBinairy[p] = 1
	return detectionBinairy