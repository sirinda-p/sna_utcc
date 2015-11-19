
def checkNormData():
	machine = "aws"
	if machine == "amm":
		prefix = "/home/amm/"
	else:
		prefix = "/home/ubuntu/"
	
	att_name = ["ID", "AllowPush","AdOptedIn","NumCampaignMatch","Carrier","AppVersion","StartDate","AllowiBeacon",
	"AllowGeo","AllowFeaturePush","ScreenHeight", "AllowBT","HaveUniqueGlobalID","NumCrash","DailyUsage","IP","LastUpdateDate",
	"mode-ignore","DeviceModel","BlockPush","OS","OSVersion","RevokePush","SignIn","smart-ignore",
	"Uninstalled","ScreenWidth","EmailExist","EmailAddress","InstallDays","PushCount", "Timezone","sdk","UserType","Questions",
	"CorrectQuestion"]
	
	new_att_name = ["ID",'AllowPush', 'AdOptedIn', 'NumCampaignMatch', 'Carrier', 'AppVersion', 'AllowiBeacon', 'AllowGeo', 'AllowFeaturePush', 'ScreenHeight',  'AllowBT', 'HaveUniqueGlobalID', 'NumCrash', 'DailyUsage', 'LastUpdateDays', 'DeviceModel', 'BlockPushTF', 'BlockPushDays', 'OS', 'OSVersion','RevokePushTF', 'RevokePushDays', 'SignIn', 'UninstalledTF', 'UninstalledDays', 'ScreenWidth', 'EmailExist', 'EmailAddress', 'InstallDays', 'PushCount',   'Timezone', 'UserType', 'Questions', 'CorrectQuestion']
	
	path = prefix+"Desktop/upwork/data/"
	f_r1 = open(path+"appt_dump_rewritten.csv", "r")
	f_r2 = open(path+"appt_dump_norm.csv", "r")
	
	 
	for l1, l2 in zip(f_r1.readlines(), f_r2.readlines()):
		arr1 = l1.split(",")
		arr2 = l2.split(",")
		 
		print att_name[1:10]
		print new_att_name[1:9]
		
		print arr1[1:10]
		print arr2[1:9]
		print ("\n")
		
		print att_name[10:21]
		print new_att_name[9:19]
		print arr1[10:21]
		print arr2[9:19]
		print ("\n")
		
		print att_name[21:30]
		print new_att_name[19:29]
		print arr1[21:30]
		print arr2[19:29]
		
		print ("\n")
		
		print att_name[30::]
		print new_att_name[29::]
		print arr1[30::]
		print arr2[29::]
		
		
		print ("\n")
		
		break
		

checkNormData()
