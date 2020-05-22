#!/bin/csh -f

# Crontab command for every 1 minute 
# */2 * * * * ~/osgQuery.sh

### going to web interface stats_results
cd /group/clas/www/gemc/html/web_interface/stats_results
rm gemcRunning.log osgLog.json

condor_q -submitter gemc | grep OWNER -A100 > gemcRunning.log
python /group/clas12/SubMit/utils/jsonify_logfile.py --logfile=gemcRunning.log --output=osgLog.json
