from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import gc

def mapper(catalog, nside, out_dir, slice_intervals):
    npix = hp.nside2npix(nside)

    # read in catalog
    c = pandas.read_csv(catalog, sep=',', header=0, dtype={'objID' : np.int64, 'ra' : np.float64, 'dec' : np.float64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec', 'z', 'zErr'])

    photo_z = c['z']
    ra = c['ra']
    dec = c['dec']

    # generate theta/phi vectors
    theta_preslice = np.deg2rad(90.0 - dec)
    phi_preslice = np.deg2rad(ra)

    # define slices
    slices = []

    for cut in slice_intervals:
        z_slice = np.where((cut[0] <= photo_z) & (photo_z <= cut[1]), True, False)
        slices.append(z_slice)

    for i, zslice in enumerate(slices):
        # generate corresponding pixel_IDs
        theta = theta_preslice[zslice]
        phi = phi_preslice[zslice]
        pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
    
        # distribute galaxies according to pixel_ID
        cmap = np.bincount(pix_IDs, minlength=npix)
        assert len(cmap) == npix, ("pixel numbers mismatched")
    
        # assign filenames & write to file
        out_filename = str((i+1)) + '_map.fits'
        hp.write_map(join(out_dir, out_filename), cmap)

        # report slice counts
        count = "slice" + str(i+1) + " # galaxies = " + str(len(theta))

        print(count)

        del theta, phi, cmap, count
        gc.collect()

    return None

def main(catalog, nside, out_dir, slice_intervals):
        
    # create destination directories
    if not isdir(out_dir):
        mkdir(out_dir)

    mapper(catalog, nside, out_dir, slice_intervals)
    
    return None

if __name__ == "__main__":
    catalog = "/share/splinter/ug_hj/M101/sdssPZvGAMA_matches_1.csv"
    nside = 256
    out_dir = '/share/splinter/ug_hj/M101/GAMA_SDSSpz_slices_1'
    slice_intervals = [[0.05, 0.10], [0.10, 0.15], [0.15, 0.20], [0.20, 0.25],
                         [0.25, 0.30], [0.30, 0.35], [0.35, 0.40]]
    main(catalog, nside, out_dir, slice_intervals)
