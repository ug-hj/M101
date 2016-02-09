#!/bin/tcsh
#PBS -q compute
#PBS -N match9
#PBS -l nodes=1:ppn=1
#PBS -l mem=15gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk
#PBS -m ea

module load dev_tools/nov2014/python-anaconda

cd $PBS_O_WORKDIR

time python /share/splinter/ug_hj/M101/spl_pz_match.py
