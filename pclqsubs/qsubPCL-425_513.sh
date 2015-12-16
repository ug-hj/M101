#!/bin/tcsh
#PBS -q compute
#PBS -N PCL
#PBS -l nodes=1:ppn=1
#PBS -l mem=50gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk
#PBS -m bea

source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh

cd $PBS_O_WORKDIR

IlmJlm -m /share/splinter/ug_hj/M101/256cutmapValuemask.fits -O /share/splinter/ug_hj/M101/PCL/256cutmapValuemask_IlmJlm_425-513.dat -N 256 -l 425 -L 513
