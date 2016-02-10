from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def mapper1(catalog_dir, nside, out_dir):
    # create empty map
    hmap = np.zeros(hp.nside2npix(nside))
    npix = hp.nside2npix(nside)
    num_gal = 0
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("with"):
            # read catalog
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64, 'modelMag_u' : np.float64, 'modelMag_g' : np.float64, 'modelMag_r' : np.float64, 'modelMag_i' : np.float64, 'modelMag_z' : np.float64, 'extinction_u' : np.float64, 'extinction_g' : np.float64, 'extinction_r' : np.float64, 'extinction_i' : np.float64, 'extinction_z' : np.float64, 'petroMag_r' : np.float64}, engine=None, usecols=['ra', 'dec', 'clean', 'type', 'modelMag_u', 'modelMag_g', 'modelMag_r', 'modelMag_i', 'modelMag_z', 'extinction_u', 'extinction_g', 'extinction_r', 'extinction_i', 'extinction_z', 'petroMag_r'])

            ra = c["ra"]
            dec = c["dec"]

            # correct model/petrosian magnitudes
            u = np.array(c['modelMag_u'] - c['extinction_u'])
            g = np.array(c['modelMag_g'] - c['extinction_g'])
            r = np.array(c['modelMag_r'] - c['extinction_r'])
            i = np.array(c['modelMag_i'] - c['extinction_i'])
            z = np.array(c['modelMag_z'] - c['extinction_z'])
            rPetro = np.array(c["petroMag_r"] - c['extinction_r'])

            # define colour & magnitude cuts
            colour_cut1 = np.where((u-g >= -2) & (u-g <= 7), True, False)
            colour_cut2 = np.where((g-r >= -2) & (g-r <= 7), True, False)
            colour_cut3 = np.where((r-i >= -2) & (r-i <= 7), True, False)
            colour_cut4 = np.where((i-z >= -2) & (i-z <= 7), True, False)
            rPetro_cut = np.where((rPetro >= 12.0) & (rPetro <= 19.4), True, False)
            cleancut = c["clean"] == True
            typecut = c["type"] == 3

            totalcut = cleancut & typecut & rPetro_cut & colour_cut1 & colour_cut2 & colour_cut3 & colour_cut4

            ra = ra[totalcut]
            dec = dec[totalcut]

            # galaxy count
            num_gal += len(ra)

            # generate theta/phi vectors
            theta = np.deg2rad(90.0 - dec)
            phi = np.deg2rad(ra)
        
            # generate corresponding pixel_IDs
            pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
        
            # distribute galaxies according to pixel_ID
            cmap = np.bincount(pix_IDs, minlength=npix)
            assert len(cmap) == npix, ("pixel numbers mismatched")
        
            # sum to hmap
            hmap = cmap
        
            # assign filenames & write to file
            out_filename = "map_" + cat[:-4] + ".fits"
            hp.write_map(join(out_dir, out_filename), hmap)

            del c, ra, dec, cleancut, typecut, rPetro_cut, colour_cut1, colour_cut2, colour_cut3, colour_cut4
            gc.collect()

    print("num_gal =", num_gal)
    count = open(join(out_dir, "count.txt"), "w")
    count.write(str(num_gal))
    count.close() 
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
    out_dir = "/share/splinter/ug_hj/M101/GAMAcuts_256"
    main(catalog_dir, nside, out_dir)
