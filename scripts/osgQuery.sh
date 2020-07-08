#!/bin/csh -f

# Crontab command for every 2 minute
# */2 * * * * ~/osgQuery.sh

## This file should be modified to only include the following command:
##  python /group/clas12/SubMit/utils/gemc_json_logging.py
## the default output file, as specified in the "Other Specifications" section of fs.py, is osgLog.json

set dataDir   = /group/clas/www/gemc/html/web_interface/data
set scriptDir = /group/clas12/SubMit/utils/

if($1 == 'test') then
	echo running test
	set dataDir   = /group/clas/www/gemc/html/test/web_interface/data
	set scriptDir = /group/clas12/SubMit/test/SubMit/utils/
endif

mkdir -p $dataDir

### going to web interface data
cd $dataDir
rm gemcRunning.log osgLog.json

# creates gemcRunning.log from condor_q
condor_q -submitter gemc | grep OWNER -A100 > gemcRunning.log

# parsing onto gemcRunning.log osgLog.json
python $scriptDir/jsonify_logfile.py --logfile=gemcRunning.log --output=osgLog.json
