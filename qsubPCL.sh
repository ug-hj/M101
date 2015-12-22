#!/bin/tcsh
#PBS -q compute
#PBS -N Cl-10
#PBS -l nodes=1:ppn=1
#PBS -l mem=50gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk
#PBS -m bea

source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh

cd $PBS_O_WORKDIR

Alm2Cl -I /share/splinter/ug_hj/M101/PCL/256cutmap_alms.fits -O /share/splinter/ug_hj/M101/PCL/bin10/256ValMax_Cls.dat -P -m /share/splinter/ug_hj/M101/256cutmapValueMaxmasks.fits -o -R /share/splinter/ug_hj/M101/PCL/bin10/256ValMax_IJs_Lbin10.dat -T /share/splinter/ug_hj/M101/256cutmap.fits -N 256 -L 513
