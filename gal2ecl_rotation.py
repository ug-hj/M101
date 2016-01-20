from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc
from astropy.coordinates import SkyCoord

def gal2ecl(in_file, out_file, deg_angles):
    # galactic = hp.read_map(in_file)
    # b = np.arange(len(galactic))

    # c = hp.pix2ang(nside, b, nest=False)
    # r = hp.Rotator(coord=['G','E'])
    # theta_ecl, phi_ecl = r(c[0], c[1])

    # pix_IDs = hp.ang2pix(nside, theta_ecl, phi_ecl, nest=False)
    # ecliptic = [0]*hp.nside2npix(nside)

    # for (i, pix) in enumerate(pix_IDs):
    #     ecliptic[pix] = galactic[i]
    
    eulers = [np.deg2rad(x) for x in deg_angles]

    alms = hp.read_alm(in_file)
    rotated_alms = hp.rotate_alm(alms, eulers[0], eulers[1], eulers[2], lmax=513)

    hp.write_map(out_file, rotated_alms)

if __name__ == "__main__":
    in_file = '/share/splinter/ug_hj/lambda256ebv_alms.fits'
    out_file = '/share/splinter/ug_hj/lambda256ebv_almsRotated.fits'
    deg_angles = [282.25, 62.6, 33]
    gal2ecl(in_file, nside, out_file)