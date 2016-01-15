#!/bin/tcsh
#PBS -q smp
#PBS -N Alms
#PBS -l nodes=1:ppn=1
#PBS -l mem=50gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk

source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh

cd $PBS_O_WORKDIR

Map2Alm -I /share/splinter/ug_hj/M101/cmod512map.fits -O /share/splinter/ug_hj/M101/PCL/ebv_plus/cmod512map_alms.fits -L 513 -m /share/splinter/ug_hj/M101/Ebv0.4See1.55Air1.4VM200BrBa_512mask.fits
