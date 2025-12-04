#!/bin/bash

# Renew the token
/home/gemc/sw/utilities/osg/bin/token-renew

# Run the command and extract the total for query using grep and awk
total=$(condor_q -totals | grep "Total for query:" | awk '{print $4}')

# Check if the extracted number is greater than 80,000
if [ "$total" -gt 80000 ]; then
    echo "Total jobs in queue is greater than 80,000"
    echo "Skipping submission"
    exit 0
else
    echo "Total jobs in queue: $total"
    echo "Submitting 1 job..."
fi

scriptDirT=/home/gemc/software/Submit/test/server/src
scriptDir=/home/gemc/software/Submit/server/src

python3 $scriptDirT/Submit_UserSubmission.py -s -t --test_database
python3 $scriptDir/Submit_UserSubmission.py -s
