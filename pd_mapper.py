from __future__ import division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def mapper1(catalog_dir, nside, ra_col, dec_col, out_dir):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with_header"):
            # read catalog
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', low_memory=False, header=0, dtype={ra_col : np.float64, dec_col : np.float64}, engine=None, usecols=[1,2])
            ra = c.loc["ra"]
            dec = c.loc["dec"]
        
            # generate theta/phi vectors
            theta = np.deg2rad(90.0 - dec)
            phi = np.deg2rad(ra)
        
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
            del ra
            del dec
            gc.collect()

    return None

def main(catalog_dir, nside, ra_col, dec_col, out_dir):
    
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
    mapper1(catalog_dir, nside, ra_col, dec_col, out_dir)

    # merge count maps
    for cmap in listdir(out_dir):
        m = hp.read_map(join(out_dir, cmap))
        hmap += m

	# assign filename & write final map
    out_filename = basename(normpath(catalog_dir)) + "_" + str(nside) + "cmap.fits"
    hp.write_map(join(out_dir, out_filename), hmap)
    
    return None

if __name__ == "__main__":
    catalog_dir = "/share/splinter/ug_hj/test_sdss"
    nside = 128
    ra_col = "ra"
    dec_col = "dec"
    out_dir = "/share/splinter/ug_hj/test_128_SDSS"
    main(catalog_dir, nside, ra_col, dec_col, out_dir)