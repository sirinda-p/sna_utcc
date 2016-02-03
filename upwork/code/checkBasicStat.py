import collections, itertools


def feature_stat():
	
	original = False
	machine = "amm"
	if machine == "amm":
		prefix = "/home/amm/Desktop/sna-project/sna-git/upwork/"
	else:
		prefix = "/home/ubuntu/Desktop/sna_utcc/upwork/"
	
	path = prefix+"data/"
	fname_arr = ["active_paid_transformed_continent.csv","active_free_transformed_continent.csv",
	"active_transformed_continent.csv","free_transformed_continent.csv", "churn_paid_transformed_continent.csv","churn_free_transformed_continent.csv",
	"churn_transformed_continent.csv","paid_transformed_continent.csv"]
	
	for fname in   fname_arr:
	
		print fname
		f_r = open(path+fname, "r")
		f_w = open(path+fname.replace(".csv", "_stat.doc"), "w")
		
		if original:
			f_r = open(path+"appt_dump_rewritten.csv", "r")
			att_name = ["ID", "AllowAccessPush","AdOptedIn","NumCampaignMatch","Carrier","AppVersion","StartDate","AllowiBeacon",
		"AllowGeo","AllowFeaturePush","ScreenHeight","AllowBT","HaveUniqueGlobalID","NumCrash","DailyUsage","IP","LastUpdateDate",
		"mode-ignore","DeviceModel","BlockPush","OS","OSVersion","RevokePush","SignIn","smart-ignore",
		"Uninstalled","ScreenWidth","EmailExist","EmailAddress","InstallDays","PushCount","Timezone","sdk","UserType","Questions",
		"CorrectQuestion"]
		else:
			#f_r = open(path+"appt_dump_transformed_continent.csv", "r")	
			att_name = ["ID", "AllowPush", "AdOptedIn", "NumCampaignMatch", "Carrier", "AppVersion", 
		"AllowiBeacon", "AllowGeo", "AllowFeaturePush", "ScreenHeight", "AllowBT", "HaveUniqueGlobalID", 
		"NumCrash", "DailyUsage","Country", "LastUpdateDays", "DeviceModel", "BlockPushTF", "BlockPushSameday", "BlockPushAfterDays", 
		"OS", "OSVersion", "RevokePushTF", "RevokePushBefore", "RevokePushSameday", "RevokePushAfterDays", "SignIn", 
		"UninstalledTF", "UninstalledSameday", "UninstalledAfter", "ScreenWidth", "EmailExist", "EmailAddress", 
		"InstallDays", "PushCount", "Timezone", "UserType", "Questions", "CorrectQuestion"]
			numerical_arr_list = ["NumCampaignMatch","NumCrash","DailyUsage","InstallDays",
	"PushCount","Questions","CorrectQuestion", "BlockPushAfterDays", "RevokePushAfterDays", "UninstalledAfter", "LastUpdateDays"]
	
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
			tow = "\n"+str(i)+": "+ att_name[i]
			
			f_w.write(tow+"\n")
			att_freqs = collections.Counter(data[i])
			tt = 0
			sum_ = 0
			count = 0
			for key, freq in att_freqs.items():
				tow = str((key, freq))
				if att_name[i] in numerical_arr_list:
					sum_ += int(key.strip())* freq
				f_w.write(tow+"\n")
				tt += freq
				count += freq
				
			tow = "sum = "+str(tt)
			f_w.write(tow+"\n")
			if att_name[i] in numerical_arr_list:
				tow = "avg = "+str(1.*sum_/count)
				f_w.write(tow+"\n")
				
			if tt!=len(data[0]):
				tow= "freq not equal original rows"
				f_w.write(tow+"\n")
		f_w.close()
		f_r.close()
	
feature_stat()
