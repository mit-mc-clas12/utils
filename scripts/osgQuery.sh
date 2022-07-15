#!/bin/csh -f

# creating osgLog.json inside /home/gemc/logs
cd /home/gemc/logs
python3 /home/gemc/software/Submit/utils/gemc_json_logging.py
scp osgLog.json dtn1902:/lustre19/expphy/volatile/clas12/osg2/

