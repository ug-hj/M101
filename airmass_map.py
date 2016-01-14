from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def see_mapper(catalog_dir, nside, out_map):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    pix_airmass = [0]*npix
    pix_totalcounts = [0]*npix
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with"):
            # read catalog, cols [ra,dec,airmass_i]
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64, "airmass_i" : np.float64}, engine=None, usecols=[1,2,297])
            ra = c["ra"]
            dec = c["dec"]
            airmass = c["airmass_i"]

            # generate object pixel_IDs & pixel_counts
            theta = np.deg2rad(90.0 - dec)
            phi = np.deg2rad(ra)
            pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
            pix_counts = np.bincount(pix_IDs, minlength=npix)
            assert len(pix_counts) == npix, ("pixel numbers mismatched")

            # sum to total counts
            pix_totalcounts += pix_counts

            # calculate "total" airmass in each pixel
            for (i, pix) in enumerate(pix_IDs):
                pix_airmass[pix] += airmass[i]

            del c, ra, dec, airmass, pix_counts
            gc.collect()

    pix_avg_airmass = np.array(pix_airmass)/np.array(pix_totalcounts)

    # map airmass
    hp.write_map(out_map, pix_avg_airmass)

if __name__ == "__main__":
    catalog_dir = "/share/data1/SDSS_DR12_Photometry"
    nside = 512
    out_map = "/share/splinter/ug_hj/M101/airmass_map512.fits"
    see_mapper(catalog_dir, nside, out_map)
