from __future__ import print_function, division
import numpy as np
import healpy as hp
import matplotlib
import random
from os.path import join, normpath, basename, isdir
import os
import pandas
import gc

def main(steps, jobname, queue, outfile_dir):
	job = np.arange(start=1, stop=steps, step=1)
	if not isdir(join(outfile_dir, "match_scripts")):
		os.mkdir(join(outfile_dir, "match_scripts"))
	for i in job:
		match_script = [
"from __future__ import print_function, division	",
"import numpy as np	",
"import healpy as hp	",
"import matplotlib	",
"import random	",
"from os.path import join, isdir	",
"from os import listdir, mkdir	",
"import pandas	",
"import gc	",
"	",
"def match(out_matches, out_NOmatches, upp, count_file):	",
"	",
"    num_gal = 0	",
"	",
"    root_masterpzc = '/share/splinter/ug_hj/M101/PZ_NOmatches2GAMA_sample.csv'	",
"    root_GAMAcut_cat = '/share/splinter/ug_hj/M101/GAMA_SDSScatalog_sample.csv'	",
"	",
"    pzc = pandas.read_csv(root_masterpzc, sep=',', header=0, dtype={'z' : np.float64, 'zErr' : np.float64}, engine=None, usecols=['objID', 'z', 'zErr'])	",
"	",
"    c = pandas.read_csv(root_GAMAcut_cat, sep=',', header=0, dtype={'ra' : np.float64, 'dec' : np.float64}, engine=None, usecols=['objID', 'ra', 'dec'])	",
"	",
"    len_pzc = len(pzc) + 1 # for indexing	",
"    intervals = np.arange(start=0, stop=len_pzc, step=len_pzc/10, dtype=np.int64)	",
"    pzc = pzc[intervals[upp-1]:intervals[upp]]	",
"	",
"    c_objID = c['objID']	",
"    pzc_objID = pzc['objID']	",
"	",
"    objID = [int(oID) for oID in c_objID]	",
"    pzcID_prematch = [int(pzID) for pzID in pzc_objID]	",
"	",
"    # match objIDs and photozcatIDs	",
"    snip = np.array([np.where(pzcID_prematch_i in objID, True, False) for pzcID_prematch_i in pzcID_prematch])	",
"    reverse = np.array([not i for i in snip])	",
"	",
"    pzc_NOmatch = pzc[reverse]	",
"    pzc = pzc[snip]	",
"	",
"    # galaxy count	",
"    num_gal += len(pzc)	",
"	",
"    pandas.DataFrame.to_csv(pzc, str(out_matches))	",
"    pandas.DataFrame.to_csv(pzc_NOmatch, str(out_NOmatches))	",
"	",
"    print('num_gal =', num_gal)	",
"    count = open(count_file, 'w')	",
"    count.write(str(num_gal))	",
"    count.close() 	",
"    return None	",
"	",
"if __name__ == '__main__':	",
"    upp = " + str(i),
"    out_matches = '/share/splinter/ug_hj/M101/SplitMatchRun/PZvGAMA_match' + str(upp) + '.csv'	",
"    out_NOmatches = '/share/splinter/ug_hj/M101/SplitMatchRun/PZvGAMA_NOmatch' + str(upp) + '.csv'	",
"    count_file = '/share/splinter/ug_hj/M101/SplitMatchRun/count' + str(upp) + '.txt'	",
"    match(out_matches, out_NOmatches, upp, count_file)	",
		]
		

		match_script.append("")

		F = str(outfile_dir) + "match_scripts/pzmatch" + str(i).zfill(3) + ".py"
		A = open(F, "w")
		T = "\n".join(match_script)
		A.write(str(T))
		A.close()

		shell_script = ["#!/bin/tcsh",
					"#PBS -q " + str(queue),
					"#PBS -N " + str(jobname),
					"#PBS -l nodes=1:ppn=1",
					"#PBS -l mem=15gb",
					"#PBS -l walltime=120:00:00",
					"",
					"module load dev_tools/nov2014/python-anaconda",
					"", 
					"cd $PBS_O_WORKDIR",
					"",
					"time python /share/splinter/ug_hj/M101/match_scripts/pzmatch" + str(i).zfill(3) + ".py",
					]

		shell_script.append("")

		F1 = str(outfile_dir) + "match_scripts/qsub" + str(i).zfill(3) + ".sh"
		A1 = open(F1, "w")
		T1 = "\n".join(shell_script)
		A1.write(str(T1))
		A1.close()


		# os.system("qsub " + F)
		# os.system("sleep 1")

if __name__ == "__main__":
	steps = 50
	jobname = "match"
	queue = "compute"
	outfile_dir = "/share/splinter/ug_hj/M101/" # check for ////
	main(steps, jobname, queue, outfile_dir)
