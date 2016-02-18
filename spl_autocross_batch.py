from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
import os
import pandas
import gc

def main(nside, jobname, queue, alms_dir, mask_fits, outfile_dir):
	
	slice_cross = [[0,0], [0,1], [0,2],	[0,3], [0,4], [0,5], [0,6], [0,7], 
					[1,1], [1,2], [1,3], [1,4], [1,5], [1,6], [1,7], 
					[2,2], [2,3], [2,4], [2,5], [2,6], [2,7], 
					[3,3], [3,4], [3,5], [3,6], [3,7], 
					[4,4], [4,5], [4,6], [4,7], 
					[5,5], [5,6], [5,7], 
					[6,6], [6,7], 
					[7,7]]

	slice_single = [1, 2, 3, 4, 5, 6, 7]

	if not isdir(outfile_dir):
		os.mkdir(outfile_dir)

	map_dir = alms_dir[:-5]
	Cls_dir = join(map_dir, "Cls")

	if not isdir(Cls_dir):
		os.mkdir(Cls_dir)

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

		shell_script.append("Alm2Cl -I " + str(alms_dir) + str(first) + "_alms.fits -O " + join(Cls_dir, str(first) + "x" + str(second) + "_Cls.dat") + " -P -m " + str(mask_fits) + " -R " + str(IJs) + " -T " + str(alms_dir) + str(first) + "_map.fits -N " + str(nside) + " -L " + str((2*nside) + 1) + " -c " + str(alms_dir) + str(second) + "_alms.fits " + str(alms_dir) + str(second) + "_map.fits -G")

		shell_script.append("")

		F = str(outfile_dir) + str(first) + "x" + str(second) + "autocross_qsub.sh"
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

		shell_script.append("Alm2Cl -I " + str(alms_dir) + str(single) + "_alms.fits -O " + join(Cls_dir, str(single) + "_Cls.dat") + " -P -m " + str(mask_fits) + " -R " + str(IJs) + " -T " + str(alms_dir) + str(single) + "_map.fits -N " + str(nside) + " -L " + str((2*nside) + 1) + " -G")

		shell_script.append("")

		F = str(outfile_dir) + "single" + str(single) + "_qsub.sh"
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
	alms_dir = "/share/splinter/ug_hj/M101/sdssPZ_slices1/Alms/" # check for ////
	mask_fits = "/share/splinter/ug_hj/M101/Mask1.fits"
	outfile_dir = "/share/splinter/ug_hj/M101/Cl_qsubs/sdssPZs_1/" # check for ////
	main(nside, jobname, queue, alms_dir, mask_fits, outfile_dir)
