from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
import os
import pandas
import gc

def main(nside, jobname, queue, root_dir, mask_fits, outfile_dir):
	
	slice_cross = [[0,0], [0,1], [0,2],	[0,3], [0,4], [0,5], [0,6], 
					[1,1], [1,2], [1,3], [1,4], [1,5], [1,6], 
					[2,2], [2,3], [2,4], [2,5], [2,6], 
					[3,3], [3,4], [3,5], [3,6], 
					[4,4], [4,5], [4,6], 
					[5,5], [5,6], 
					[6,6]]

	slice_single = [1, 2, 3, 4, 5, 6, 7]

	if not isdir(outfile_dir):
		os.mkdir(outfile_dir)

	ANNz_dir = join(root_dir, "ANNz")
	sdssPZ_dir = join(root_dir, "sdssPZ")
	ANNz_alms = join(ANNz_dir, "Alms")
	sdssPZ_alms = join(sdssPZ_dir, "Alms")
	ANNz_Cls = join(ANNz_dir, "Cls")
	sdssPZ_Cls = join(sdssPZ_dir, "Cls")

	z_src_attr = [[ANNz_dir, ANNz_alms, ANNz_Cls, "ANNz"], 
					[sdssPZ_dir, sdssPZ_alms, sdssPZ_Cls, "sdssPZ"]]

	for attr in z_src_attr:

		if not isdir(attr[2]):
			os.mkdir(attr[2])

		for cross in slice_cross:
			first = cross[0] + 1
			second = cross[1] + 1
			shell_script = ["#!/bin/tcsh",
						"#PBS -q " + str(queue),
						"#PBS -N " + str(jobname) + str(first) + "x" + str(second),
						"#PBS -l nodes=1:ppn=1",
						"#PBS -l mem=10gb",
						"#PBS -l walltime=120:00:00",
						"",
						"source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh",
						"", 
						"cd $PBS_O_WORKDIR",
						""]									

			shell_script.append("Alm2Cl -I " + join(attr[1], str(first) + "_alms.fits") + " -O " + join(attr[2], str(first) + "x" + str(second) + "_Cls.dat") + " -P -m " + str(mask_fits) + " -R " + str(IJs) + " -T " + join(attr[0], str(first) + "_map.fits") + " -N " + str(nside) + " -L " + str((2*nside) + 1) + " -c " + join(attr[1], str(second) + "_alms.fits") + " " + join(attr[0], str(second) + "_map.fits") + " -G")

			shell_script.append("")

			F = join(outfile_dir, attr[3] + str(first) + "x" + str(second) + "autocross_qsub.sh")
			A = open(F, "w")
			T = "\n".join(shell_script)
			A.write(str(T))
			A.close()

		for single in slice_single:
		
			shell_script = ["#!/bin/tcsh",
						"#PBS -q " + str(queue),
						"#PBS -N Cl." + str(single),
						"#PBS -l nodes=1:ppn=1",
						"#PBS -l mem=10gb",
						"#PBS -l walltime=120:00:00",
						"",
						"source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh",
						"", 
						"cd $PBS_O_WORKDIR",
						""]

			shell_script.append("Alm2Cl -I " + join(attr[1], str(single) + "_alms.fits") + " -O " + join(attr[2], str(single) + "_Cls.dat") + " -P -m " + str(mask_fits) + " -R " + str(IJs) + " -T " + join(attr[0], str(single) + "_map.fits") + " -N " + str(nside) + " -L " + str((2*nside) + 1) + " -G")

			shell_script.append("")

			F = join(outfile_dir, attr[3] + "single" + str(single) + "_qsub.sh")
			A = open(F, "w")
			T = "\n".join(shell_script)
			A.write(str(T))
			A.close()

			# os.system("qsub " + F)
			# os.system("sleep 1")

if __name__ == "__main__":
	nside = 256
	jobname = "cross."
	queue = "compute"
	IJs = "/share/splinter/ug_hj/M101/GAMA_Mask1_IJs.dat"
	root_dir = "/share/splinter/ug_hj/M101/Slices/" # check for ////
	mask_fits = "/share/splinter/ug_hj/M101/Mask1.fits"
	outfile_dir = "/share/splinter/ug_hj/M101/Cl_qsubs/Mask1/" # check MASK & 																			check for ////
	main(nside, jobname, queue, root_dir, mask_fits, outfile_dir)
