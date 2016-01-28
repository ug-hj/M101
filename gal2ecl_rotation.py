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
    
    eulers = (deg_angles*2*np.pi)/360

    alms = hp.read_alm(in_file)
    hp.smoothalm(alms, fwhm=0.018)
    hp.rotate_alm(alms, eulers[0], eulers[1], eulers[2])

    hp.write_alm(out_file, alms)

if __name__ == "__main__":
    in_file = '/share/splinter/ug_hj/M101/lambda256ebv_alms.fits'
    out_file = '/share/splinter/ug_hj/M101/lambda256ebv_almsRotated.fits'
    deg_angles = np.array([282.25, 62.6, 33])
    gal2ecl(in_file, out_file, deg_angles)
