#!/bin/tcsh -f
#PBS -q compute
#PBS -N test
#PBS -l nodes=1:ppn=1
#PBS -l mem=50gb
#PBS -l walltime=01:00:00
#PBS -o /share/splinter/ug_hj
#PBS -S /bin/tcsh

cd $PBS_O_WORKDIR
source /etc/profile.d/modules.csh
module load dev_tools/nov2014/python-anaconda

python /share/splinter/ug_hj/hp_map_maker_hj.py