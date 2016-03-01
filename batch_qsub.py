import os
from os.path import join

def batchsub(qsub_dir):
	for q in os.listdir(qsub_dir):
		if q.endswith("sh"):
			os.system("qsub " + join(qsub_dir, q))
	#		os.system("sleep 1")

if __name__ == "__main__":
	qsub_dir = "/share/splinter/ug_hj/M101/Cl_qsubs_Ovr/Mask1/"
	batchsub(qsub_dir)
