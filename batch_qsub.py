import os

for q in os.listdir("/share/splinter/ug_hj/M101/PCL/Mask1/"):
	if q.endswith(".sh"):
		os.system("qsub " + "/share/splinter/ug_hj/M101/PCL/Mask1/" + q)
		os.system("sleep 1")
