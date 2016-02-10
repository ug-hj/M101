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
	sw_cut = np.array([item.startswith('photoz_cat') for item in cat_list])
	cat_list = cat_list[sw_cut]

	pzc1 = pandas.read_csv(join(catalog_dir, cat_list[0]), sep=',', header=1, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'type', 'clean', 'z', 'zErr'])

	c_cut = np.array(pzc1['clean'] == 1)
	t_cut = np.array(pzc1['type'] == 3)
	z = np.array(pzc1['z'])
	z_cut = np.where((0 < z) & (z < 0.8), True, False)
	cuts = c_cut & t_cut & z_cut

	pzc1 = pzc1[cuts]

	del cuts, c_cut, t_cut, z_cut
	gc.collect()

	for cat in cat_list[1:]:

		pzc = pandas.read_csv(join(catalog_dir, cat), sep=',', header=1, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'type', 'clean', 'z', 'zErr'])

		c_cut = np.array(pzc['clean'] == 1)
		t_cut = np.array(pzc['type'] == 3)
		z = np.array(pzc['z'])
		z_cut = np.where((0 < z) & (z < 0.8), True, False)
		cuts = c_cut & t_cut & z_cut

		pzc = pzc[cuts]

		pzc1 =  pzc1.append(pzc) #pandas.concat([pzc1, pzc])

		del pzc, cuts, c_cut, t_cut, z_cut
		gc.collect()

	pzc1.to_csv(str(out_csv))

	print('num_gal =', len(pzc1))

	return None

if __name__ == '__main__':
	catalog_dir = '/share/splinter/moraes/photoz_cats/'
	out_csv = '/share/splinter/ug_hj/M101/PZs_sdss_totcat.csv'
	concatenate(catalog_dir, out_csv)
