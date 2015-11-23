#!/bin/tcsh
#PBS -q cores12
#PBS -N pd_test
#PBS -l nodes=1:ppn=1
#PBS -l mem=48gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk
#PBS -m bea

module load dev_tools/nov2014/python-anaconda

cd $PBS_O_WORKDIR

time python /share/splinter/ug_hj/M101/pandas_test.py
