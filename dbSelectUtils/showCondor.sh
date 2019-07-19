#!/bin/bash

submissionID=$1

echo
echo Downloading clas12_condor_text with submissionID: $submissionID
echo

mysql --defaults-extra-file=msql_conn.txt -N -s --execute="SELECT clas12_condor_text FROM CLAS12OCR.Submissions where submissionId = $submissionID;" | awk '{gsub(/\\n/,"\n")}1'
