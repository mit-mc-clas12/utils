import subprocess
import datetime
import json
from collections import OrderedDict

currentDT = datetime.datetime.now()

text=subprocess.Popen(['ssh','t3home000.mit.edu','~/farmnodes.sh'], stdout=subprocess.PIPE)
string=text.communicate()[0]
array=string.split(' ',2)
array[2]=array[2].split('\n')[0]

dic =OrderedDict([('farm','MIT'),('Total cores',array[0]),('Busy cores',array[1]),('Idle cores',array[2]),('timestamp',currentDT.strftime("%Y-%m-%d %H:%M:%S"))])
with open('../stats_results/stats_MIT.json', 'w') as outfile:
    json.dump(dic, outfile)