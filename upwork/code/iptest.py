

import pygeoip, sys


machine = "aws"

if machine == "amm":
	prefix = "/home/amm/"
else:
	prefix = "/home/ubuntu/Desktop/sna_utcc/"
	
gi = pygeoip.GeoIP(prefix+"/upwork/data/GeoLiteCity.dat")

for line in ["68.80.169.17"]:
	rec = gi.record_by_addr(line)
 	print rec['country_name']
	
