from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
from os import listdir, mkdir
import pandas
import gc
import math

def merger(infile_1, infile_2, out_filename):
	A = hp.read_map(infile_1)
	B = hp.read_map(infile_2)

	C = A*B

	hp.write_map(out_filename, C)

	return None
