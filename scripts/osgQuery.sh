#!/bin/csh -f

# creating osgLog.json inside /home/gemc/logs
cd /home/gemc/logs
setenv PYTHONPATH /home/gemc/software/Submit
python3 -m utils.gemc_json_logging
pelican object put osgLog.json osdf:///jlab-osdf/clas12/volatile/osg/osgLog.json
