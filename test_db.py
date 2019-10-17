#!/usr/bin/env python 

from utils import (establish_database_connection, 
                   load_database_credentials)

if __name__ == '__main__':

    creds_file = '../msqlrw.txt'
    uname, pword = load_database_credentials(creds_file)
    db_connection, sql = establish_database_connection(uname, pword) 

    # A simple test query
    query = """ 
    SELECT User, timestamp FROM UserSubmissions 
        WHERE UserSubmissionID > 65 AND User = 'dmriser';
    """
    sql.execute(query)
    result = sql.fetchall()
    print(result)
    
    # User is responsible for closing the database before 
    # exiting the program. 
    db_connection.close() 
