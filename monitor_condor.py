"""
Using the results of condor_q -submitter gemc
populate the database table called job_queue.
"""

import argparse 
import os 
import subprocess
import sys 
from collections import OrderedDict 

# This project 
import fs
from database import (get_database_connection, 
                      load_database_credentials)
from utils import gettime 

USER_QUERY = """
SELECT user,user_submission_id FROM submissions 
WHERE pool_node = {}
"""

COLS_TO_SPLIT = ['submitted', 'batch_name']
COLS_TO_SKIP = ['batch_name', 'owner', 'job_ids']
ORDERING = ['user', 'job id', 'submitted', 'total',
            'done', 'run', 'idle', 'hold', 
            'osg id']    

def connect_to_database(database_name='CLAS12TEST'):

    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)

    return get_database_connection(use_mysql=True, username=uname, password=pword,
                                   hostname='jsubmit.jlab.org', database_name=database_name) 

def build_user_data(columns, line, user, job_id, osg_id, farm_sub_id):
    """
    Sample input from the logfile.  This output is not standard, sometimes
    the hold column is missing.  For that reason, there is an if statement 
    on the length of the line.
    """
    user_data = {}
    
    icol = 0 
    for col in columns:

        col = col.lower() 
        if col in COLS_TO_SPLIT:
            entry = ' '.join(line[icol:icol+2])
            icol += 2
        else:
            entry = line[icol]
            icol += 1 

        if col not in COLS_TO_SKIP:
            user_data[col] = entry

    user_data['user'] = user
    user_data['osg id'] = osg_id
    user_data['job id'] = job_id
    return user_data

def build_dummy_user_data(columns):

    user_data = {}
    for col in columns:
        user_data[col.lower()] = "No data"

    user_data['user'] = "No user"
    user_data['osg id'] = "No ID"
    user_data['job id'] = "No ID"
    return user_data

def enforce_preferential_key_ordering(input_data, ordering):
    """ Order the keys of a dictionary according 
    to some prefered scheme. """
    data = OrderedDict() 

    for key in ordering:
        if key in input_data:
            data[key] = input_data[key]
    
    # Anything that doesn't have a preferential order. 
    for key in input_data:
        if key not in data:
            data[key] = input_data[key]

    return data

def extract_osg_id(line):
    return line[-1].split('.')[0] + '.'

if __name__ == '__main__':

    ap = argparse.ArgumentParser() 
    args = ap.parse_args()

    # Connect to our database with read/write access. 
    db_conn, sql = connect_to_database() 

    logtime = gettime() 
    log_output = subprocess.check_output(['/usr/bin/condor_q', '-submitter', 'gemc'])
    log_text = [line.strip().split() for line in log_output.split('\n') if line]        
    columns = log_text[1]
    footer = log_text[-1]

    print(log_output)
    print(log_text)

    json_dict = {} 
    json_dict['metadata'] = {
        'update_timestamp': logtime,
        'footer': ' '.join(footer),
    }
    json_dict['user_data'] = [] 

    # Debug 
    sql.execute("SELECT pool_node FROM submissions")
    print(sql.fetchall())

    # Don't read header/columns/footer 
    for line in log_text[2:-1]:
        
        # Don't process empty lists 
        if line:
            line = [l.replace('_','0') for l in line]
            osg_id = extract_osg_id(line)

            sql.execute("SELECT COUNT(pool_node) FROM submissions WHERE pool_node = {}".format(
                osg_id
            ))
            count = sql.fetchall()[0][0]
            print("SELECT COUNT(pool_node) FROM submissions WHERE pool_node = {}".format(
                osg_id
            ))
            print(sql.fetchall())

            if count > 0:
                # Get information from database to connect with this job
                sql.execute(USER_QUERY.format(osg_id))
                user, farm_sub_id = sql.fetchall()[0]
                user_data = build_user_data(columns, line, user, 
                                            farm_sub_id, osg_id, farm_sub_id)
                user_data = enforce_preferential_key_ordering(user_data, ORDERING)
                json_dict['user_data'].append(user_data)

            else:
                print('Skipping {}'.format(osg_id))

    db_conn.close() 

    # Nothing was added 
    if not json_dict['user_data']:
        json_dict['user_data'].append(enforce_preferential_key_ordering(
            build_dummy_user_data(columns), ORDERING))
    
    print(json_dict)
