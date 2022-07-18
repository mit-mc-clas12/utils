#!/bin/bash

# cd /home/gemc/software/Submit//utils/scardTests
# ./runTests.sh

gcards="rga_fall2018_bgmerging.txt rga_fall2018_nobg.txt   rga_spring2018_nobg.txt   rgb_spring2019_nobg.txt  \
        rgk_fall2018_FTOn_nobg.txt rga_spring2019_nobg.txt rgk_fall2018_FTOff_nobg.txt"

cd /group/clas/www/gemc/html/test/web_interface

for scard in $gcards
do
	echo
	cp /home/gemc/software/Submit/test/SubMit/utils/scardTests/$scard scard_type2.txt
	echo Submitting $scard to test database
	../SubMit/client/src/SubMit.py --test_database -u ungaro scard_type2.txt
done

echo
echo Submitting Jobs to OSG
cd /home/gemc/software/Submit//test/SubMit/server/
python3 src/Submit_UserSubmission.py -s -t --test_database
echo

# Output:
# job_91/output/simu_0/   rga_fall2018_bgmerging
# job_92/output/simu_0/   rga_fall2018_nobg
# job_93/output/simu_0/   rga_spring2018_nobg
# job_94/output/simu_0/   rgb_spring2019_nobg
# job_95/output/simu_0/   rgk_fall2018_FTOn_nobg
# job_96/output/simu_0/   rga_spring2019_nobg
# job_97/output/simu_0/   rgk_fall2018_FTOff_nobg



