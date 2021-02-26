#!/bin/csh -f

echo
echo Ticket:
echo https://support.opensciencegrid.org/support/home
echo Subject: report of problems on site CRUSH
echo

rm -f ~/oasisMissing.txt
grep "Transport endpoint is not connected" log/*.err | awk -F. '{print $3}' | sort -u > ~/oasisMissing.txt

echo
echo Jobs with missing oasis:
cat ~/oasisMissing.txt
echo

foreach j ( `cat ~/oasisMissing.txt` )
	grep JOB_GLIDEIN_SiteWMS_Slot log/job*.$j".log" | tail -1
end
