"""
Logfile jsonification for monitoring. 
"""

import argparse 
import json 
import os 
import sys 
from collections import OrderedDict 

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

COLS_TO_SPLIT = ['SUBMITTED', 'BATCH_NAME']
COLS_TO_SKIP = ['BATCH_NAME', 'OWNER', 'JOB_IDS']
    
def connect_to_database():

    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)

    return get_database_connection(use_mysql=True, username=uname, password=pword,
                                   hostname='jsubmit.jlab.org', database_name="CLAS12OCR") 

def build_user_data(columns, line, user, osg_id, farm_sub_id):
    """
    Sample input from the logfile.  This output is not standard, sometimes
    the hold column is missing.  For that reason, there is an if statement 
    on the length of the line.
    """
    user_data = OrderedDict() 
    
    icol = 0 
    for col in columns:

        if col in COLS_TO_SPLIT:
            entry = ' '.join(line[icol:icol+2])
            icol += 2
        else:
            entry = line[icol]
            icol += 1 

        if col not in COLS_TO_SKIP:
            user_data[col] = entry

    user_data['USER'] = user
    user_data['OSG ID'] = osg_id
    return user_data

def build_dummy_user_data(columns):

    user_data = OrderedDict() 
    for col in columns:
        user_data[col] = "No data"

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
    log_text = [l for l in log_text if l]
    columns = log_text[0]
    footer = log_text[-1]

    json_dict = {} 
    json_dict['metadata'] = {
        'update_timestamp': logtime,
        'footer': ' '.join(footer),
    }
    json_dict['user_data'] = [] 

    # Don't read header/columns/footer 
    for line in log_text[1:-1]:
        
        # Don't process empty lists 
        if line:
            line = [l.replace('_','0') for l in line]
            osg_id = line[-1].split('.')[0]

            sql.execute("SELECT COUNT(pool_node) FROM FarmSubmissions WHERE pool_node = {}".format(
                osg_id
            ))
            count = sql.fetchall()[0][0]

            if count > 0:
                # Get information from database to connect with this job
                sql.execute(USER_QUERY.format(osg_id))
                user, farm_sub_id = sql.fetchall()[0]
                user_data = build_user_data(columns, line, user, osg_id, farm_sub_id)
                json_dict['user_data'].append(user_data)

            else:
                print('Skipping {}'.format(osg_id))

    db_conn.close() 

    # Nothing was added 
    if not json_dict['user_data']:
        json_dict['user_data'].append(build_dummy_user_data(columns))
    
    with open(args.output, 'w') as output_file:
        json.dump(json_dict, output_file, indent=4)
