

import pygeoip, sys

gi = pygeoip.GeoIP('GeoLiteCity.dat')

for line in sys.stdin:
	rec = gi.record_by_addr(line)
	rec = gi.record_by_addr(line)
	print rec['country_name']
	
