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
    c = pandas.read_csv(catalog, sep=',', header=0, dtype={'objID' : np.int64, 'ra' : np.float64, 'dec' : np.float64, 'z' : np.float64, 'ANNZ_best' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec', 'z', 'ANNZ_best'])

    photo_z = c['z']
    ANNz = c['ANNZ_best']
    ra = c['ra']
    dec = c['dec']

    # generate theta/phi vectors
    theta_preslice = np.deg2rad(90.0 - dec)
    phi_preslice = np.deg2rad(ra)

    # define slices
    z_slices = []
    ANNz_slices = []

    for cut in slice_intervals:
        z_slice = np.where((cut[0] <= photo_z) & (photo_z <= cut[1]), True, False)
        ANNz_slice = np.where((cut[0] <= ANNz) & (ANNz <= cut[1]), True, False)
        z_slices.append(z_slice)
        ANNz_slices.append(ANNz_slice)

    sdssPZ_dir = join(Slices, "sdssPZ")
    if not isdir(sdssPZ_dir):
        mkdir(sdssPZ_dir)

    for i, zslice in enumerate(z_slices):
        # generate corresponding pixel_IDs
        theta = theta_preslice[zslice]
        phi = phi_preslice[zslice]
        pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
    
        # distribute galaxies according to pixel_ID
        cmap = np.bincount(pix_IDs, minlength=npix)
        assert len(cmap) == npix, ("pixel numbers mismatched")
    
        # assign filenames & write to file
        out_filename = str((i+1)) + '_map.fits'
        hp.write_map(join(sdssPZ_dir, out_filename), cmap)

        # report slice counts
        count = "z_slice" + str(i+1) + " # galaxies = " + str(len(theta))

        print(count)

        del theta, phi, cmap, count
        gc.collect()

    ANNz_dir = join(Slices, "ANNz")
    if not isdir(ANNz_dir):
        mkdir(ANNz_dir)

    for i, ANNzslice in enumerate(ANNz_slices):
        # generate corresponding pixel_IDs
        theta = theta_preslice[ANNzslice]
        phi = phi_preslice[ANNzslice]
        pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
    
        # distribute galaxies according to pixel_ID
        cmap = np.bincount(pix_IDs, minlength=npix)
        assert len(cmap) == npix, ("pixel numbers mismatched")
    
        # assign filenames & write to file
        out_filename = str((i+1)) + '_map.fits'
        hp.write_map(join(ANNz_dir, out_filename), cmap)

        # report slice counts
        count = "ANNz_slice" + str(i+1) + " # galaxies = " + str(len(theta))

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
    catalog = "/share/splinter/ug_hj/M101/SDSS_GAMA_photozs_merged.csv"
    nside = 256
    out_dir = '/share/splinter/ug_hj/M101/Slices'
    slice_intervals = [[0.05, 0.10], [0.10, 0.15], [0.15, 0.20], [0.20, 0.25],
                         [0.25, 0.30], [0.30, 0.35], [0.35, 0.40]]
    main(catalog, nside, out_dir, slice_intervals)
