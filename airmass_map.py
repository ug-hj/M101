from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def airmass_mapper(catalog_dir, nside, out_map):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    pix_airmass = np.zeros(npix) # [0]*npix
    pix_totalcounts = np.zeros(npix) # [0]*npix
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with"):
            # read catalog, cols [ra,dec,airmass_i]
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64, "airmass_i" : np.float64}, engine=None, usecols=[1,2,297])
            ra = c["ra"]
            dec = c["dec"]
            airmass = np.array(c["airmass_i"])

            # generate object pixel_IDs & pixel_counts
            theta = np.deg2rad(90.0 - dec)
            phi = np.deg2rad(ra)
            pix_IDs = np.array(hp.ang2pix(nside, theta, phi, nest=False))
            pix_counts = np.bincount(pix_IDs, minlength=npix)
            assert len(pix_counts) == npix, ("pixel numbers mismatched")

            # calculate "total" airmass in each pixel
            for (i, pix) in enumerate(pix_IDs):
                pix_airmass[pix] += airmass[i]
                pix_totalcounts[pix] += 1

            # TRYING ARRAY INDEXING - IS THE SAME???    
            # pix_airmass[pix_IDs] += airmass
            # pix_totalcounts += pix_counts

            del c, ra, dec, airmass, pix_counts, pix_IDs
            gc.collect()

    pix_avg_airmass = pix_airmass/pix_totalcounts

    # map airmass
    hp.write_map(out_map, pix_avg_airmass) # CHANGE FILENAMES??

if __name__ == "__main__":
    catalog_dir = "/share/data1/SDSS_DR12_Photometry"
    nside = 256
    out_map = "/share/splinter/ug_hj/M101/ai_airmass.fits"
    airmass_mapper(catalog_dir, nside, out_map)
