from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import gc

def match(photozcat_dir, out_matches, out_NOmatches):
    
    num_gal = 0

    root_masterpzc = '/share/splinter/ug_hj/M101/photoz_headers.csv'
    root_GAMAcut_cat = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog.csv'

    save_pzcats_dir = '/share/splinter/ug_hj/M101/Photoz_cats'
    
    master_pzc = pandas.read_csv(root_masterpzc, sep=',', header=0, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])
    master_pzcNOmatch = master_pzc

    c = pandas.read_csv(root_GAMAcut_cat, sep=',', header=0, dtype={'objID' : np.int64, 'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec'])

    objID = c['objID']
    
    for pzcat in listdir(photozcat_dir):
        if pzcat.endswith(".csv") and pzcat.startswith('photoz'):
            # read photo_z catalog
            pzc = pandas.read_csv(join(photozcat_dir, pzcat), sep=',', header=1, dtype={'objID' : np.int64, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'type', 'clean', 'z', 'zErr'])

            # define cuts
            pzc_type = pzc['type'] == 3
            pzc_clean = pzc['clean'] == 1
            pzc_bad_z = np.where((pzc['z'] > 0) & (pzc['z'] < 0.8), True, False)
            pzc_large_zErr = np.where((pzc['zErr'] < pzc['z']), True, False)
            pzc_cut = pzc_type & pzc_clean & pzc_bad_z & pzc_large_zErr

            pzcID_prematch = pzc['objID']

            # cut data for type/clean
            pzcID_prematch = pzcID_prematch[pzc_cut]
            pzc = pzc[pzc_cut]

            pandas.DataFrame.to_csv(pzc, join(save_pzcats_dir, str(pzcat)))

            pzc = pzc[['objID', 'z', 'zErr']]

            # match objIDs and photozcatIDs
            snip = np.array([np.where(pzcID_prematch_i in objID, True, False) for pzcID_prematch_i in pzcID_prematch])
            reverse = np.array([not i for i in snip])

            pzc_NOmatch = pzc[reverse]
            pzc = pzc[snip]

            # galaxy count
            num_gal += len(pzc)

            # generate theta/phi vectors                        -----> GET CATALOGS FIRST
            # theta_preslice = np.deg2rad(90.0 - dec)
            # phi_preslice = np.deg2rad(ra)

            # # define slices
            # slice1 = np.where((0.2 <= photo_z) & (photo_z < 0.3), True, False)
            # slice2 = np.where((0.3 <= photo_z) & (photo_z < 0.4), True, False)
            # slice3 = np.where((0.4 <= photo_z) & (photo_z < 0.5), True, False)
            # slice4 = np.where((0.5 <= photo_z) & (photo_z < 0.6), True, False)
            # slices = [slice1, slice2, slice3, slice4]
        
            # for i, z_slice in enumerate(slices):
            #     # generate corresponding pixel_IDs
            #     theta = theta_preslice[z_slice]
            #     phi = phi_preslice[z_slice]
            #     pix_IDs = hp.ang2pix(nside, theta, phi, nest=False)
            
            #     # distribute galaxies according to pixel_ID
            #     cmap = np.bincount(pix_IDs, minlength=npix)
            #     assert len(cmap) == npix, ("pixel numbers mismatched")
            
            #     # assign filenames & write to file
            #     out_filename = pzcat[:-4] + '_' + cat[:-4] + ".fits"
            #     slice_dir = 'slice' + str((i+1))
            #     out_file = join(slice_dir, out_filename)
            #     hp.write_map(join(out_dir, out_file), cmap)

            #     del theta, phi, cmap
            #     gc.collect()

            # del c, ra, dec, objID, pzcID
            # gc.collect()

            master_pzc = pandas.concat([master_pzc, pzc])
            master_pzcNOmatch = pandas.concat([master_pzcNOmatch, pzc_NOmatch])

        del pzc, pzc_NOmatch, pzc_clean, pzc_type, pzc_bad_z, pzc_large_zErr, pzcID_prematch, snip, reverse
        gc.collect()

    pandas.DataFrame.to_csv(master_pzc, str(out_matches))
    pandas.DataFrame.to_csv(master_pzcNOmatch, str(out_NOmatches))

    print("num_gal =", num_gal)
    count = open("/share/splinter/ug_hj/M101/matched_pz_count.txt", "w")
    count.write(str(num_gal))
    count.close() 
    return None

# def main(catalog_dir, photozcat_dir, nside, out_dir):
    
#     # define map resolution, create map of zeros
#     assert hp.isnsideok(nside), ("nside must be a power of 2")
#     npix = hp.nside2npix(nside)
#     hmap = np.zeros(npix)
    
#     # create destination directories
#     if not isdir(out_dir):
#         mkdir(out_dir)
#     # else:
#     # 	assert listdir(out_dir) == [], ("out_dir already exists/has content, choose a new destination directory")

#     sub_dirs = ['slice1', 'slice2', 'slice3', 'slice4']
#     for sub_dir in sub_dirs:
#         if not isdir(join(out_dir, sub_dir)):
#             mkdir(join(out_dir, sub_dir))
    
#     # create count maps
#     mapper(catalog_dir, photozcat_dir, nside, out_dir)

#     # merge count maps                                      <------ ADAPT TO MERGE AFTER RUN
#     # for z_bin in listdir(out_dir):
#     #     if not z_bin.endswith('.txt'):
#     #         fileroot = join(out_dir, z_bin)
#     #         for cmap in listdir(join(out_dir, z_bin)):
#     #             if cmap.endswith(".fits"):
#     #                 m = hp.read_map(join(fileroot, cmap))
#     #                 hmap += m

#     #     	# assign filename & write final map
#     #         if not all(x == 0 for x in hmap):
#     #             out_file = "totalmap.fits"
#     #             hp.write_map(join(fileroot, out_file), hmap)
#     #         else:
#     #             print("empty map")

#     return None

if __name__ == "__main__":
    photozcat_dir = "/share/splinter/moraes/photoz_cats/"
    out_matches = "/share/splinter/ug_hj/M101/PZ_matches2GAMA.csv"
    out_NOmatches = "/share/splinter/ug_hj/M101/PZ_NOmatches2GAMA.csv"
    match(photozcat_dir, out_matches, out_NOmatches)
