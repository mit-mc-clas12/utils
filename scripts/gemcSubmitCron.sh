#!/bin/bash

scriptDir=/home/gemc/software/Submit/server/src
scriptDirT=/home/gemc/software/Submit/test/server/src

python3 $scriptDir/Submit_UserSubmission.py -s
python3 $scriptDirT/Submit_UserSubmission.py -s -t --test_database
