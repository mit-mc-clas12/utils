"""

Priority calculation and database update. 

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

class PrioritizedUser:
    """ Simple class that tracks data for each user.
    It could be a namedtuple, but I wanted to add
    the weight calculation method here. """

    def __init__(self, username=None, submission_time=None, 
                 rank=None, priority=None, weight=None):
        self.username = username
        self.priority = priority
        self.rank = rank
        self.weight = weight
        self.submission_time = submission_time
        self.total_jobs = 0 
        self.idle_jobs = 0 
        self.jobs = []

    def calculate_weight(self):
        self.weight = self.priority
        if self.total_jobs > 0:
            self.weight = float(self.priority) / float(self.total_jobs)

def connect_to_database():
    """ Load the database login file and 
    get a read/write connection. """
    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)
    return get_database_connection(use_mysql=True, username=uname, password=pword,
                                   hostname='jsubmit.jlab.org', database_name="CLAS12OCR") 

def load_users_from_json(jsonfile):
    """ 
    This function reads the output of jsonify_logfile.py. 
    This could also be done directly with the output of 
    condor_q, which is the input to jsonify_logfile.py.  

    In this function, the users with multiple submissions
    are combined into one.  This is done so that we can 
    assign them a priority based on their total usage.

    Inputs: 
    -------
    - jsonfile (str) - path to the json file 

    Returns:
    --------
    - users (list(PrioritizedUser)) - A list of 
    users from the current usage.

    """
    with open(args.jsonfile, 'r') as json_log:
        data = json.load(json_log)

    jobs = {}
    for user in data['user_data']:
        if user['user'] in jobs:
            jobs[user['user']]['njobs'] += int(user['run'])
            jobs[user['user']]['idle'] += int(user['idle'])
            jobs[user['user']]['ids'].append(int(user['osg id']))
        else:
            jobs[user['user']] = {}
            jobs[user['user']]['njobs'] = 0
            jobs[user['user']]['idle'] = 0
            jobs[user['user']]['ids'] = []
            jobs[user['user']]['njobs'] += int(user['run'])
            jobs[user['user']]['idle'] += int(user['idle'])
            jobs[user['user']]['ids'].append(int(user['osg id']))
            jobs[user['user']]['submit_time'] = user['submitted']
    
    users = []

    time_format = '%m/%d %H:%M'
    for user in jobs:
        prio_user = PrioritizedUser(username=user)
        prio_user.submission_time = datetime.datetime.strptime(
            jobs[user]['submit_time'], time_format) 
        prio_user.total_jobs += jobs[user]['njobs']
        prio_user.idle_jobs += jobs[user]['idle']
        
        for j in jobs[user]['ids']:
            prio_user.jobs.append(j)
            
        users.append(prio_user)

    return users

def get_user_priority(user, sql):
    """ Get a users (static) priority from the
    database. """

    query = """
    SELECT priority FROM users
    WHERE user = '{0}'
    """.format(user)
    sql.execute(query)

    return int(sql.fetchall()[0][0])

def sort_and_rank_users(users_):
    """ A version of sort modified to 
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
    users = deepcopy(users_)
    sorted_users = []

    current_rank = len(users)
    while users:

        big_index = 0 
        big_user = users[0]
        for index, user in enumerate(users):
            if user.weight > big_user.weight:
                big_index = index
                big_user = user
            elif user.weight == big_user.weight:
                if user.submission_time < big_user.submission_time:
                    big_index = index
                    big_user = user

        users[big_index].rank = current_rank
        sorted_users.append(users.pop(big_index))
        current_rank -= 1

    return sorted_users

def demote_users_with_no_pending(users):
    """ For users with no pending jobs, 
    we can set their rank to zero. We also 
    then need to shift the user ranks. 

    Inputs:
    -------
    Users - List of PrioritizedUsers, modified
    inplace. 

    Returns: 
    --------
    Nothing - the list is modified
    """

    demoted_users = 0 
    for user in users:
        if user.idle_jobs == 0:
            user.rank = 0
            demoted_users += 1 
    
    rank = len(users) - demoted_users
    for user in users:
        if user.rank != 0:
            user.rank = rank
            rank -= 1 

def clear_database(db_conn, sql):
    """ Reset ranks to zero.  """
    query = """
    SELECT user FROM users
    """
    sql.execute(query)
    users = [tup[0] for tup in sql.fetchall()]

    for u in users:
        command = """
        UPDATE users SET priority_weight
        = {} WHERE user = '{}';
        """.format(0.0, u)
        sql.execute(command)
        
        command = """
        UPDATE users SET condor_rank
        = {} WHERE user = '{}';
        """.format(0, u)
        sql.execute(command)

        command = """
        UPDATE users SET total_running_jobs
        = {} WHERE user = '{}';
        """.format(0, u)
        sql.execute(command)
        db_conn.commit()

def update_database(users, db_conn, sql):
    """ Set database status variables based on the
    analysis in this script.  """
    for u in users:
        command = """
        UPDATE users SET priority_weight
        = {} WHERE user = '{}';
        """.format(u.weight, u.username)
        sql.execute(command)
        
        command = """
        UPDATE users SET condor_rank
        = {} WHERE user = '{}';
        """.format(u.rank, u.username)
        sql.execute(command)

        command = """
        UPDATE users SET total_running_jobs
        = {} WHERE user = '{}';
        """.format(u.total_jobs, u.username)
        sql.execute(command)
        db_conn.commit()

def print_debug(users):
    for user in users:
        print(user.username, user.weight, user.rank)

def print_commands(users):
    for user in users:
        for job_id in user.jobs:
            print('-p +{} {}'.format(user.rank, job_id))

def process_args():
    ap = argparse.ArgumentParser() 
    ap.add_argument('-j', '--jsonfile', required=True)
    ap.add_argument('-d', '--debug', action='store_true')
    ap.add_argument('-u', '--update', action='store_true')
    return ap.parse_args()

if __name__ == '__main__':

    args = process_args()
    db_conn, sql = connect_to_database() 
    users = load_users_from_json(args.jsonfile)

    for user in users:
        user.priority = get_user_priority(user.username, sql)
        user.calculate_weight()

    users = sort_and_rank_users(users)
    demote_users_with_no_pending(users)

    if args.debug:
        print_debug(users)
    else:
        print_commands(users)

    if args.update:
        clear_database(db_conn, sql)
        update_database(users, db_conn, sql)

    db_conn.close()
    

