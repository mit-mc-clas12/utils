#!/bin/csh -f

# Crontab command for every 2 minutes
# */2 * * * * flock -n $HOME/.submit.lock $HOME/gemcSubmitCron.sh >& $HOME/submitCron.log

cd /group/clas12/SubMit/server
python src/Submit_UserSubmission.py -s
