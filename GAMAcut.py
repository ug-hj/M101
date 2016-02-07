from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc

def cut(catalog_dir, out_cat):
    for x in np.arange(len(listdir(catalog_dir))):
        x_cat = listdir(catalog_dir)[x]
        if x_cat.endswith('.csv') and x_cat.startswith('SDSS'):
            master_cat = pandas.read_csv(join(catalog_dir, listdir(catalog_dir)[x]), sep=',', header=0, dtype={'objID' : np.int64, 'ra' : np.float64, 'dec' : np.float64, 'modelMag_u' : np.float64, 'modelMag_g' : np.float64, 'modelMag_r' : np.float64, 'modelMag_i' : np.float64, 'modelMag_z' : np.float64, 'extinction_u' : np.float64, 'extinction_g' : np.float64, 'extinction_r' : np.float64, 'extinction_i' : np.float64, 'extinction_z' : np.float64, 'petroMag_r' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec', 'clean', 'type', 'modelMag_u', 'modelMag_g', 'modelMag_r', 'modelMag_i', 'modelMag_z', 'extinction_u', 'extinction_g', 'extinction_r', 'extinction_i', 'extinction_z', 'petroMag_r'], nrows=0)
        if 'master_cat' in globals():
            break
    
    for cat in listdir(catalog_dir):
        if cat.endswith(".csv") and cat.startswith("SDSS"):
            # read catalog
            c = pandas.read_csv(join(catalog_dir, cat), sep=',', header=0, dtype={'objID' : np.int64, 'ra' : np.float64, 'dec' : np.float64, 'modelMag_u' : np.float64, 'modelMag_g' : np.float64, 'modelMag_r' : np.float64, 'modelMag_i' : np.float64, 'modelMag_z' : np.float64, 'extinction_u' : np.float64, 'extinction_g' : np.float64, 'extinction_r' : np.float64, 'extinction_i' : np.float64, 'extinction_z' : np.float64, 'petroMag_r' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec', 'clean', 'type', 'modelMag_u', 'modelMag_g', 'modelMag_r', 'modelMag_i', 'modelMag_z', 'extinction_u', 'extinction_g', 'extinction_r', 'extinction_i', 'extinction_z', 'petroMag_r'])

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
            colour_cut3 = np.where((r-i >= -2) & (r-i <= 7), True, False)# CRAZY REDSHIFT CUT 0.2 < Z < 0.8 ?
            colour_cut4 = np.where((i-z >= -2) & (i-z <= 7), True, False)
            rPetro_cut = np.where((rPetro >= 12.0) & (rPetro <= 19.4), True, False)
            cleancut = c["clean"] == True
            typecut = c["type"] == 3

            totalcut = cleancut & typecut & rPetro_cut & colour_cut1 & colour_cut2 & colour_cut3 & colour_cut4

            c = c[totalcut]

            master_cat = pandas.concat([master_cat, c])

            del c
            gc.collect()

    pandas.DataFrame.to_csv(master_cat, str(out_cat), columns=['objID', 'ra', 'dec'])

if __name__ == '__main__':
    out_cat = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog.csv'
    catalog_dir = '/share/data1/SDSS_DR12_Photometry/'
    cut(catalog_dir, out_cat)
    
