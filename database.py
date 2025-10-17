"""

This module provides database configuration functions as well
as database read access functions.  Write access functions
for the client side live in client/update_tables.py.

"""


import datetime 

import fs
import sqlite3
import pymysql

def connect_to_mysql(host, username, password, db_name):
  """Return a MySQL database connection. """

  # print("username is {0}".format(username))
  if username == 'root':
    host='localhost' #This is so tests work on travis-ci, where we ue root user

  return pymysql.connect(host, username, password, db_name)

def connect_to_sqlite(db_name):
  """Return an sqlite database connection. """
  return sqlite3.connect(db_name)

def load_database_credentials(cred_file):
  """Read a file with database username and password and
  return a tuple. """
  with open(cred_file, 'r') as creds:

    # Ensure the file contents are on one line
    login = creds.read().replace('\n', ' ').split()

    if len(login) < 2:
      #raise ValueError(("Credential file must contain username and password,"
      #                  " separated by a space and nothing else."))
      return (login[0], "") #root user on travis-ci does not need password
      

    return (login[0], login[1])

def get_database_connection(use_mysql=True, hostname=None,
                            database_name=None, username=None,
                            password=None):
  """ 

  Authenticate to the database as done in the db_write and db_grab
  functions.  Returns an active database connection, this must be closed
  by the user.

  Inputs: 
  -------
  - use_mysql - (boolean) will configure sqlite or mysql 
  - hostname - (str) the database hostname 
  - username - (str) username loaded from file 
  - password - (str) password loaded from file 
  - database_name - (str) Database name, if using sqlite
  this should be the entire path to the database.  If the 
  database is MySQL, this should be the name of the table. 
  Valid options are "CLAS12OCR" for production or "CLAS12TEST"
  for testing. 

  Returns:
  --------
  db_connection - a MySQL or sqlite database connection
  sql - A cursor for the database, used to execute all queries

  """

  # Configure for MySQL
  if use_mysql:
    db_connection = connect_to_mysql(hostname, username,
                                     password, database_name)
  # Configure for sqlite
  else:
    db_connection = connect_to_sqlite(database_name)

  # Create a cursor object for executing statements.
  sql = db_connection.cursor()

  # For SQLite, foreign keys need to be enabled
  # manually.
  if not use_mysql:
    sql.execute("PRAGMA foreign_keys = ON;")

  return db_connection, sql

def get_users(sql):
  """Get a set of database users from the Users table. """

  query = """
  SELECT DISTINCT user FROM users
  """
  sql.execute(query)

  # The result of fetchall is a list of tuples, we need
  # just the first element of each tuple.
  return { user_tuple[0] for user_tuple in sql.fetchall() }

def get_user_id(username, sql):
  """Get UserID from the Users table based on our username.

  Inputs:
  -------
  username - The current username, returned from user_validation.get_username
  sql - Database cursor object used to execute statements.

  Returns:
  --------
  user_id - The integer UserID.
  """

  query = """
  SELECT user_id FROM users
      WHERE user = '{0}'
  """.format(username)
  sql.execute(query)

  # If you query one column for one value
  # that exists once, you get ((value,),).
  return sql.fetchall()[0][0]

def select_by_user_submission_id(usub_id, table, fields, sql):
  """A common operation in this project
  is the retrieval of data from tables indexed by
  UserSubmissionID.  This funtion can be used to
  do that.

  Inputs:
  -------
  sql - Database cursor object for execution of queries
  table - Name of the table to get fields from (str)
  fields - Fields to select from table (str)
  usub_id - The UserSubmissionID key

  Outputs:
  --------
  results - Tuple returned from the SELECT call

  """

  if isinstance(fields, list):
    query_fields = ', '.join(fields)
  elif isinstance(fields, str):
    query_fields = fields
  else:
    raise ValueError('fields must be a list of fields (strings) or a string')

  query = """
  SELECT {0} FROM {1}
      WHERE user_submission_id = {2};
  """.format(query_fields, table, usub_id)

  sql.execute(query)

  return sql.fetchall()

def get_gcards_for_submission(usub_id, sql):
  """ Return all gcards with their ID for a
  specified UserSubmissionID.

  Inputs:
  -------
  - usub_id - (int) UserSubmissions.UserSubmissionID
  - sql - cursor for accesing database

  Returns:
  --------
  - tuple((gcard_id1, gcard_text1), ...)
  """

  query = """
  SELECT GCardID, gcard_text FROM Gcards
  WHERE UserSubmissionID = {};
  """.format(usub_id)
  sql.execute(query)

  return sql.fetchall()

def get_username_for_submission(usub_id, sql):
  """ Return the user for this submission.

  Inputs:
  -------
  - usub_id - (int) UserSubmissions.UserSubmissionID
  - sql - cursor for accesing database

  Returns:
  --------
  - username (str)
  """
  query = """
  SELECT user FROM submissions
  WHERE user_submission_id = {0};""".format(usub_id)

  sql.execute(query)
  return sql.fetchall()[0][0]

def get_scard_text_for_submission(usub_id, sql):
  """ Get the scard text for this UserSubmissionID.

  Inputs:
  -------
  - usub_id - (int) UserSubmissions.UserSubmissionID
  - sql - cursor for accesing database

  Returns:
  --------
  - scard_text (str)
  """
  query  = """
  SELECT scard FROM submissions
  WHERE user_submission_id = {0};""".format(usub_id)
  sql.execute(query)
  return sql.fetchall()[0][0]

def get_unsubmitted_jobs(sql):
  """ Return a list of UserSubmissionID for 
  jobs that have not yet been submitted. 

  Inputs: 
  -------
  - sql - cursor object for querying database 


  Returns: 
  --------
  - ids - list of UserSubmissionID
  """
  query = """
    SELECT user_submission_id 
    FROM submissions
    WHERE run_status NOT LIKE '{0}'
      AND run_status NOT LIKE '{1}';
  """.format(
	  "Submitted to%",
	  "Submission scripts generated%"
  )
  sql.execute(query)

  return [entry[0] for entry in sql.fetchall()]

def get_old_jobs_from_queue(sql, hours=1):
  """ Get old jobs from the job_queue table. """
  query = """
  SELECT entry,update_time FROM job_queue
  """
  sql.execute(query)

  current_time = datetime.datetime.now()

  old_jobs = [] 
  for entry, timestamp in sql.fetchall():
    entry_time = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    expire_time = entry_time + datetime.timedelta(hours=hours)
    
    if expire_time < current_time:
      old_jobs.append(entry)

  return old_jobs
