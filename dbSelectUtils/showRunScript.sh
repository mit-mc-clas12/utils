#!/bin/bash 

#!/bin/bash

submissionID=$1

echo
echo Downloading clas12_condor_text with submissionID: $submissionID
echo

mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT runscript_text FROM CLAS12OCR.FarmSubmissions where FarmSubmissionID = $submissionID;" | awk '{gsub(/\\n/,"\n")}1' | awk '{gsub(/\\t/,"\t")}1'
