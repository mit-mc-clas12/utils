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
import get_condor_q
import get_args
import fs
import utils
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

def create_json_dict(args):
    db_conn, sql = connect_to_database(args.lite)

    condor_info = get_condor_q.get_condor_q(args)

    batch_ids = condor_info[0]
    total_jobs_submitted = condor_info[1]
    total_jobs_running = condor_info[2]
    idle_jobs = condor_info[3]
    running_jobs = condor_info[4]
    jobs_start_dates = condor_info[5]

    footer_placeholder_text = "Total for all users: 14598 jobs; 0 completed, 0 removed, 12378 idle, 1903 running, 317 held, 0 suspended"
    footer = footer_placeholder_text
    json_dict = {}
    json_dict['metadata'] = {
        'update_timestamp': gettime(),
        'footer': footer,
    }
    json_dict['user_data'] = []


    for index,osg_id in enumerate(batch_ids):
            jobs_total = total_jobs_submitted[index]
            jobs_done = jobs_total - total_jobs_running[index]
            jobs_idle = idle_jobs[index]
            jobs_running = running_jobs[index]
            jobs_start = utils.unixtimeconvert(jobs_start_dates[index])

            sql.execute("SELECT COUNT(pool_node) FROM submissions WHERE pool_node = {}".format(osg_id))
            count = sql.fetchall()[0][0]
            print("count is {0}".format(count))

            #I dont get exactly what is going on here. How can we have a zero in the DB but nonzero  in condor?
            #looking at this more, it is only 1 if exists in db, or 0 if not in db
            if count > 0:
                # Get information from database to connect with this job
                sql.execute("SELECT user,user_submission_id FROM submissions WHERE pool_node = {}".format(osg_id))
                user, farm_sub_id = sql.fetchall()[0]

                user_info = [user, farm_sub_id, jobs_start, jobs_total,jobs_done,jobs_running,jobs_idle,osg_id]

                user_data = {}
                for index,key in enumerate(fs.user_data_keys):
                    user_data[key] = user_info[index]

                user_data = enforce_preferential_key_ordering(user_data, fs.user_data_keys)
                json_dict['user_data'].append(user_data)

            else:
                print('Skipping {}'.format(osg_id))

    db_conn.close()

    # Nothing was added
    if not json_dict['user_data']:
        user_data = {}
        for index,key in enumerate(fs.user_data_keys):
            user_data[key] = fs.null_user_info[index]

        json_dict['user_data'].append(enforce_preferential_key_ordering(user_data,fs.user_data_keys))

    return json_dict

if __name__ == '__main__':
    args = get_args.get_args()

    json_dict = create_json_dict(args)

    args.OutputDir = fs.default_osg_json_log if args.OutputDir == 'none' else args.OutputDir
    with open(args.OutputDir, 'w') as output_file:
        json.dump(json_dict, output_file, indent=4)
