import subprocess
import datetime
import json
from collections import OrderedDict

currentDT = datetime.datetime.now()

text=subprocess.Popen(['../stats_raw/osg/farmnodes.sh'], stdout=subprocess.PIPE)
string=text.communicate()[0]
array=string.split(' ',2)

dic =OrderedDict([('farm','osg'),('Total cores',array[0]),('Busy cores',array[1]),('Idle cores',array[2]),('timestamp',currentDT.strftime("%Y-%m-%d %H:%M:%S"))])
with open('../data/stats_osg.json', 'w') as outfile:
    json.dump(dic, outfile)
