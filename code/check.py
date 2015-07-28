

def check():
	path = path = "/media/sf_analysis/data/"
	fname = "test.gml"
 	f_r = open(path+fname,"r")
	data = f_r.read().decode("utf-8-sig").encode("utf-8")
	 
 	f_w = open("/home/amm/Desktop/sna-git/data/temp","w")
	f_w.write(data)
	f_w.close()
	f_r.close()
	
	f_r = open("/home/amm/Desktop/sna-git/data/temp", "r") 
	f_w = open("/home/amm/Desktop/sna-git/data/"+fname,"w")
	
	for line in f_r.readlines():
		if len(line.split())>1:
			fst, snd = line.split()
			if fst=="id":
				newid = snd.strip()[5::]
 				f_w.writelines(fst+" "+ newid+"\n")
			elif fst == "source" or fst == "target":
				newid = snd.strip()[5::]
 				f_w.writelines(fst+" "+ newid+"\n")	
			else:
				f_w.writelines(line)
				
		else:
			f_w.writelines(line)
	
	f_r.close()
	f_w.close()
		
	
check()
