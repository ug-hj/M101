#!/bin/tcsh
#PBS -q compute
#PBS -N Alms
#PBS -l nodes=1:ppn=1
#PBS -l mem=5gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk

source /share/splinter/sbalan/Projects/LauraPCL/envvars.csh

cd $PBS_O_WORKDIR

Map2Alm -I /share/splinter/ug_hj/M101/lambda256_ebv.fits -O /share/splinter/ug_hj/M101/lambda256ebv_alms.fits -L 513 -m /share/splinter/ug_hj/M101/lambda256_ebvValuemask.fits
