import json
from collections import OrderedDict


str = "[\n"
for files in ['stats_osg.json','stats_MIT.json','stats_jlab.json']:
	with open('../data/'+files,'r') as jsondata:
		str += jsondata.readline()+",\n"

str = str[:-2]
str += "\n]"

writefile = open('../data/stats.json','w')
writefile.write(str)
writefile.close()
