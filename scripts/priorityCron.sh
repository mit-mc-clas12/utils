#!/bin/csh -f

# Crontab command for every 1 minute 
# */5 * * * * flock -n $HOME/.osgpriority.lock  $HOME/priorityCron.sh >& $HOME/priorityCron.log

python /home/gemc/software/SubMit/utils/update_priority.py -j /u/group/clas/www/gemc/html/web_interface/data/osgLog.json -u | xargs -n3 condor_prio



