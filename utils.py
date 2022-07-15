"""This is the second most important file behind fs to understanding
    the flow of this software. Commonly used functions are defined here and
    reference in most parts of the code. The functions are:
    printer and printer2 - prints strings depending on value of DEBUG variable
    overwrite_file - overwrites a template file to a newfile based off old
    and new value lists (this will be replaced in the future with functions to
    generate scripts directly) grab_DB_data - creates lists by grabbing values
    from the DB based on a dictionary add_field  and create_table - functions
    to create the SQLite DB, used by create_database.py db_write and
    db_grab - functions to write and read information to/from the DB
"""


import datetime
import logging
import sys
import calendar
from . import fs
#import MySQLdb
import sqlite3

def getPythonVersion():
    return sys.version_info[0] #element 0 is the major release, e.g. python 2 or python 3




#For some very, very annoying reason, pytz is not a supported module on ifarm for python3
#Therefore, if we are using python3, we will just do a hard-coded time conversion, which is not optimal
pyversion = getPythonVersion()
if pyversion == 2:
    import pytz

    def unixtimeconvert(time,timezone):
      utc = datetime.datetime.utcfromtimestamp(time)
      if timezone == 'eastern':
          local_tz = pytz.timezone('America/New_York')
      else:
          print("please specifiy a supported timezone")

      ## You could use `tzlocal` module to get local timezone on Unix and Win32
      # from tzlocal import get_localzone # $ pip install tzlocal
      # # get local timezone
      # local_tz = get_localzone()
      #Y You might not want to do this though if servers are running in different timezones

      local_dt = utc.replace(tzinfo=pytz.utc).astimezone(local_tz).strftime('%m/%d %H:%M')

      return local_dt

elif pyversion == 3:

      def unixtimeconvert(time,timezone):
        
        if timezone == 'eastern':
            local_tz_shift = 4*3600 #Easter timezone is 4 hours off UTC. This might get messed up around daylight saving times
        else:
            print("please specifiy a supported timezone")

        utc = datetime.datetime.utcfromtimestamp(time-local_tz_shift)
        ## You could use `tzlocal` module to get local timezone on Unix and Win32
        # from tzlocal import get_localzone # $ pip install tzlocal
        # # get local timezone
        # local_tz = get_localzone()
        #Y You might not want to do this though if servers are running in different timezones

        local_dt = utc.strftime('%m/%d %H:%M')

        return local_dt
else:
    print("This code only works with python version 2 or 3")
    print("Python version is listed as {0}, please change".format(pyversion))
    exit()


def gettime():
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def printer(strn): # Can't call the function print because it already exists in python
  if (int(fs.DEBUG) == 1) or (int(fs.DEBUG) == 2):
    print(strn)

def printer2(strn): # Can't call the function print because it already exists in python
  if (int(fs.DEBUG) == 2):
    print(strn)

""" The below function is probably no longer needed"""
#Takes in a .template file, a list of values to replace (old_vals) and a list of what to replace them with (new_vals)
#def overwrite_file(template_file,newfile,old_vals,new_vals): #template_file = str, old_vals, new_vals = LIST
#    with open(template_file,"r") as tmp: str_script = tmp.read()
#    for i in range(0,len(old_vals)):
#      str_script = str_script.replace(old_vals[i],str(new_vals[i]))
#    with open(newfile,"w") as file: file.write(str_script)
#    return str_script

#Takes a dictionary, retuns 2 lists: key (oldvals) and value (newvals) from table in DB_name
def grab_DB_data(table,dictionary,UserSubmissionID): #DB_name, table = str, dictionary = dict
    oldvals, newvals = [],[]
    for key in dictionary:
      strn = "SELECT {0} FROM {1} Where UserSubmissionID = {2};".format(dictionary[key],table,UserSubmissionID)
      value = db_grab(strn)[0][0]#Grabs value from list of tuples
      oldvals.append(key)
      newvals.append(value)
    return oldvals, newvals

# Add a field to an existing DB. Need to add error statements if DB
# or table does not exist
def add_field(tablename,field_name,field_type,args):
  strn = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(tablename,field_name, field_type)
  db_write(strn)
  printer('In database {0}, table {1} has succesfully added field {2}'.format(fs.DB_name,tablename,field_name))

#Create a table in a database
def create_table(tablename,PKname,FKargs,args):
  if args.lite:
    strn = "CREATE TABLE IF NOT EXISTS {0}({1} integer primary key autoincrement {2})".format(tablename,PKname,FKargs)
  if not args.lite:
    strn = "CREATE TABLE IF NOT EXISTS {0}({1} INT AUTO_INCREMENT, PRIMARY KEY ({1}) {2});".format(tablename,PKname,FKargs)
  db_write(strn)
  printer('In database {0}, table {1} has succesfully been created with primary key {2}'.format(fs.DB_name,
        tablename,PKname))

# Executes writing commands to DB. To return data from DB, use db_grab(),
# defined below
def db_write(strn):
  if fs.use_mysql:
    DB = fs.MySQL_DB_path+fs.DB_name
    #mysqldb.connect doesn't work with optional arguments from frontend. It used be
    #conn = MySQLdb.connect(fs.MySQL_DB_path, user=fs.mysql_uname,
    #                        password=fs.mysql_psswrd,database="CLAS12OCR")
    conn = MySQLdb.connect(fs.MySQL_DB_path, fs.mysql_uname, fs.mysql_psswrd, "CLAS12TEST")
    c = conn.cursor()
  else:
    DB = fs.SQLite_DB_path
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys = ON;')
  printer2("Connecting to Database at {0}".format(DB))
  printer2('Executing SQL Command: {0}'.format(strn)) #Turn this on for explict printing of all DB write commands
  c.execute(strn)
  insertion_id = c.lastrowid
  conn.commit()
  c.close()
  conn.close()
  return insertion_id

# Executes reading commands to DB. Cannot currently be used to return
# data from DB.
def db_grab(strn):

  if fs.use_mysql:
    DB = fs.MySQL_DB_path+fs.DB_name
    #mysqldb.connect doesn't work with optional arguments from frontend. It used be
    #conn = MySQLdb.connect(fs.MySQL_DB_path, user=fs.mysql_uname,
    #                        password=fs.mysql_psswrd,database="CLAS12OCR")
    conn = MySQLdb.connect(fs.MySQL_DB_path, fs.mysql_uname, fs.mysql_psswrd, "CLAS12OCR")

  else:
    DB = fs.SQLite_DB_path
    print('Connecting to SQLite database@{}'.format(DB))
    conn = sqlite3.connect(DB)

  c = conn.cursor()
  printer2('Executing SQL Command: {0}'.format(strn)) #Turn this on for explict printing of all DB write commands
  c.execute(strn)
  return_array = c.fetchall()
  c.close()
  conn.close()
  return return_array


def configure_logger(args):
    """ Logging, very basic for now. """
    logger = logging.getLogger('SubMit')
    level = logging.DEBUG if (args.debug > 0) else logging.INFO
    logger.setLevel(level)

    # Can be changed to output file
    console_log = logging.StreamHandler()
    console_log.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s:%(levelname)s] %(message)s')
    console_log.setFormatter(formatter)

    logger.addHandler(console_log)
    return logger