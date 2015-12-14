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

Map2Alm -I /share/splinter/ug_hj/M101/256cutmap.fits -O /share/splinter/ug_hj/M101/PCL/256cutmap_alms.fits -L 513 -m /share/splinter/ug_hj/M101/256cutmapValuemask.fits

Alm2Cl -I /share/splinter/ug_hj/M101/PCL/256cutmap_alms.fits -O /share/splinter/ug_hj/M101/PCL/256cutmap_Cls.dat -P -m /share/splinter/ug_hj/M101/256cutmapValuemask.fits -o -C /share/splinter/ug_hj/M101/PCL/256cutmapValuemask_IlmJlm.dat -T /share/splinter/ug_hj/M101/256cutmap.fits -N 256 -L 513