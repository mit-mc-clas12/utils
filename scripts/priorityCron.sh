#!/bin/csh -f

# Crontab command for every 1 minute 
# */5 * * * * ~/priorityCron.sh >& ~/priorityCron.log

# check if we're already running
ps -ef | grep gemc | grep priorityCron | grep -v grep | grep -v nano 

set nrunning =  `ps -ef | grep gemc | grep priorityCron | grep -v grep | grep -v nano | wc | awk '{print $1}'`

# running this cronjob abounts for 2 of the above running
if ($nrunning != "2") then
        echo running: $nrunning                                       
	echo priorityCron already running. Nothing to do. 
else
	python /group/clas12/SubMit/utils/update_priority.py -j /u/group/clas/www/gemc/html/web_interface/data/osgLog.json -u | xargs -n3 condor_prio
endif


