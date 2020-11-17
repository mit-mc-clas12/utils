#!/bin/csh -f

# Crontab command for every 4 hours at the 44 minute
# 44 */4 * * * ~/volatileQuery.sh 


# check if we're already running
ps -ef | grep gemc | grep volatileQuery | grep -v grep | grep -v nano

set nrunning =  `ps -ef | grep gemc | grep volatileQuery | grep -v grep | grep -v nano | wc | awk '{print $1}'`

# running this cronjob abounts for 2 of the above running
if ($nrunning != "2") then
	echo running: $nrunning
	echo volatileQuery already running. Nothing to do.
else
	set dataDir   = /group/clas/www/gemc/html/web_interface/data
	set scriptDir = /group/clas12/SubMit/utils/
	set osgOutput = /volatile/clas12/osg

	if($1 == 'test') then
		echo running test
		set dataDir   = /group/clas/www/gemc/html/test/web_interface/data
		set scriptDir = /group/clas12/SubMit/test/SubMit/utils/
	endif

	### going to web interface data
	rm $dataDir/volatile.log
	cd $osgOutput

	# du takes too long
	# nice +20 du -B G -d 2 -t 1 | grep -v lund | grep -v gemc | grep -v test

	find -maxdepth 2 -type d -ls | awk '{print $11}' > $dataDir/volatile.log

	cd $dataDir
	pwd
	# python $scriptDir/jsonify_disk_usage.py --logfile volatile.log --output disk.json

endif


