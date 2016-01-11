#!/bin/tcsh
#PBS -q smp
#PBS -N Alms
#PBS -l nodes=1:ppn=1
#PBS -l mem=50gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk

source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh

cd $PBS_O_WORKDIR

Map2Alm -I /share/splinter/ug_hj/M101/cmod_cutmap256.fits -O /share/splinter/ug_hj/M101/PCL/cmodVMBrBa/cmod256_map_alms.fits -L 513 -m /share/splinter/ug_hj/M101/cmod_V_M_Br_Ba_mask256.fits
