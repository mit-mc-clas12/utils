# Testing portal and scripts


https://gemc.jlab.org/test/web_interface/index.php


grepo = https://github.com/mit-mc-clas12

web_portal = /group/clas/www/gemc/html/test

## On web_portal:

clone or update $grepo/web_interface

## On web_portal/Submit

clone or update $grepo/utils, client


## On scosg22:



set test_dir = /home/gemc/software/Submit/test

clone or update $grepo/utils, client, server

make sure msql_conn_test.txt is in $test_dir



	To submit to OSG:

	 cd /home/gemc/software/Submit/test/server/
	 python3 src/Submit_UserSubmission.py -s -t --test_database
	 
	 
	 

## Tips:


- If mysql table are changed:

	- mysql backup
	- alter table CLAS12OCR.submissions auto_increment = 220;
	- copy users tables into new one




