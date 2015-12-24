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

def mapper1(catalog_dir, nside, ra_col, dec_col, out_dir, sw=None, ew=None, weights=None):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    num_s = 0
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with"):
            # read catalog
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={ra_col : np.float64, dec_col : np.float64}, engine=None, usecols=[1,2,9,10])
            ra = c["ra"]
            dec = c["dec"]
            # ifib2 = c["fiberMag_i"]

            cleancut = c["clean"] == True
            typecut = c["type"] == 6
            totalcut = cleancut & typecut

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
            cmap = np.bincount(pix_IDs, weights=weights, minlength=npix)
            if weights is not None:
                assert len(weights) == len(pix_IDs), ("shape of weights must match shape of ra/dec data")
            assert len(cmap) == npix, ("pixel numbers mismatched")

            # # define empty weight vector
            # w = np.zeros(len(pix_IDs))
            # n_s = np.zeros(len(pix_IDs))

            # # define A, B, n_s
            # A_0 = 4.41
            # A_1 = -0.17
            # B_0 = -1.36*math.exp(-3)
            # B_1 = 6.65*math.exp(-5)

            # A = A_0*ifib2 + A_1
            # B = B_0*ifib2 + B_1 # may need to fix A & B to some min(ifib2)                                              (Anderson2012)

            # # define number of stars in resident pixel of each                       galaxy, len(n_s)=len(ra)
            # # for (star, pixel) in enumerate(pix_IDs):
            # #     n_s[star] = cmap[pixel]

            # # populate w
            # w = A + B*n_s
        
            # sum to hmap
            hmap = cmap
        
            # assign filenames & write to file
            out_filename = "countmap_" + cat[:-4] + ".fits"
            hp.write_map(join(out_dir, out_filename), hmap)

            del c, ra, dec, cleancut, typecut
            gc.collect()
    # print("num_s =", num_s)
    # count = open(join(out_dir, "count.txt"), "w")
    # count.write(str(num_s))
    # count.close() 
    return None

def main(catalog_dir, nside, ra_col, dec_col, out_dir, sw=None, ew=None, weights=None):
    
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
    mapper1(catalog_dir, nside, ra_col, dec_col, out_dir, sw, ew, weights)

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
    nside = 512
    ra_col = "ra"
    dec_col = "dec"
    out_dir = "/share/splinter/ug_hj/M101/SDSS_stellar_density_512"
    sw = None
    ew = None
    weights = None
    main(catalog_dir, nside, ra_col, dec_col, out_dir, sw, ew, weights)
