from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def striper(catalog_dir, ra_col, dec_col, outimg):
	for cat in listdir(catalog_dir):
		if cat.endswith(".csv") and cat.startswith("with_header"):
			# read catalog
			c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={ra_col : np.float64, dec_col : np.float64}, engine=None, usecols=[1, 2, 311])
			ra = c[ra_col]
			dec = c[dec_col]
			stripe = c["stripe"]

			# plot ra vs dec w/ colour scale according to stripes
			plt.scatter(ra, dec, c=stripe)

			# define new stripe vector with no repeated values
			#stripe1 = np.zeros(len(stripe))
			#for x in np.arange(len(stripe)):
			#	if not stripe[x] in stripe1:
			#		stripe1[x] = stripe[x]

			# annotate points on scatter with stripe numbers
			#for l in np.arange(len(ra)):
			#	if stripe1[l] != 0:
			#		plt.annotate(s=str(int(stripe1[l])), xy=(str(ra[l]), str(dec[l])))

			del c
			del ra
			del dec
			del stripe
			#del stripe1
			gc.collect()
	plt.colorbar()
	plt.savefig(outimg)
	return None

if __name__ == '__main__':
	catalog_dir = '/share/data1/SDSS_DR12_Photometry'
	ra_col = 'ra'
	dec_col = 'dec'
	outimg = '/share/splinter/ug_hj/M101/SDSS_ra_vs_dec_wstripes.png'
	striper(catalog_dir, ra_col, dec_col, outimg)