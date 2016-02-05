from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import gc

def mapper(catalog_dir, photozcat_dir, nside, out_dir, start, end):
    # create empty map
    npix = hp.nside2npix(nside)
    num_gal = 0
    
    for pzcat in listdir(photozcat_dir)[start:end]:
        if pzcat.endswith(".csv") and pzcat.startswith('photoz'):
            # read photo_z catalog
            pzc = pandas.read_csv(join(photozcat_dir, pzcat), sep=',', header=1, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'type', 'clean', 'z', 'zErr'])

            # define cuts
            pzc_type = pzc['type'] == 3
            pzc_clean = pzc['clean'] == 1
            pzc_bad_z = pzc['z'] > 0
            pzc_cut = pzc_type & pzc_clean & pzc_bad_z

            photo_z_prematch = pzc["z"] # INCLUDE ERRORS WHERE?
            pzcID_prematch = pzc['objID']

            # cut data for type/clean
            photo_z_prematch = photo_z_prematch[pzc_cut]
            pzcID_prematch = pzcID_prematch[pzc_cut]

            for cat in listdir(catalog_dir):
                if cat.endswith(".csv") and cat.startswith('with'):
                
                    # read catalog
                    c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64, 'modelMag_u' : np.float64, 'modelMag_g' : np.float64, 'modelMag_r' : np.float64, 'modelMag_i' : np.float64, 'modelMag_z' : np.float64, 'extinction_u' : np.float64, 'extinction_g' : np.float64, 'extinction_r' : np.float64, 'extinction_i' : np.float64, 'extinction_z' : np.float64, 'petroMag_r' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec', 'clean', 'type', 'modelMag_u', 'modelMag_g', 'modelMag_r', 'modelMag_i', 'modelMag_z', 'extinction_u', 'extinction_g', 'extinction_r', 'extinction_i', 'extinction_z', 'petroMag_r'])

                    objID = c['objID']
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

                    pre_cut = cleancut & typecut & rPetro_cut & colour_cut1 & colour_cut2 & colour_cut3 & colour_cut4

                    ra = ra[pre_cut]
                    dec = dec[pre_cut]
                    objID = objID[pre_cut]

                    # match objIDs and photozcatIDs
                    match1 = [ID in pzcID_prematch for ID in objID]
                    objID = objID[match1]
                    ra = ra[match1]
                    dec = dec[match1]

                    match2 = [ID in objID for ID in pzcID_prematch]
                    pzcID = pzcID_prematch[match2]
                    photo_z = np.array(photo_z_prematch[match2])

                    assert len(objID) == len(pzcID), ("object IDs and photo_z's mismatched")

                    # galaxy count
                    num_gal += len(ra)

                    # generate theta/phi vectors
                    theta_preslice = np.deg2rad(90.0 - dec)
                    phi_preslice = np.deg2rad(ra)

                    # define slices
                    slice1 = np.where((0.2 <= photo_z) & (photo_z < 0.3), True, False)
                    slice2 = np.where((0.3 <= photo_z) & (photo_z < 0.4), True, False)
                    slice3 = np.where((0.4 <= photo_z) & (photo_z < 0.5), True, False)
                    slice4 = np.where((0.5 <= photo_z) & (photo_z < 0.6), True, False)
                    slices = [slice1, slice2, slice3, slice4]
                
                    for i, z_slice in enumerate(slices):
                        # generate corresponding pixel_IDs
                        theta = theta_preslice[z_slice]
                        phi = phi_preslice[z_slice]
                        pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
                    
                        # distribute galaxies according to pixel_ID
                        cmap = np.bincount(pix_IDs, minlength=npix)
                        assert len(cmap) == npix, ("pixel numbers mismatched")
                    
                        # assign filenames & write to file
                        out_filename = pzcat[:-4] + '_' + cat[:-4] + ".fits"
                        slice_dir = 'slice' + str((i+1))
                        out_file = join(slice_dir, out_filename)
                        hp.write_map(join(out_dir, out_file), cmap)

                        del theta, phi, cmap
                        gc.collect()

                    del c, ra, dec, objID, pzcID, cleancut, typecut, rPetro_cut, colour_cut1, colour_cut2, colour_cut3, colour_cut4, match1, match2, slice1, slice2, slice3, slice4
                    gc.collect()

        del pzc_clean, pzc_type, pzc_bad_z, photo_z_prematch, pzcID_prematch
        gc.collect()

    print("num_gal =", num_gal)
    count = open(join(out_dir, "count.txt"), "w")
    count.write(str(num_gal))
    count.close() 
    return None

def main(catalog_dir, photozcat_dir, nside, out_dir, start, end):
    
    # define map resolution, create map of zeros
    assert hp.isnsideok(nside), ("nside must be a power of 2")
    npix = hp.nside2npix(nside)
    hmap = np.zeros(npix)
    
    # create destination directories
    if not isdir(out_dir):
        mkdir(out_dir)
    # else:
    # 	assert listdir(out_dir) == [], ("out_dir already exists/has content, choose a new destination directory")

    sub_dirs = ['slice1', 'slice2', 'slice3', 'slice4']
    for sub_dir in sub_dirs:
        if not isdir(join(out_dir, sub_dir)):
            mkdir(join(out_dir, sub_dir))
    
    # create count maps
    mapper(catalog_dir, photozcat_dir, nside, out_dir, start, end)

    # merge count maps                                      <------ ADAPT TO MERGE AFTER RUN
    # for z_bin in listdir(out_dir):
    #     if not z_bin.endswith('.txt'):
    #         fileroot = join(out_dir, z_bin)
    #         for cmap in listdir(join(out_dir, z_bin)):
    #             if cmap.endswith(".fits"):
    #                 m = hp.read_map(join(fileroot, cmap))
    #                 hmap += m

    #     	# assign filename & write final map
    #         if not all(x == 0 for x in hmap):
    #             out_file = "totalmap.fits"
    #             hp.write_map(join(fileroot, out_file), hmap)
    #         else:
    #             print("empty map")

    return None

if __name__ == "__main__":
    catalog_dir = "/share/data1/SDSS_DR12_Photometry"
    photozcat_dir = "/share/splinter/moraes/photoz_cats/"
    nside = 256
    out_dir = "/share/splinter/ug_hj/M101/Photoz_sliced"
    main(catalog_dir, photozcat_dir, nside, out_dir, start, end)
