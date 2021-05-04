#!/bin/csh -f

# Crontab command for every 2 minute
# */2 * * * * flock -n $HOME/.jlog.lock $HOME/osgQuery.sh 

set dataDir   = /group/clas/www/gemc/html/web_interface/data
set scriptDir = /group/clas12/SubMit/utils/


### going to web interface data
cd $dataDir

# parsing onto gemcRunning.log osgLog.json
python $scriptDir/gemc_json_logging.py
