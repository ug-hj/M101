from __future__ import division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
from astropy.table import Table
import gc

def mapper1(catalog_dir, nside, out_dir):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    
    for cat in listdir(catalog_dir)[0:1]:
        if cat.endswith(".csv"):
            # read catalog
            try:
            	c = Table.read(join(catalog_dir, cat), format='ascii', delimiter=',')
            except:
            	pass
            
            # generate theta/phi vectors
            try:
            	theta = np.deg2rad(90.0 - c[:,2])
            	phi = np.deg2rad(c[:,1])
            
            	# generate corresponding pixel_IDs
            	pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
            
            	# distribute galaxies according to pixel_ID, weights deal with potential systematics
            	cmap = np.bincount(pix_IDs, weights=None, minlength=npix)
            	assert len(cmap) == npix, ("pixel numbers mismatched")
            
            	# sum to hmap
            	hmap = cmap
            
            	# assign filenames & write to file
            	out_filename = "countmap_" + cat[:-4] + ".fits"
            	hp.write_map(join(out_dir, out_filename), hmap)

            	del c
            	gc.collect()
            except NameError:
            	pass
                
    return None

def main(catalog_dir, nside, out_dir):
    
    # check catalog_dir is a string
    assert isinstance(catalog_dir, basestring) == True, ("catalog_dir must be input as a string")
    
    # define map resolution, create map of zeros
    assert hp.isnsideok(nside), ("nside must be a power of 2")
    npix = hp.nside2npix(nside)
    hmap = np.zeros(hp.nside2npix(nside))
    
    # create destination directory
    assert isinstance(out_dir, basestring) == True, ("out_dir must be input as a string")
    if not isdir(out_dir):
        mkdir(out_dir)
    else:
    	assert listdir(out_dir) == [], ("out_dir already exists/has content, choose a new destination directory")
    
    # create count maps
    mapper1(catalog_dir, nside, out_dir)

    # merge count maps
    for cmap in listdir(out_dir):
        m = hp.read_map(join(out_dir, cmap))
        hmap += m

	# assign filename & write final map
    out_filename = basename(normpath(catalog_dir)) + "_" + str(nside) + "cmap.fits"
    hp.write_map(join(out_dir, out_filename), hmap)
    
    return None

if __name__ == "__main__":
    catalog_dir = "/share/data1/SDSS_DR12_Photometry"
    nside = 128
    out_dir = "/share/splinter/ug_hj/128_SDSS"
    main(catalog_dir, nside, out_dir)