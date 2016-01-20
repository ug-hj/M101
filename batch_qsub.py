import os

for q in os.listdir("/share/splinter/ug_hj/M101/PCL/ebv_plus/"):
	if q.endswith(".sh"):
		os.system("qsub " + "/share/splinter/ug_hj/M101/PCL/ebv_plus/" + q)
		os.system("sleep 1")
