
#def cluster():
	

def extractFeature():
	path = "/home/ubuntu/Desktop/upwork/data/"
	f_r = open(path+"appt_dump.csv", "r")
	
	## Make original features 
	## Normalize features
	## Feature selection 
	## Perform clustering 
	att_name = ["ID", "AllowAccessPush","AdOptedIn","NumCampaignMatch","Carrier","AppVersion","StartDate","AllowiBeacon",
	"AllowGeo","AllowFeaturePush","ScreenHeight","AllowBT","HaveUniqueGlobalID","NumCrash","DailyUsage","IP","LastUpdateDate",
	"mode-ignore","DeviceModel","BlockPush","OS","OSVersion","RevokePush","SignIn","smart-ignore",
	"Uninstalled","ScreenWidth","EmailExist","EmailAddress","InstallDays","PushCount","TimeOffset","sdk","UserType","Questions",
	"CorrectQuestion"]
	num_att = len(att_name)
	print num_att
	len_arr = []
	print36 = False
	print37 = False
	
	data = dict()
	for i in range(0, num_att):
		data[i] = set()
		
	extra_att = set() 
	num_extra_rows = 0
	for line in f_r.readlines():
		arr = line.strip().split(",") 
		
		## Check format of each attribute
		if len(arr) > num_att:
			for i in range(0, 19):
				data[i].add(arr[i]) 
			## skip attribute #20 (19 in arr) 
			extra_att.add(arr[19])
			num_extra_rows += 1 
			for i in range(20, num_att+1):
				data[i-1].add(arr[i]) 
				
		else:
			for i in range(0, num_att):
				data[i].add(arr[i])  
					
	
	for i, arr in data.items():
				
		print str(i+1)+": "+ att_name[i]
		print arr
	
	print "Extra attribute"
	print extra_att	
	print num_extra_rows
	f_r.close()


extractFeature()
