import os

for q in os.listdir("/share/splinter/ug_hj/M101/PCL/bin10/"):
	if q.endswith(".sh"):
		os.system("qsub" + q)
		os.system("sleep 1")