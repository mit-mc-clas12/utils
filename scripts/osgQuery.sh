#!/bin/csh -f

# Crontab command for every 2 minute
# */2 * * * * ~/osgQuery.sh

##This file should be modified to only include the following command:
#python /group/clas12/SubMit/utils/gemc_json_logging.py
## the default output file, as specified in the "Other Specifications" section of fs.py, is osgLog.json


### going to web interface data
cd /group/clas/www/gemc/html/web_interface/data
rm gemcRunning.log osgLog.json

condor_q -submitter gemc | grep OWNER -A100 > gemcRunning.log
python /group/clas12/SubMit/utils/jsonify_logfile.py --logfile=gemcRunning.log --output=osgLog.json
