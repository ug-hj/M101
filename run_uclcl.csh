#!/bin/tcsh
#PBS -q compute
#PBS -N uclcl
#PBS -l nodes=1:ppn=1
#PBS -l mem=16gb
#PBS -l walltime=12:0:00
#PBS -V

module load dev_tools/nov2014/python-anaconda
module load dev_tools/nov2014/gcc-4.8.2
module load dev_tools/nov2014/boost-5.57.0


#setenv OMP_NUM_THREADS 1

cd /share/splinter/ug_hj/M101/UCLCl/
/share/data1/sbalan/source_tree/uclcl/build/interface/uclcl ../uclcl_topspline_test.ini
