from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def mapper1(catalog, nside, out_map):
    # create empty map
    npix = hp.nside2npix(nside)

    # read catalog
    c = pandas.read_csv(catalog, sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['ra', 'dec'])

    ra = c["ra"]
    dec = c["dec"]

    # galaxy count
    num_gal = len(ra)

    # generate theta/phi vectors
    theta = np.deg2rad(90.0 - dec)
    phi = np.deg2rad(ra)

    # generate corresponding pixel_IDs
    pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)

    # distribute galaxies according to pixel_ID
    cmap = np.bincount(pix_IDs, minlength=npix)
    assert len(cmap) == npix, ("pixel numbers mismatched")

    # write to file
    hp.write_map(out_map, cmap)

    print("num_gal =", num_gal)
    return None

if __name__ == "__main__":
    catalog = "/share/splinter/ug_hj/M101/SDSS_GAMA_photozs_merged.csv"
    nside = 2048
    out_map = "/share/splinter/ug_hj/M101/2048_map.fits"
    mapper1(catalog, nside, out_map)
