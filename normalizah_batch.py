from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def normalise(map_dir):

	map_list = np.array(listdir(map_dir))
	ew_cut = np.array([item.endswith('map.fits') for item in map_list]) # EDIT CUTS 
	map_list = map_list[ew_cut]

	for slice_map in map_list:
		count_map = hp.read_map(join(map_dir, slice_map))

		nonzero = count_map != 0
		cut = count_map[nonzero]
		mean = np.mean(cut)

		overdensity_map = np.array(count_map)/mean

		out_name = "Ovr_" + slice_map
		out_file = join(map_dir, out_name)
		hp.write_map(out_file, overdensity_map)

	print('mean =', str(mean))

	return None

if __name__ == '__main__':
	map_dir = "/share/splinter/ug_hj/M101/Slices/sdssPZ/"
	normalise(map_dir)
