from __future__ import print_function, division	
import numpy as np	
import healpy as hp	
import matplotlib	
import random	
from os.path import join, isdir	
from os import listdir, mkdir	
import pandas	
import gc	
	
def match(out_matches, out_NOmatches, count_file):	
	
    num_gal = 0	
	
    root_masterpzc = '/share/splinter/ug_hj/M101/PZs_sdss_totcat.csv'	
    root_GAMAcut_cat = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog.csv'	
	
    pzc = pandas.read_csv(root_masterpzc, sep=',', header=0, dtype={'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])

    z = np.array(pzc['z'])
    z_cut = np.where((0 < z) & (z < 0.8), True, False)
    pzc = pzc[z_cut]
	
    c = pandas.read_csv(root_GAMAcut_cat, sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec'])
	
    pzc = pandas.merge(c, pzc, on="objID")

    # galaxy count	
    num_gal += len(pzc)	
	
    pzc.to_csv(str(out_matches))
	
    print('num_gal =', num_gal)	
    count = open(count_file, 'w')	
    count.write(str(num_gal))	
    count.close() 	
    return None	
	
if __name__ == '__main__':
    out_matches = '/share/splinter/ug_hj/M101/PZvGAMA_match.csv'	
    out_NOmatches = '/share/splinter/ug_hj/M101/PZvGAMA_NOmatch.csv'	
    count_file = '/share/splinter/ug_hj/M101/PZvGAMAcount.txt'	
    match(out_matches, out_NOmatches, count_file)	
