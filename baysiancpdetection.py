import changedetect as cpt
import numpy as np

#This function is to apply the algorithm of Baysian
def cpt(values):
	detectionIndex = cpt.cpt_np(y)
	detectionBinairy = np.zeros(len(values))
	for p in detectionIndex:
		detectionBinairy[p] = 1
	return detectionBinairy