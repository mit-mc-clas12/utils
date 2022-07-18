#!/bin/bash

# Crontab command for every 1 minute 
# */5 * * * * flock -n $HOME/.osgpriority.lock  $HOME/priorityCron.sh >& $HOME/priorityCron.log

python3 /home/gemc/software/Submit/utils/update_priority.py -j /home/gemc/logs/osgLog.json -u | xargs -n3 condor_prio



