from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
import os
import pandas
import gc

def main(nside, jobname, queue, map_dir, mask_fits, outfile_dir):
	
	slice_number = np.arange(start=1,stop=8,step=1)

	if not isdir(outfile_dir):
		os.mkdir(outfile_dir)

	for i in slice_number:
		shell_script = ["#!/bin/tcsh",
					"#PBS -q " + str(queue),
					"#PBS -N " + str(jobname) + str(i),
					"#PBS -l nodes=1:ppn=1",
					"#PBS -l mem=10gb",
					"#PBS -l walltime=120:00:00",
					"",
					"source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh",
					"", 
					"cd $PBS_O_WORKDIR",
					""]									

		shell_script.append("Map2Alm -I " + str(map_dir) + str(i) + "_map.fits -O " + str(map_dir) + str(i) + "_alms.fits -L " + str((2*nside) + 1) + " -m " + str(mask_fits))

		shell_script.append("")

		F = str(outfile_dir) + str(i) + "alm_qsub.sh"
		A = open(F, "w")
		T = "\n".join(shell_script)
		A.write(str(T))
		A.close()

		# os.system("qsub " + F)
		# os.system("sleep 1")

if __name__ == "__main__":
	nside = 256
	jobname = "alms."
	queue = "compute"
	map_dir = "/share/splinter/ug_hj/M101/sdssPZ_slices1/"
	mask_fits = "/share/splinter/ug_hj/M101/Mask1.fits"
	outfile_dir = "/share/splinter/ug_hj/M101/qsubalms/" # check for ////
	main(nside, jobname, queue, map_dir, mask_fits, outfile_dir)
