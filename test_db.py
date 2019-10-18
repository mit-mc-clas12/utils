#!/usr/bin/env python 

import fs 
from database import (get_database_connection, 
                      load_database_credentials, get_users)

if __name__ == '__main__':

    creds_file = '../msqlrw.txt'
    uname, pword = load_database_credentials(creds_file)

    fs.mysql_uname = uname
    fs.mysql_psswrd = pword
    
    db_connection, sql = get_database_connection() 

    # A simple test query
    query = """ 
    SELECT User, timestamp FROM UserSubmissions 
        WHERE UserSubmissionID > 65 AND User = 'dmriser';
    """
    sql.execute(query)
    result = sql.fetchall()
    print(result)

    # Test function 
    users = get_users(sql)
    print(users)
    print(type(users))

    # User is responsible for closing the database before 
    # exiting the program. 
    db_connection.close() 
