"""
Tool for inspecting things in the 
database. 
"""

import argparse
import os 

# This project                                                                                                                                           
import fs
from database import (get_database_connection,
                      load_database_credentials)

def connect_to_database():
    creds_file = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../msqlrw.txt')
    uname, pword = load_database_credentials(creds_file)
    return get_database_connection(use_mysql=True, username=uname, password=pword,
                                   hostname='jsubmit.jlab.org', database_name="CLAS12OCR")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--submission', type=int, required=True)
    parser.add_argument('--show_scard', action='store_true')
    args = parser.parse_args()

    db_conn, sql = connect_to_database()
    
    if args.show_scard:
        sql.execute("SELECT scard FROM UserSubmissions WHERE UserSubmissionID = {}".format(
            args.submission))
        data = sql.fetchall()[0][0]
        print(data)

    db_conn.close()
