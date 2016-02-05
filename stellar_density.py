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

def mapper1(catalog_dir, nside, out_dir):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    num_s = 0
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with"):
            # read catalog
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64, 'modelMag_i' : np.float64, 'modelMag_r' : np.float64, 'extinction_i' : np.float64, 'extinction_r' : np.float64}, engine=None, usecols=['ra', 'dec', 'clean', 'type', 'modelMag_i', 'modelMag_r', 'extinction_i'. 'extinction_r'])
            ra = c["ra"]
            dec = c["dec"]
            i = np.array(c["modelMag_i"] - c["extinction_i"])
            r = np.array(c["modelMag_r"] - c["extinction_r"])

            r_cut = np.where((r > 18.0) & (r < 18.5), True, False)
            i_cut = i < 21.3
            cleancut = c["clean"] == True
            typecut = c["type"] == 6
            totalcut = cleancut & typecut & r_cut & i_cut

            ra = ra[totalcut]
            dec = dec[totalcut]
            # ifib2 = np.array(ifib2[totalcut])

            # star count
            num_s += len(ra)

            # generate theta/phi vectors
            theta = np.deg2rad(90.0 - dec)
            phi = np.deg2rad(ra)
        
            # generate corresponding pixel_IDs
            pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)

            # distribute stars according to pixel_ID
            cmap = np.bincount(pix_IDs, minlength=npix)
            assert len(cmap) == npix, ("pixel numbers mismatched")
        
            # sum to hmap
            hmap = cmap
        
            # assign filenames & write to file
            out_filename = "countmap_" + cat[:-4] + ".fits"
            hp.write_map(join(out_dir, out_filename), hmap)

            del c, ra, dec, cleancut, typecut, r_cut, i_cut
            gc.collect()
    # print("num_s =", num_s)
    # count = open(join(out_dir, "count.txt"), "w")
    # count.write(str(num_s))
    # count.close() 
    return None

def main(catalog_dir, nside, out_dir):
    
    # define map resolution, create map of zeros
    assert hp.isnsideok(nside), ("nside must be a power of 2")
    npix = hp.nside2npix(nside)
    hmap = np.zeros(npix)
    
    # create destination directory
    if not isdir(out_dir):
        mkdir(out_dir)
    else:
    	assert listdir(out_dir) == [], ("out_dir already exists/has content, choose a new destination directory")
    
    # create count maps
    mapper1(catalog_dir, nside, out_dir)

    # merge count maps
    for cmap in listdir(out_dir):
        if cmap.endswith(".fits"):
            m = hp.read_map(join(out_dir, cmap))
            hmap += m

	# assign filename & write final map
    if not all(x == 0 for x in hmap):
        out_filename = basename(normpath(catalog_dir)) + "_" + str(nside) + "cmap.fits"
        hp.write_map(join(out_dir, out_filename), hmap)
    else:
        print("empty map")

    return None

if __name__ == "__main__":
    catalog_dir = "/share/data1/SDSS_DR12_Photometry"
    nside = 256
    out_dir = "/share/splinter/ug_hj/M101/stell_dens_withcuts"
    main(catalog_dir, nside, out_dir)
