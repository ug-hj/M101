from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import gc

def concatenate(catalog_dir, out_csv):

	cat_list = np.array(listdir(catalog_dir))
	sw_cut = np.array([item.startswith('PZvGAMA_m') for item in cat_list])
	cat_list = cat_list[sw_cut]

	pzc1 = pandas.read_csv(join(catalog_dir, cat_list[0]), sep=',', header=0, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])

	for cat in cat_list[1:]:

		pzc = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])

		pzc1 =  pzc1.append(pzc) #pandas.concat([pzc1, pzc])

		del pzc
		gc.collect()

	pzc1.to_csv(str(out_csv))

	print('num_gal =', len(pzc1))

	return None

if __name__ == '__main__':
	catalog_dir = '/share/splinter/ug_hj/M101/SplitMatchRun/'
	out_csv = '/share/splinter/ug_hj/M101/GAMAMatched_PZs.csv'