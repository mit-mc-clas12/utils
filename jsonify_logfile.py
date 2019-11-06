"""

Logfile jsonification for monitoring. 

"""

import json 
import os 
import sys 

import argparse 

# This project 
import fs
from database import (get_database_connection, 
                      load_database_credentials)
from utils import gettime 

USER_QUERY = """
SELECT User from UserSubmissions 
WHERE UserSubmissionID IN 
(SELECT UserSubmissionID FROM FarmSubmissions 
WHERE pool_node = {}
)
"""

def connect_to_database():

    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)

    # Manual injection of username and password, still
    # not quite ideal. 
    fs.mysql_uname = uname
    fs.mysql_psswrd = pword
    
    return get_database_connection() 

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
        
    log_text = [line.strip().split() for line in log_text]

    header = log_text[0]
    footer = log_text[-1]

    json_dict = {} 
    json_dict['metadata'] = {
        'update_timestamp': logtime,
        'jobs': footer[0],
        'completed': footer[2],
        'removed': footer[4],
        'idle': footer[6],
        'running': footer[8],
        'held': footer[10],
        'suspended': footer[12]
    }
    json_dict['user_data'] = [] 

    # Example Header 
    # ['SUBMITTED', 'DONE', 'RUN', 'IDLE', 'HOLD', 'TOTAL', 'JOB_IDS']

    # Example entry 
    # ['gemc', '11/4', '12:02', '999', '1', '_', '_', '1000', '1417876.13']


    for line_number, line in enumerate(log_text[1:-1]):
        if line:
            job_id = line[8].split('.')[0]
            
            sql.execute(USER_QUERY.format(job_id))
            user = sql.fetchall()[0][0]
            
            user_data = {} 
            user_data['username'] = user
            user_data['job_id'] = job_id
            user_data['submit_date'] = line[1]
            user_data['submit_time'] = line[2]
            user_data['submitted'] = line[3]
            user_data['done'] = line[4]
            user_data['total'] = line[7]

            json_dict['user_data'].append(user_data)

    # End by closing the database. 
    db_conn.close() 


    with open(args.output, 'w') as output_file:
        json.dump(json_dict, output_file, indent=4)
