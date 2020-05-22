#!/bin/csh -f

# Crontab command for every 1 minute 
# */10 * * * * ~/osgStats.sh 

### going to web interface stats_results
cd /group/clas/www/gemc/html/web_interface/stats_results
rm gemcRunning.log osgLog.json

condor_q -submitter gemc > gemcRunning.log
python /group/clas12/SubMit/utils/jsonify_logfile.py --logfile=gemcRunning.log --output=osgLog.json
