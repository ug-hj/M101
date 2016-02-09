from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import gc

def match(out_matches, out_NOmatches, low, upp):
    
    num_gal = 0

    root_masterpzc = '/share/splinter/ug_hj/M101/PZ_NOmatches2GAMA.csv'
    root_GAMAcut_cat = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog.csv'
    
    pzc = pandas.read_csv(root_masterpzc, sep=',', header=0, dtype={'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])

    c = pandas.read_csv(root_GAMAcut_cat, sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec'])

    len_pzc = len(pzc)

    c_objID = c['objID']
    pzc_objID = pzc['objID']

    objID = [int(oID) for oID in c_objID]

    if low is not None:
        pzcID_prematch = [int(pzID) for pzID in pzc_objID[(len_pzc/low):(len_pzc/upp)]]
    else:
        pzcID_prematch = [int(pzID) for pzID in pzc_objID[:(len_pzc/upp)]]

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
    count = open("/share/splinter/ug_hj/M101/SplitMatchRun/count1.txt", "w")
    count.write(str(num_gal))
    count.close() 
    return None

if __name__ == "__main__":
    out_matches = "/share/splinter/ug_hj/M101/SplitMatchRun/PZvGAMA_match1.csv"
    out_NOmatches = "/share/splinter/ug_hj/M101/SplitMatchRun/PZvGAMA_NOmatch1.csv"
    low = None
    upp = 6
    match(out_matches, out_NOmatches, low, upp)
