"""
Priority calculation for users. 
"""

import argparse 
import datetime
import json 
import os 
import subprocess
import sys 
from copy import deepcopy

# This project 
from database import (get_database_connection, 
                      load_database_credentials)

def connect_to_database():
    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)
    return get_database_connection(use_mysql=True, username=uname, password=pword,
                                   hostname='jsubmit.jlab.org', database_name="CLAS12OCR") 

def weight_time_sort(items_, weights_, times_):
    """ A version of insertion sort modified to 
    do a sort based on weight but break ties
    with times. Algorithm is O(n**2) time complex
    but our user base is so small, it doesn't matter.

    Inputs: 
    -------
    - items - some items that you want sorted according to 
    the weights given and times given (list)
    - weights - list of weights between 0, 1
    - times - unix times 

    Returns:
    --------
    sorted list of items

    """

    assert(len(weights_) == len(times_))
    assert(len(weights_) == len(items_))

    items = deepcopy(items_)
    weights = deepcopy(weights_)
    times = deepcopy(times_)

    out_items = []
    out_weights = []
    out_times = []
    while items:

        big_index = 0 
        for index, (i,w,t) in enumerate(zip(items, weights, times)):
            if w > weights[big_index]:
                big_index = index
            elif w == weights[big_index]:
                if t < times[big_index]:
                    big_index = index

        out_items.append(items.pop(big_index))
        out_weights.append(weights.pop(big_index))
        out_times.append(times.pop(big_index))
        
    return out_items, out_weights, out_times

if __name__ == '__main__':

    ap = argparse.ArgumentParser() 
    ap.add_argument('-j', '--jsonfile', required=True)
    ap.add_argument('-d', '--debug', action='store_true')
    ap.add_argument('-u', '--update', action='store_true')
    args = ap.parse_args()

    # Connect to our database with read/write access. 
    db_conn, sql = connect_to_database() 

    with open(args.jsonfile, 'r') as json_log:
        data = json.load(json_log)

    jobs = {}
    for user in data['user_data']:
        if user['user'] in jobs:
            jobs[user['user']]['njobs'] += int(user['run'])
            jobs[user['user']]['ids'].append(int(user['osg id']))
        else:
            jobs[user['user']] = {}
            jobs[user['user']]['njobs'] = 0
            jobs[user['user']]['ids'] = []
            jobs[user['user']]['njobs'] += int(user['run'])
            jobs[user['user']]['ids'].append(int(user['osg id']))
            jobs[user['user']]['submit_time'] = user['submitted']
            
    for user in jobs:
        query = """
        SELECT priority FROM users
        WHERE user = '{0}'
        """.format(user)
        sql.execute(query)

        jobs[user]['priority'] = int(sql.fetchall()[0][0])

    items = [(u,jobs[u]['ids']) for u in jobs]
    weights = [] 
    for user in jobs:
        if jobs[user]['njobs'] > 0:
            weights.append(float(jobs[user]['priority']) / float(jobs[user]['njobs']))
        else:
            weights.append(float(jobs[user]['priority']))

    time_format = '%m/%d %H:%M'
    times = [datetime.datetime.strptime(jobs[u]['submit_time'], time_format) 
             for u in jobs]

    sorted_items, sorted_weights, sorted_times = weight_time_sort(
        items, weights, times
    )
    ranking = range(len(sorted_weights), 0, -1)

    if args.debug:
        print(sorted_items)
        print(sorted_weights)
        print(ranking)
    else:
        for (user, job_ids), rank in zip(sorted_items, ranking):
            for job_id in job_ids:
                print('condor_prio +{} {}'.format(rank, job_id))

    #if args.update:
    #    for (u,_),w,r in zip(sorted_items, sorted_weights, ranking):
    #        command = """
    #        UPDATE users SET (total_running_jobs, priority_weight, condor_rank)
    #        = ({},{},{}) WHERE user = '{}';
    #        """.format()

    db_conn.close()
    

