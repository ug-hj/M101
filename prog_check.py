from __future__ import division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
from astropy.table import Table
import gc

out_dir = "/share/splinter/ug_hj/128_SDSS"
nside = 128

assert hp.isnsideok(nside), ("nside must be a power of 2")
npix = hp.nside2npix(nside)
hmap = np.zeros(hp.nside2npix(nside))

for cmap in listdir(out_dir):
	if cmap.endswith(".fits"):
        m = hp.read_map(join(out_dir, cmap))
        hmap += m

out_filename = str(nside) + "PRELIMcmap.fits"
f = join(out_dir, out_filename)
hp.write_map(f, hmap)
