from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, isdir
from os import listdir, mkdir
import pandas
import csv
import gc

def stats(catalog, out_dir, slice_intervals):

    # read in catalog
    c = pandas.read_csv(catalog, sep=',', header=0, dtype={'z' : np.float64, 'ANNZ_best' : np.float64}, engine=None, usecols=['z', 'ANNZ_best'])

    z = np.array(c['z'])
    ANNz = np.array(c['ANNZ_best'])

    sanity_z = np.where((0 < z) & (z < 0.8), True, False)
    sanity_ANNz = np.where((0 < ANNz) & (ANNz < 0.8), True, False)

    z = z[sanity_z]
    ANNz = ANNz[sanity_ANNz]

    # define slices
    z_slices = []
    ANNz_slices = []

    for cut in slice_intervals:
        z_slice = np.where((cut[0] <= z) & (z <= cut[1]), True, False)
        ANNz_slice = np.where((cut[0] <= ANNz) & (ANNz <= cut[1]), True, False)
        z_slices.append(z_slice)
        ANNz_slices.append(ANNz_slice)

    sdssPZ_dir = join(out_dir, "sdssPZ")
    if not isdir(sdssPZ_dir):
        mkdir(sdssPZ_dir)

    fl_1 = open(join(out_dir, 'sdss_stats_wN.csv'), 'w')

    writer = csv.writer(fl_1)
    writer.writerow(['mean', 'var', 'N'])

    for i, zslice in enumerate(z_slices):

        z_1 = z[zslice]

        mean = np.mean(z_1)
        var = np.var(z_1)
        count = len(z_1)

        z_csv_row = [mean, var, count]

        writer.writerow(z_csv_row)
        
        # report z-mean
        mean_rep = "z_slice" + str(i+1) + " z-mean = " + str(mean)

        # report z-variance
        var_rep = "z_slice" + str(i+1) + " z-var = " + str(var)

        # report slice counts
        count_rep = "z_slice" + str(i+1) + " # galaxies = " + str(count)

        print("z_slice" + str(i+1) + " z-mean = " + str(mean),
                "z_slice" + str(i+1) + " z-var = " + str(var),
                "z_slice" + str(i+1) + " # galaxies = " + str(count))

        del mean, var, count, z_1, z_csv_row 
        gc.collect()

    fl_1.close()

    ANNz_dir = join(out_dir, "ANNz")
    if not isdir(ANNz_dir):
        mkdir(ANNz_dir)

    fl_2 = open(join(out_dir, 'ANNz_stats_wN.csv'), 'w')

    writer = csv.writer(fl_2)
    writer.writerow(['mean', 'var', 'N'])

    for i, ANNzslice in enumerate(ANNz_slices):

        ANNz_1 = ANNz[ANNzslice]

        mean = np.mean(ANNz_1)
        var = np.var(ANNz_1)
        count = len(ANNz_1)

        ANNz_csv_row = [mean, var, count]

        writer.writerow(ANNz_csv_row)
        
        # report z-mean
        mean_rep = "ANNz_slice" + str(i+1) + " z-mean = " + str(mean)

        # report z-variance
        var_rep = "ANNz_slice" + str(i+1) + " z-var = " + str(var)

        # report slice counts
        count_rep = "ANNz_slice" + str(i+1) + " # galaxies = " + str(count)

        print("ANNz_slice" + str(i+1) + " z-mean = " + str(mean),
                "ANNz_slice" + str(i+1) + " z-var = " + str(var),
                "ANNz_slice" + str(i+1) + " # galaxies = " + str(count))

        del mean, var, count, ANNz_1, ANNz_csv_row
        gc.collect()

    fl_2.close()

    return None

def main(catalog, out_dir, slice_intervals):
        
    # create destination directories
    if not isdir(out_dir):
        mkdir(out_dir)

    stats(catalog, out_dir, slice_intervals)
    
    return None

if __name__ == "__main__":
    catalog = "/share/splinter/ug_hj/M101/SDSS_GAMA_photozs_merged.csv"
    out_dir = '/share/splinter/ug_hj/M101/Slices/z-stats'
    slice_intervals = [[0.05, 0.10], [0.10, 0.15], [0.15, 0.20], [0.20, 0.25],
                         [0.25, 0.30], [0.30, 0.35], [0.35, 0.40]]
    main(catalog, out_dir, slice_intervals)
