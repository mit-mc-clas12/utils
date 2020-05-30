"""
Logfile jsonification for monitoring.
"""

import argparse
import json
import os
import sys
from collections import OrderedDict
import htcondor
import classad

# This project
import fs
from database import (get_database_connection,
                      load_database_credentials)
from utils import gettime

def connect_to_database(sqlite_db_name):

    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)

    mysql=True
    db_name="CLAS12OCR"
    if sqlite_db_name != None:
        mysql=False
        db_name = "CLAS12OCR.db"

    return get_database_connection(use_mysql=mysql, username=uname, password=pword,
                                   hostname='jsubmit.jlab.org', database_name=db_name)

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


def get_htcondor_q():
    batch_ids = []
    num_jobs = []
    qdates = []
    total_jobs = []
    done_jobs = []
    running_jobs = []
    idle_jobs = []

    schedd = htcondor.Schedd()

    for job in schedd.xquery():
            if job.get("owner") == "gemc":
                batch_id = str(job.get("ClusterID"))
                if batch_id in batch_ids:
                    num_jobs[batch_ids.index(batch_id)] +=1 #increment number of jobs
                else:
                    batch_ids.append(batch_id)
                    num_jobs.append(1)


    return batch_ids, num_jobs

if __name__ == '__main__':


    USER_QUERY = """
    SELECT user,user_submission_id FROM submissions
    WHERE pool_node = {}
    """

    COLS_TO_SPLIT = ['submitted', 'batch_name']
    COLS_TO_SKIP = ['batch_name', 'owner', 'job_ids']
    ORDERING = ['user', 'job id', 'submitted', 'total',
                'done', 'run', 'idle', 'hold',
                'osg id']


    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--output', required=False, default="osgLog.json")
    ap.add_argument('-q', '--lite', required=False)
    args = ap.parse_args()

    # Connect to our database with read/write access.
    db_conn, sql = connect_to_database(args.lite)

    users, jobs = get_htcondor_q()

    columns = ['OWNER', 'BATCH_NAME', 'SUBMITTED', 'DONE', 'RUN', 'IDLE', 'TOTAL', 'JOB_IDS']

    logtime = gettime()
    footer_placeholder_text = "Total for all users: 14598 jobs; 0 completed, 0 removed, 12378 idle, 1903 running, 317 held, 0 suspended"
    footer = footer_placeholder_text

    json_dict = {}
    json_dict['metadata'] = {
        'update_timestamp': logtime,
        'footer': ' '.join(footer),
    }
    json_dict['user_data'] = []

    for osg_id in users:

            sql.execute("SELECT COUNT(pool_node) FROM submissions WHERE pool_node = {}".format(osg_id))
            count = sql.fetchall()[0][0]

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

    with open(args.output, 'w') as output_file:
        json.dump(json_dict, output_file, indent=4)
