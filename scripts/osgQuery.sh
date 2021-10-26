#!/bin/csh -f

set logDir    = /home/gemc/logs
set scriptDir = /home/gemc/software/Submit/utils

# creating osgLog.json inside $logDir
cd $logDir
python $scriptDir/gemc_json_logging.py
