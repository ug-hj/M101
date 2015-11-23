from __future__ import division
import numpy as np
import healpy as hp
import matplotlib
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import random
import gc

nside = 128
hmap = np.zeros(hp.nside2npix(nside))
npix = hp.nside2npix(nside)

# read catalog
c = pandas.read_csv(join("/share/data1/SDSS_DR12_Photometry", random.choice(listdir("/share/data1/SDSS_DR12_Photometry")), sep=',', low_memory=False, skip_blank_lines=False, header=0, dtype={'ra' : np.float64, 'dec' : np.float64})
ra = c.iloc[:, 1]
dec = c.iloc[:, 2]

# generate theta/phi vectors
theta = np.deg2rad(90.0 - dec)
phi = np.deg2rad(ra)

# generate corresponding pixel_IDs
pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)

# distribute galaxies according to pixel_ID, weights deal with potential systematics
cmap = np.bincount(pix_IDs, weights=None, minlength=npix)
assert len(cmap) == npix, ("pixel numbers mismatched")

# sum to hmap
hmap += cmap

del c
gc.collect()

hp.write_map("/share/splinter/ug_hj/pd_testmap", hmap)