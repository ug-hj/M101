from __future__ import print_function
import time
from astropy.table import Table
import random
from os.path import join
from os import listdir

t0 = time.time()
c = Table.read(join("/share/data1/SDSS_DR12_Photometry", random.choice(listdir("/share/data1/SDSS_DR12_Photometry"))))
t1 = time.time() - t0

print("Table reading time:", t1)
