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

    root_masterpzc = '/share/splinter/ug_hj/M101/PZ_NOmatches2GAMA.csv'
    root_GAMAcut_cat = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog.csv'
    
    pzc = pandas.read_csv(root_masterpzc, sep=',', header=0, dtype={'objID' : np.int32, 'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])

    c = pandas.read_csv(root_GAMAcut_cat, sep=',', header=0, dtype={'objID' : np.int32, 'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec'])

    objID = [int(oID) for oID in c['objID']]
    pzcID_prematch = [int(pzID) for pzID in pzc['objID']]

    # match objIDs and photozcatIDs
    snip = np.array([np.where(pzcID_prematch_i in objID, True, False) for pzcID_prematch_i in pzcID_prematch])
    reverse = np.array([not i for i in snip])

    pzc_NOmatch = pzc[reverse]
    pzc = pzc[snip]

    # galaxy count
    num_gal += len(pzc)

    pandas.DataFrame.to_csv(master_pzc, str(out_matches))
    pandas.DataFrame.to_csv(master_pzcNOmatch, str(out_NOmatches))

    print("num_gal =", num_gal)
    count = open("/share/splinter/ug_hj/M101/matched_pz_count.txt", "w")
    count.write(str(num_gal))
    count.close() 
    return None

if __name__ == "__main__":
    photozcat_dir = "/share/splinter/moraes/photoz_cats/"
    out_matches = "/share/splinter/ug_hj/M101/PZ_matches2GAMA_2.csv"
    out_NOmatches = "/share/splinter/ug_hj/M101/PZ_NOmatches2GAMA_2.csv"
    match(photozcat_dir, out_matches, out_NOmatches)
