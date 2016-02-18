import os

for q in os.listdir("/share/splinter/ug_hj/M101/Cl_qsubs/Mask1/sdssPZs_1/"):
	if q.endswith(".sh"):
		os.system("qsub " + "/share/splinter/ug_hj/M101/Cl_qsubs/Mask1/sdssPZs_1/" + q)
		os.system("sleep 1")
