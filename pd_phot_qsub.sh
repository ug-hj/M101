#!/bin/tcsh
#PBS -q smp
#PBS -N pd.dr12.map
#PBS -l nodes=1:ppn=4
#PBS -l mem=50gb
#PBS -l walltime=120:00:00
#PBS -M zcaphjo@ucl.ac.uk

module load dev_tools/nov2014/python-anaconda

cd $PBS_O_WORKDIR

time python /share/splinter/ug_hj/M101/pd_mapper.py
