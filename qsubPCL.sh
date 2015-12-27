#!/bin/tcsh
#PBS -q compute
#PBS -N Cl.4mask
#PBS -l nodes=1:ppn=1
#PBS -l mem=50gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk

source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh

cd $PBS_O_WORKDIR

Alm2Cl -I /share/splinter/ug_hj/M101/PCL/ValMaxBriBadx1/256cutmap_alms.fits -O /share/splinter/ug_hj/M101/PCL/ValMaxBriBadx1/256ValMaxBriBadx1_Cls.dat -P -m /share/splinter/ug_hj/M101/256ValMaxBriBadx1_mask.fits -o -R /share/splinter/ug_hj/M101/PCL/ValMaxBriBadx1/256ValMaxBriBadx1_IJ_tot.dat -T /share/splinter/ug_hj/M101/256cutmap.fits -N 256 -L 513
