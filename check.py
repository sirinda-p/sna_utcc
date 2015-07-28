
def check():
	path = path = "/media/sf_analysis/data/"
	fname = "test.gml"
 	f_r = open(path+fname)
	data = f_r.read().decode("utf-8-sig").encode("utf-8")
	
	f_w = open("/Desktop/sna-git/+fname.replace(".gml","_new.gml"))
	f_w.write(data)
	
check()
