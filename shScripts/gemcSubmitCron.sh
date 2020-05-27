#!/bin/csh -f

# Crontab command for every 1 minute 
# */1 * * * * ~/gemcSubmitCron.sh >& ~/submitCron.log

# check if we're already running
ps -ef | grep gemc | grep gemcSubmitCron | grep -v grep | grep -v nano 

set nrunning =  `ps -ef | grep gemc | grep gemcSubmitCron | grep -v grep | grep -v nano | wc | awk '{print $1}'`

# running this cronjob abounts for 2 of the above running
if ($nrunning != "2") then
        echo running: $nrunning                                       
	echo gemcSubmitCron already running. Nothing to do. 
else
	cd /group/clas12/SubMit/server
	python src/Submit_UserSubmission.py -s  
endif
