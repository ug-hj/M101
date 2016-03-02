from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
import os
import pandas
import gc

def main(nside, jobname, queue, map_dir, mask, mask_fits, outfile_dir):
	
	slice_number = np.arange(start=1,stop=8,step=1)

	if not isdir(outfile_dir):
		os.mkdir(outfile_dir)

	ANNz_dir = join(map_dir, "ANNz")
	sdssPZ_dir = join(map_dir, "sdssPZ")

	ANNzalm_root = join(map_dir, mask, "ANNz")
	sdssPZalm_root = join(map_dir, mask, "sdssPZ")

	for root in [ANNzalm_root, sdssPZalm_root]:
		if not isdir(root):
			os.mkdir(root)

	ANNzalm_dir = join(ANNzalm_root, "Alms")
	sdssPZalm_dir = join(sdssPZalm_root, "Alms")

	map_alm_dirs = [[ANNz_dir, ANNzalm_dir, "ANNz"], [sdssPZ_dir, sdssPZalm_dir, "sdssPZ"]]

	for attr in map_alm_dirs:
		if not isdir(attr[1]):
			os.mkdir(attr[1])

		for i in slice_number:
			shell_script = ["#!/bin/tcsh",
						"#PBS -q " + str(queue),
						"#PBS -N " + str(jobname) + str(attr[2]) + str(i),
						"#PBS -l nodes=1:ppn=1",
						"#PBS -l mem=10gb",
						"#PBS -l walltime=120:00:00",
						"",
						"source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh",
						"", 
						"cd $PBS_O_WORKDIR",
						""]									

			shell_script.append("Map2Alm -I " + join(attr[0],"Ovr2_" + str(i) + "_map.fits") + " -O " + join(attr[1], str(i) + "_Ovr2_alms.fits") + " -L " + str((2*nside) + 1) + " -m " + str(mask_fits))

			shell_script.append("")

			F = join(outfile_dir, attr[2] + str(i) + "_Ovr2_alm_qsub.sh")
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
	map_dir = "/share/splinter/ug_hj/M101/Slices/"
	mask = "Mask3"											# CHECK MASKS
	mask_fits = "/share/splinter/ug_hj/M101/Mask3.fits"
	outfile_dir = "/share/splinter/ug_hj/M101/qsubalms_Ovr2/Mask3/" # check for ////
	main(nside, jobname, queue, map_dir, mask, mask_fits, outfile_dir)
