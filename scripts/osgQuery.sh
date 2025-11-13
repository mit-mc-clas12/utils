#!/bin/csh -f

# creating osgLog.json inside /home/gemc/logs
cd /home/gemc/logs
python3 /home/gemc/software/Submit/utils/gemc_json_logging.py
pelican object put osgLog.json osdf:///jlab-osdf/clas12/volatile/osg/osgLog.json

#scp osgLog.json dtn1902:/lustre/expphy/volatile/clas12/osg/
