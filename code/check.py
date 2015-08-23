import os
from tempfile import mkstemp
from shutil import move
from os import remove, close

'''
1. Replace F/M-> "F"/"M"
''' 
def replace_value(fname):
	path= "/home/amm/Desktop/sna-git/data/"
	
	#for fname in os.listdir(path):
	file_path = path+fname
	pattern = "gender F" 
	subst = "gender \"F\"" 
	replace(file_path, pattern, subst)
	pattern = "gender M" 
	subst = "gender \"M\"" 
	replace(file_path, pattern, subst)

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)
    
'''
1. Remove unreadable characters    
2. Add ex-students (not in official student list) sreferred by current students
'''
def check():
	path =   "/media/sf_analysis/data/GML/"
	#fname_list = ["ICT55_friend.gml","ICT55_bf.gml","ICT55_study.gml"]
	fname_list = ["ICT57-All_friend.gml"]#"ICT57-All_friend.gml",,"ICT57-All_study.gml"
	
	#fname_list = os.listdir(path)
	for fname in fname_list:
		print fname
		if os.path.isdir(path+fname): continue
		if fname.split(".")[1] !="gml": continue
		if fname.startswith("ICT57"):
			num = 4
		else:
			num = 5
 		f_r = open(path+fname,"r")
		 
		data = f_r.read().decode("utf-8-sig").encode("utf-8")
		 
 		f_w = open("/home/amm/Desktop/sna-git/temp","w")
 					
		f_w.write(data)
		f_w.close()
		f_r.close()	
		
		f_r = open("/home/amm/Desktop/sna-git/temp", "r") 
		f_w = open("/home/amm/Desktop/sna-git/data/"+fname,"w")
		
		id_set = set()
		lineno = 0 
  		for line in f_r.readlines():
			 
			line = line.strip('\xe2\x80\x83')
			line = line.strip('?')
			lineno += 1
			if len(line.split())>1:
				 
				fst, snd = line.split()
			  
				if fst.strip()=="id":
					newid = snd.strip()[num::]
					if newid not in id_set:
						id_set.add(newid)
					f_w.writelines(fst+" "+ newid+"\n")
					
				elif fst.strip() == "source" or fst.strip() == "target":
					newid = snd.strip()[num::]
					if newid not in id_set:
						
						newid = snd 
						print newid+" not in id_set at line "+str(lineno)
						#if newid == "x":
						newid = '99999'
  							
 						 
 					f_w.writelines(fst+" "+ newid+"\n")	
  					
				else:
					f_w.writelines(line)
					
			else:
				f_w.writelines(line)
						
		f_r.close()
		f_w.close()
		
		f_r = open("/home/amm/Desktop/sna-git/data/"+fname,"r")
		data = f_r.readlines()
		f_r.close()
		
		f_w = open("/home/amm/Desktop/sna-git/data/"+fname,"w")
 		data.insert(2, "node [\n")
		data.insert(3, "id 99999\n")
		data.insert(4, "gpa 0.00\n")
		data.insert(5, "year 00\n")
		data.insert(6, "gender \"x\"\n")
		data.insert(7, "]\n")
		data = "".join(data)
		f_w.write(data)
		f_w.close()
		replace_value(fname)	

check()
 

'''
Steps to process data
1. check()
2. markUnsurveyed()

'''
