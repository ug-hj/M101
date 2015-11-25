#%matplotlib
import os
import os.path
import healpy as hp
import numpy as np

npix = hp.nside2npix(128)
hmap = np.zeros(npix)

for cmap in os.listdir("/share/splinter/ug_hj/M101/128_SDSS"):
    m = hp.read_map(os.path.join("/share/splinter/ug_hj/M101/128_SDSS", cmap))
    hmap += m
    
hp.write_map("/share/splinter/ug_hj/M101/128_SDSS/SDSS_cmap_128.fits", hmap)