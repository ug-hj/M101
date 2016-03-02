from __future__ import print_function, division	
import numpy as np	
import healpy as hp	
import matplotlib	
import random	
from os.path import join, isdir	
from os import listdir, mkdir
import os	
import pandas	
import gc

def sort(dir, limit, new_dir):
	
	if not isdir(new_dir):
		mkdir(new_dir)

	dir_list = listdir(dir)
	sort_cut = np.array([('o126' in item) for item in dir_list])
	dir_list = dir_list[sort_cut]

	for qsub in dir_list:
		if (int(qsub[-7:]) > limit):
			os.system("mv " + join(dir, qsub) + " " + new_dir)

	return None

if __name__ == "__main__":
	dir = '/share/splinter/ug_hj/M101/'
	limit = 1264771
	new_dir = '/share/splinter/ug_hj/M101/Mask3_Cl_outputs'
	sort(dir, limit, new_dir)
	