#!/bin/zsh

sg=/home/gemc/software/simGrid/main

# creating osgLog.json inside /home/gemc/logs
cd /home/gemc/logs
export PYTHONPATH=/home/gemc/software/Submit
python3 -m utils.gemc_json_logging
$sg/condor_io/list_owner_submission.py -q -c ~/software/Submit/msql_conn.txt  -dev -j osg-devel.json
$sg/condor_io/list_owner_submission.py -q -c ~/software/Submit/msql_conn.txt       -j osg-production.json

pelican object put osgLog.json         osdf:///jlab-osdf/clas12/volatile/osg/osgLog.json
pelican object put osg-devel.json      osdf:///jlab-osdf/clas12/volatile/osg/osg-devel.json
pelican object put osg-production.json osdf:///jlab-osdf/clas12/volatile/osg/osg-production.json
