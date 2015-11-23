from __future__ import print_function
import time
from astropy.table import Table

t0 = time.time()
c = Table.read("/Users/Harry/M101/catalogs_sdss/sdss_dr12_testfile_copy.csv")
t1 = time.time() - t0

print("Table reading time:", t1)
