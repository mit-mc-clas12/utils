import subprocess
import datetime
import re
import json
from collections import OrderedDict

currentDT = datetime.datetime.now()

a=subprocess.Popen("/site/scicomp/auger-slurm/bin/slurmHosts",stdout=subprocess.PIPE)
b= a.communicate()[0]
available=0
total=0
state='DEFAULT'
c=re.split('684|1563|771|308|332',b)
for i, array in enumerate(c):
	content=array.split()
	if i==0:
		state=content[-1]
		continue
	if len(content)==1:
		continue
	job=content[1]
	total=total+int(job.split('/')[1])
	if state=='IDLE' or state=='MIXED':
		available=available+int(job.split('/')[0])
	state=content[-1]
	
dic =OrderedDict([('farm','JLab'),('Total cores',str(total)),('Busy cores',str(total-available)),('Idle cores',str(available)),('timestamp',currentDT.strftime("%Y-%m-%d %H:%M:%S"))])
with open('../data/stats_jlab.json', 'w') as outfile:
    json.dump(dic, outfile)
