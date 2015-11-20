import datetime
import shutil
import pygeoip

def isEnglish(s):
	try:
		s.encode('ascii')
		return True
	except:
 		return False
        
def checkFile():
		
	if machine == "amm":
		prefix = "/home/amm/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	
	path = prefix+"upwork/data/"
	original_filename = "appt_dump.csv"
	new_filename = "appt_dump_rewritten.csv"
	f_r = open(path+original_filename, "r")
	
	num_att = 36
	
	rewrite = False
	lines = f_r.readlines()
	f_r.close()
	
	for line in lines :
		arr = line.strip().split(",") 
		
		## Check format of each attribute
		if len(arr) > num_att:
			rewrite = True 
			break
	
	if rewrite:
		lno =0 
		f_w = open(path+new_filename, "w")
		print "Rewrite a file :"+path+new_filename
		for line in lines:
			arr = line.strip().split(",") 
 			if len(arr) > num_att:
				## ignote att#19 
				row = [] 
				for i in range(0, 19):
					row.append(arr[i]) 
					
				## skip attribute #19(19 in arr) 
				 
				for i in range(20, num_att+1):
					row.append(arr[i]) 
				row = str(row).strip("[").strip("]").replace(" '","").replace("'","")
				f_w.write(row)
				f_w.write("\n")
				print lno
			else:
				
				f_w.write(line)
			lno += 1
		f_w.close() 
	else:
		print "Copy a file :"+path+new_filename
		shutil.copyfile(path+original_filename, path+new_filename)
				
	f_r.close()
	


def threedotnumber(dotted_number, need2num=False):
	dotted_number = dotted_number.split(".")
	if len(dotted_number ) == 2: #1.3 
		number = dotted_number[0]+dotted_number[1]+"0"
	elif len(dotted_number ) == 3:
		if need2num and int(dotted_number[2])<10:
			number = dotted_number[0]+dotted_number[1]+dotted_number[2]+"0"
		else:
			number = dotted_number[0]+dotted_number[1]+dotted_number[2]
	else:
		print "Incorrect format" 
	
	return number
					
