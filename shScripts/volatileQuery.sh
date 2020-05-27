#!/bin/csh -f

# Crontab command for every 4 hours at the 44 minute
# 44 */4 * * * ~/volatileQuery.sh 

### going to web interface stats_results
rm /group/clas/www/gemc/html/web_interface/stats_results/volatile.log
cd /volatile/clas12/osg
nice +20 du -B G -d 2 -t 1 | grep -v lund | grep -v gemc | grep -v test > /group/clas/www/gemc/html/web_interface/stats_results/volatile.log
cd /group/clas/www/gemc/html/web_interface/stats_results/
python /group/clas12/SubMit/utils/jsonify_disk_usage.py --logfile volatile.log --output disk.json
