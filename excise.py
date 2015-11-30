from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def exscissor(infile, ra_starts, dec_starts, ra_stops, dec_stops, nside):
	assert len(ra_starts) == len(ra_stops) == len(dec_starts) == len(dec_stops), ("stripe coordinate vectors mismatched/missing data")

	# calculate length scale of 1 pixel in radians
	radperpix = ((4*np.pi)/(12*(nside**2))/np.pi)**(0.5)

	# define "galaxy" separation, such that all pixels in ra/dec range are populated
	ra_steps = np.around(1.1*(ra_stops - ra_starts)/radperpix)
	dec_steps = np.around(1.1*(dec_stops - dec_starts)/radperpix)
	steps = np.zeros(len(ra_steps))

	for l in np.arange(len(ra_steps)):
		if ra_steps[l] > dec_steps[l]:
			steps[l] = ra_steps[l]
		else:
			steps[l] = dec_steps[l]
	assert len(steps) == len(ra_starts), ("mismatched vector lengths")

	# create vectors defining areas of stripes
	ra = []
	dec = ra

	# populate vectors with "galaxies"
	for l in np.arange(len(ra_starts)):
		a = np.linspace(ra_starts[l], ra_stops[l], num=steps[l])
		ra = np.concatenate((ra,a))
	for l in np.arange(len(dec_starts)):
		a = np.linspace(dec_starts[l], dec_stops[l], num=steps[l])
		dec = np.concatenate((dec,a))
	assert len(ra) == len(dec), ("mismatched vector lengths")

	# identify pixels corresponding to "galaxies"
	theta = np.deg2rad(90.0 - dec)
	phi = np.deg2rad(ra)
	pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)

	# distribute "galaxies"
	npix = hp.nside2npix(nside)
	excise = np.bincount(pix_IDs, minlength=npix)

	# erase pixels in map
	hmap = hp.read_map(infile)
	hmap1 = hmap
	for l in np.arange(len(excise)):
		if excise[l] != 0.0:
			hmap[l] = 0

	# write new map to file
	# if all(x == hmap1[x] for x in hmap):
	outfilename = infile[:-5] + "_exsc.fits"
	hp.write_map(outfilename, hmap)

	return None

if __name__ == "__main__":
	infile = "/Users/Harry/M101/128_SDSS/SDSS_cmap_128.fits"
	nside = 128
	ra_starts = np.array([122,121,119,111,111.5,110,246,255,268,232])
	ra_stops = np.array([139,126,128,119,117.5,116,251,270,271,240])
	dec_starts = np.array([-1.5,0,4,6,25,32,8.5,20,46,26])
	dec_stops = np.array([-0.5,4,6,25,30,35,13.5,40,49,30])

