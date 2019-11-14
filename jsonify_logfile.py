"""
Logfile jsonification for monitoring. 
"""

import json 
import os 
import sys 
from collections import OrderedDict 

import argparse 

# This project 
import fs
from database import (get_database_connection, 
                      load_database_credentials)
from utils import gettime 

USER_QUERY = """
SELECT User,FarmSubmissionID FROM UserSubmissions 
INNER JOIN FarmSubmissions ON FarmSubmissions.UserSubmissionID = UserSubmissions.UserSubmissionID
WHERE FarmSubmissions.pool_node = {}
"""

def connect_to_database():

    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)

    # Manual injection of username and password, still
    # not quite ideal. 
    fs.mysql_uname = uname
    fs.mysql_psswrd = pword
    
    return get_database_connection() 

def build_user_data(line, user, osg_id, farm_sub_id):
    """
    Sample input from the logfile.  This output is not standard, sometimes
    the hold column is missing.  For that reason, there is an if statement 
    on the length of the line.

    SUBMITTED   DONE   RUN    IDLE   HOLD  TOTAL JOB_IDS
    gemc        11/4  16:55    239      5      _      _    244 1417932.64
    gemc        11/6  12:50     43    956      _      1   1000 1422770.0-
    gemc        11/6  14:22      4   1571   1424      1   3000 1423098.0-

    """
    user_data = OrderedDict() 
    user_data['username'] = user
    user_data['job_id'] = farm_sub_id
    user_data['submitted'] = ' '.join(line[1:3])

    if len(line) > 8:
        user_data['total'] = line[7]
    else:
        user_data['total'] = line[6]

    user_data['done'] = line[3]
    user_data['running'] = line[4]
    user_data['idle'] = line[5]

    if len(line) > 8:
        user_data['hold'] = line[6]
    else:
        user_data['hold'] = 0

    user_data['osg_id'] = osg_id
    return user_data

def build_dummy_user_data():

    user_data = OrderedDict() 
    user_data['username'] = ''
    user_data['job_id'] = ''
    user_data['submitted'] = ''
    user_data['total'] = 0
    user_data['done'] = 0
    user_data['running'] = 0
    user_data['idle'] = 0
    user_data['hold'] = 0
    user_data['osg_id'] = 0
    return user_data
    

if __name__ == '__main__':

    ap = argparse.ArgumentParser() 
    ap.add_argument('-l', '--logfile', required=True)
    ap.add_argument('-o', '--output', required=True)
    args = ap.parse_args()

    # Connect to our database with read/write access. 
    db_conn, sql = connect_to_database() 

    logfile = args.logfile 
    logtime = gettime() 
    
    with open(logfile, 'r') as raw_log:
        log_text = raw_log.readlines()
        
    log_text = [l.strip().split() for l in log_text]
    header = log_text[0]
    footer = log_text[-1]

    json_dict = {} 
    json_dict['metadata'] = {
        'update_timestamp': logtime,
        'jobs': 0,
        'completed': 0,
        'idle': 0,
        'running': 0,
        'held': 0
    }
    json_dict['user_data'] = [] 

    # Don't read header/footer 
    for line in log_text[1:-1]:
        
        # Don't process empty lists 
        if line:
            line = [l.replace('_','0') for l in line]
            osg_id = line[7].split('.')[0]

            # Get information from database to connect with this job
            sql.execute(USER_QUERY.format(osg_id))
            user, farm_sub_id = sql.fetchall()[0]
            user_data = build_user_data(line, user, osg_id, farm_sub_id)
            json_dict['user_data'].append(user_data)

            json_dict['metadata']['jobs'] += int(user_data['total'])
            json_dict['metadata']['completed'] += int(user_data['done'])
            json_dict['metadata']['idle'] += int(user_data['idle'])
            json_dict['metadata']['held'] += int(user_data['hold'])
            json_dict['metadata']['running'] += int(user_data['running'])

    db_conn.close() 

    # Nothing was added 
    if not json_dict['user_data']:
        json_dict['user_data'].append(build_dummy_user_data())
    
    with open(args.output, 'w') as output_file:
        json.dump(json_dict, output_file, indent=4)
