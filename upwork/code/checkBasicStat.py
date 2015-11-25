import collections, itertools


def feature_stat():
	
	original = False
	machine = "amm"
	if machine == "amm":
		prefix = "/home/amm/Desktop/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/"
	
	path = prefix+"/upwork/data/"
	f_r = open(path+"appt_dump_transformed_continent.csv", "r")
	
	if original:
		f_r = open(path+"appt_dump_rewritten.csv", "r")
 		att_name = ["ID", "AllowAccessPush","AdOptedIn","NumCampaignMatch","Carrier","AppVersion","StartDate","AllowiBeacon",
	"AllowGeo","AllowFeaturePush","ScreenHeight","AllowBT","HaveUniqueGlobalID","NumCrash","DailyUsage","IP","LastUpdateDate",
	"mode-ignore","DeviceModel","BlockPush","OS","OSVersion","RevokePush","SignIn","smart-ignore",
	"Uninstalled","ScreenWidth","EmailExist","EmailAddress","InstallDays","PushCount","Timezone","sdk","UserType","Questions",
	"CorrectQuestion"]
	else:
		f_r = open(path+"appt_dump_transformed_continent.csv", "r")	
		att_name = ['ID', 'AllowPush', 'AdOptedIn', 'NumCampaignMatch', 'Carrier', 'AppVersion', 
	'AllowiBeacon', 'AllowGeo', 'AllowFeaturePush', 'ScreenHeight', 'AllowBT', 'HaveUniqueGlobalID', 
	'NumCrash', 'DailyUsage','Country', 'LastUpdateDays', 'DeviceModel', 'BlockPushTF', 'BlockPushSameday', 'BlockPushAfterDays', 
	'OS', 'OSVersion', 'RevokePushTF', 'RevokePushBefore', 'RevokePushSameday', 'RevokePushAfterDays', 'SignIn', 
	'UninstalledTF', 'UninstalledSameday', 'UninstalledAfter', 'ScreenWidth', 'EmailExist', 'EmailAddress', 
	'InstallDays', 'PushCount', 'Timezone', 'UserType', 'Questions', 'CorrectQuestion']
	
	## Boolean feature list
	boolean_arr_list = ["AllowPush", "AdOptedIn", "AllowiBeacon","AllowGeo","AllowFeaturePush","AllowBT",
	"HaveUniqueGlobalID","SignIn","EmailExist","EmailAddress","BlockPushTF","BlockPushSameday","RevokePushTF",
	"RevokePushBefore", "RevokePushSameday", "UninstalledTF","UninstalledSameday"]
	
	## Categorical feature list
	category_arr_list = ["AppVersion","Carrier", "DeviceModel","OS","UserType", "OSVersion","Timezone","ScreenWidth","ScreenHeight","Country" ] 
 	
	integer_arr_list = ["NumCampaignMatch","NumCrash","DailyUsage","InstallDays",
	"PushCount","Questions","CorrectQuestion", "BlockPushAfterDays", "RevokePushAfterDays", "UninstalledAfter", "LastUpdateDays"]
	
	Uni_arr_list = "AdOptedIn", "AllowiBeacon","HaveUniqueGlobalID","OS","SignIn","EmailExist","UserType"

	num_att = len(att_name)
  
	data = dict()
	for i in range(0, num_att):
		data[i] = []
		
	extra_att = set() 
	num_extra_rows = 0
	for line in f_r.readlines()[1::]:
		arr = line.strip().split(",") 
		
		for i in range(0, num_att):
			data[i].append(arr[i]) 
			 
	
	
	for i, arr in data.items():
		if i==0: continue		
		print "\n"+str(i)+": "+ att_name[i]
		att_freqs = collections.Counter(data[i])
		tt = 0
		for key, freq in att_freqs.items():
			print str((key, freq))
			tt += freq
		print "sum = "+str(tt)
		if tt!=len(data[0]):
			print "freq not equal original rows"
 
	f_r.close()
	
feature_stat()
