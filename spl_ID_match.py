from __future__ import print_function, division	
import numpy as np	
import healpy as hp	
import matplotlib	
import random	
from os.path import join, isdir	
from os import listdir, mkdir	
import pandas	
import gc	
	
def match(in_IDs, in_PZs, out_matches):	
	
    pzc = pandas.read_csv(in_PZs, sep=',', header=0, dtype={'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])
	
    c = pandas.read_csv(in_IDs, sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec'])
	
    match_cat = pandas.merge(c, pzc, on="objID")

    # galaxy count	
    num_gal = len(match_cat)	
	
    match_cat.to_csv(str(out_matches), float_format='%d')
	
    print('num_gal =', num_gal, '  SAVE OUTPUT')
    return None	
	
if __name__ == '__main__':
    in_PZs = '/share/splinter/ug_hj/M101/PZs_sdss_totcat.csv'
    in_IDs = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog.csv'
    out_matches = '/share/splinter/ug_hj/M101/sdssPZvGAMA_matches.csv'
    match(in_IDs, in_PZs, out_matches)
