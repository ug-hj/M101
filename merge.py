from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc
import math
import seaborn
import matplotlib.cm as cm

def merger(out_filename, *in_files):
	mask1 = hp.read_map(in_files[0])
	C = np.array([1]*len(mask1))
	
	for mask in in_files:
		A = np.array(hp.read_map(mask))
		assert len(A) == len(C), ("nsides mismatched")
		C = C*A

	hp.write_map(out_filename, C)
	hp.mollview(C, cmap=cm.inferno, rot=(180,0,0))

	return None
