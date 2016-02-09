from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import gc

def match(out_matches, out_NOmatches, upp, count_file):
    
    num_gal = 0

    root_masterpzc = '/share/splinter/ug_hj/M101/PZ_NOmatches2GAMA_sample.csv'
    root_GAMAcut_cat = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog_sample.csv'
    
    pzc = pandas.read_csv(root_masterpzc, sep=',', header=0, dtype={'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])

    c = pandas.read_csv(root_GAMAcut_cat, sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec'])

    len_pzc = len(pzc) + 1 # for indexing
    intervals = np.arange(start=0, stop=len_pzc, step=len_pzc/10, dtype=np.int64)
    pzc = pzc[intervals[upp-1]:intervals[upp]]

    c_objID = c['objID']
    pzc_objID = pzc['objID']

    objID = [int(oID) for oID in c_objID]
    pzcID_prematch = [int(pzID) for pzID in pzc_objID]

    # match objIDs and photozcatIDs
    snip = np.array([np.where(pzcID_prematch_i in objID, True, False) for pzcID_prematch_i in pzcID_prematch])
    reverse = np.array([not i for i in snip])

    pzc_NOmatch = pzc[reverse]
    pzc = pzc[snip]

    # galaxy count
    num_gal += len(pzc)

    pandas.DataFrame.to_csv(pzc, str(out_matches))
    pandas.DataFrame.to_csv(pzc_NOmatch, str(out_NOmatches))

    print("num_gal =", num_gal)
    count = open(count_file, "w")
    count.write(str(num_gal))
    count.close() 
    return None

if __name__ == "__main__":
    upp = 1
    out_matches = "/share/splinter/ug_hj/M101/SplitMatchRun/PZvGAMA_match" + str(upp) + ".csv"
    out_NOmatches = "/share/splinter/ug_hj/M101/SplitMatchRun/PZvGAMA_NOmatch" + str(upp) + ".csv"
    count_file = "/share/splinter/ug_hj/M101/SplitMatchRun/count" + str(upp) + ".txt"
    match(out_matches, out_NOmatches, upp, count_file)