def transformFeature():
 	
 	machine = "aws"
	if machine == "amm":
		prefix = "/home/amm/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	
	gi = pygeoip.GeoIP(prefix+"/upwork/data/GeoLiteCity.dat")

	path = prefix+"/upwork/data/"
	f_r = open(path+"appt_dump_rewritten.csv", "r")
	f_w = open(path+"appt_dump_transformed.csv", "w")
	## Make original features 
	## Normalize features
	## Feature selection 
	## Perform clustering 
	att_name = ["ID", "AllowPush","AdOptedIn","NumCampaignMatch","Carrier","AppVersion","StartDate","AllowiBeacon",
	"AllowGeo","AllowFeaturePush","ScreenHeight","AllowBT","HaveUniqueGlobalID","NumCrash","DailyUsage","IP","LastUpdateDate",
	"mode-ignore","DeviceModel","BlockPush","OS","OSVersion","RevokePush","SignIn","smart-ignore",
	"Uninstalled","ScreenWidth","EmailExist","EmailAddress","InstallDays","PushCount","Timezone","sdk","UserType","Questions",
	"CorrectQuestion"]
	
	boolean_arr_list = ["AllowPush", "AdOptedIn", "AllowiBeacon","AllowGeo","AllowFeaturePush","AllowBT",
	"HaveUniqueGlobalID","SignIn","EmailExist","EmailAddress"]
	
	## Keep originak values or group them
	interget_arr_list = ["NumCampaignMatch","ScreenHeight","NumCrash","DailyUsage","ScreenWidth","InstallDays",
	"PushCount","Questions","CorrectQuestion"]
	
	## Keep original values
	string_arr_list = ["Carrier","DeviceModel","OS","UserType"]
	
 	datetime_arr_list = [ "StartDate", "LastUpdateDate","BlockPush","RevokePush","Uninstalled"]
	special_format = ["AppVersion", "OSVersion","Timezone"]
	ignore_list = ["ID","smart-ignore", "mode-ignore", "sdk"] 
	
	num_att = len(att_name)
 	len_arr = []
	 
	'''
	data = dict()
	for i in range(0, num_att):
		data[i] = set()
	'''
	extra_att = set() 
	num_extra_rows = 0
	
	firstLine = True 
	new_att_name_arr = []
	asciirun = 0
	myhash = dict()
	new_att_name_arr.append("ID")
	countline = 0
	for line in f_r.readlines():
		arr = line.strip().split(",") 
		norm_arr = []
		## Check format of each attribute
		i=1 
		norm_arr.append( arr[0])
 		id = arr[0]
 		countline += 1
 		print countline
 		while i<len(arr):
			if att_name[i] == "IP":
				try:
					rec = gi.record_by_addr(arr[i])
					country = rec['country_name']
				except:
					country = "Unknown" 
				
				norm_arr.append(str(country).replace(",","-"))
				
				if firstLine: new_att_name_arr.append("Country")
  			elif  att_name[i] in  boolean_arr_list:
				#print att_name[i]
				if arr[i].lower()=="true":
					norm_arr.append(1)
					#print arr[i]+"->1"
				elif arr[i].lower()=="false":
					norm_arr.append(0)
					#print arr[i]+"->0"
				else:
					norm_arr.append(None)
					#print arr[i]+"->None"
					
				if firstLine: new_att_name_arr.append( att_name[i])
			
			elif att_name[i] in  interget_arr_list:
				norm_arr.append(arr[i])
				
				if firstLine: new_att_name_arr.append( att_name[i])
			
 			elif att_name[i] in string_arr_list :
				#Change category to integer
 				if not isEnglish(arr[i][0]) or arr[i][0] == "\\":
					hashval = hash(arr[i])
					#print arr[i][0] 
					if hashval not in myhash:
						asciirun += 1
						myhash[hashval] = asciirun
						ascii = asciirun 
					else:
						ascii = myhash[hashval]
 					norm_arr.append("non-ascii"+str(ascii))
					#print arr[i]+"-> non-ascii"+str(ascii)
 
				else:
					norm_arr.append(arr[i]) 
 				
 				if firstLine: new_att_name_arr.append( att_name[i])
 			
 			elif  att_name[i] in datetime_arr_list : # [ "StartDate", "LastUpdateDate","BlockPush","RevokePush","Uninstalled"]
				
				## Will not keep this attribute
				if att_name[i] == "StartDate": #'2015-10-31 08:17:03' or 2015-09-29 22:58:51.013352
 					if len( arr[i].split("."))>1: # 2015-09-29 22:58:51.013352
						start_date = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S.%f')
					else:
 						start_date = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S')
 				
					#print "\n"+att_name[i]+":"+	str(start_date)
 				
				elif att_name[i] == "LastUpdateDate":
					if len( arr[i].split("."))>1: # 2015-09-29 22:58:51.013352
						lastdate = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S.%f')
					else:
						lastdate = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S')
					
					norm_arr.append((lastdate - start_date).days) 
					#print att_name[i]+":"+	str(lastdate)  
					if firstLine: new_att_name_arr.append( "LastUpdateDays")
				
				elif att_name[i] == "RevokePush":
					## For "RevokePush" , there will be 4 new attributes  
					## 1. RevokePushTF 
					## Get RevokeDays 
					## 2. RevokePushBafore = 1 if RevokeDays <0, = 0 otherwise
					## 3. RevokePushSameDay = 1 if RevokeDays = 0 , = 0 otherwise
					## 4. RevokePushAfter = RevokeDays if RevokeDays>0, = 0 otherwise

					
  					if str(arr[i])=="None":
 						norm_arr.append(0) ## 1. RevokePushTF - False
						norm_arr.append(0) ## 2. RevokePushBafore
						norm_arr.append(0) ## 3. RevokePushSameDay
						norm_arr.append(0) ## 4. RevokePushAfter
						
						#print att_name[i]+": 0, 0, 0, 0 "
 					else:
 						if len( arr[i].split("."))>1: # 2015-09-29 22:58:51.013352
							cdate = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S.%f')
						else:
							cdate = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S')
  						days = (cdate - start_date).days
  						norm_arr.append(1) ## 1. RevokePushTF - True
  						if days< 0: ## Revoke push before first use
							norm_arr.append(1) ## 2. RevokePushBafore
							norm_arr.append(0) ## 3. RevokePushSameDay
							norm_arr.append(0) ## 4. RevokePushAfter
							#print att_name[i]+": 1, 1, 0, 0 "+str(cdate)+", "+str(days)
							
						elif  days == 0:## Revoke push same day as first use
							norm_arr.append(0) ## 2. RevokePushBafore
							norm_arr.append(1) ## 3. RevokePushSameDay
							norm_arr.append(0) ## 4. RevokePushAfter
							#print att_name[i]+": 1, 0, 1, 0 "+str(cdate)+", "+ str(days)
						else: # ## Revoke push after first use
							norm_arr.append(0) ## 2. RevokePushBafore
							norm_arr.append(0) ## 3. RevokePushSameDay
							norm_arr.append(days) ## 4. RevokePushAfter
							#print att_name[i]+": 1, 0, 0, "+str(days)+" "+str(cdate)+", "+str(days)
						
 						#print att_name[i]+"("+str(cdate)+") :1, "+str((cdate - start_date).days)
				
					if firstLine: 
						new_att_name_arr.append(att_name[i]+"TF"  )
						new_att_name_arr.append(att_name[i]+"Before"  )
						new_att_name_arr.append(att_name[i]+"Sameday"  )
						new_att_name_arr.append(att_name[i]+"After"  )
					
				elif 	 att_name[i]  in ["BlockPush","Uninstalled"]:
					## For "BlockPush" and "Uninstalled", there will be 3 new attributes for each one 
 					## BlockPush and Uninstalled on same day same time
					## 1. BlockPushTF, UninstalledTF
					## Get BlockPushDays and UninstalledDays 
					## 2. BlockPushSameday,  UninstalledSameday = 1 if Days = 0,= 0 otherwise
					## 3. BlockPushAfter,  UninstalledAfter = 1 if Days > 0,= 0 otherwise
					
					if str(arr[i])=="None":
 						norm_arr.append(0) ## 1. BlockPushTF, UninstalledTF - False
						norm_arr.append(0) ## 2. BlockPushSameday,  UninstalledSameday
						norm_arr.append(0) ## 3. BlockPushAfter,  UninstalledAfter
						
						#print att_name[i]+": 0, 0, 0"
 					else:
 						if len( arr[i].split("."))>1: # 2015-09-29 22:58:51.013352
							cdate = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S.%f')
						else:
							cdate = datetime.datetime.strptime(arr[i], '%Y-%m-%d %H:%M:%S')
  						days = (cdate - start_date).days
  						norm_arr.append(1) ## 1. BlockPushTF, UninstalledTF - True
  						if days<1: ## block push/install same day as first use
 							norm_arr.append(1) ## 2. BlockPushSameday,  UninstalledSameday
							norm_arr.append(0) ## 3. BlockPushAfter,  UninstalledAfter
							#print att_name[i]+": 1, 1, 0 "+str(cdate)+"-"+str(days)
						else: # ## Revoke push after first use
 							norm_arr.append(0) ## 2. BlockPushSameday,  UninstalledSameday
							norm_arr.append(days) ## 3. BlockPushAfter,  UninstalledAfter
							#print att_name[i]+": 1, 0, "+str(days)+" "+str(cdate)+"-"+str(days)
 						#print att_name[i]+"("+str(cdate)+") :1, "+str((cdate - start_date).days)
					
					if firstLine: 
						new_att_name_arr.append(att_name[i]+"TF"  )
 						new_att_name_arr.append(att_name[i]+"Sameday"  )
						new_att_name_arr.append(att_name[i]+"After"  )
					
			
  			## ["AppVersion","IP","OSVersion","Timezone","sdk"]
			elif att_name[i] == "AppVersion": #client_version '1.0.7 (1.2.56)'
				num_arr = arr[i].split("(")
				
				## split number by dot and return a whole integer number
				first_number = threedotnumber(num_arr[0].strip())
				second_number = threedotnumber(num_arr[1].strip().strip(")"), need2num=True )
			 
 				norm_arr.append(first_number+second_number )			
				if firstLine: new_att_name_arr.append( att_name[i])
				
			elif  att_name[i] == "OSVersion":	
				
 				norm_arr.append(threedotnumber(arr[i]))
				if firstLine: new_att_name_arr.append( att_name[i])
				
			elif  att_name[i] == "Timezone":	
 				norm_arr.append(int(arr[i])/60) 
				if firstLine: new_att_name_arr.append( att_name[i])
				
			elif  att_name[i] in ignore_list:	## IP: won't use it , # SDK: probably irrelevant DOTTED NUMBER
				i += 1
				continue
 
			else:
				print arr[i]+" at "+str(i)+" not checked\n"
			
			i += 1
		
		if firstLine: 
			#print new_att_name_arr
			#print len(new_att_name_arr)
			f_w.write(str(new_att_name_arr).strip("[").strip("]").replace("'",""))
			f_w.write("\n")
		firstLine = False
 		f_w.write(str(norm_arr).strip("[").strip("]").replace("'","")+"\n")
 		if len(norm_arr) != 39:
			print "incorrect #norm_arr +"+str(len(norm_arr))
	
	f_r.close()
	f_w.close()

transformFeature()
#steps
#1. extract.py
#2. normalize.py
