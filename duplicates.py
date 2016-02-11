from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import gc

def ratios(catalog_dir):

	cat_list = np.array(listdir(catalog_dir))
	sw_cut = np.array([item.startswith('photoz_cat') for item in cat_list])
	cat_list = cat_list[sw_cut]

	ratios = []

	for cat in cat_list[1:]:

		pzc = pandas.read_csv(join(catalog_dir, cat), sep=',', header=1, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'type', 'clean', 'z', 'zErr'])

		ID = pzc['objID']
		unique = np.unique(ID)

		if len(ID) != 0:
			ratio = len(unique)/len(ID)

			ratios.append(ratio)
			del ratio

		del pzc
		gc.collect()

	print('ratio spread =', np.unique(ratios))

	return None

if __name__ == '__main__':
	catalog_dir = '/share/splinter/moraes/photoz_cats/'
	ratios(catalog_dir)
