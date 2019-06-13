#****************************************************************
"""
# This is the second most important file behind file_struct to understanding
# the flow of this software. Commonly used functions are defined here and
# reference in most parts of the code. The functions are:
# printer and printer2 - prints strings depending on value of DEBUG variable
# overwrite_file - overwrites a template file to a newfile based off old and new value lists
# (this will be replaced in the future with functions to generate scripts directly)
# grab_DB_data - creates lists by grabbing values from the DB based on a dictionary
# add_field  and create_table - functions to create the SQLite DB, used by create_database.py
# sql3_exec and sql3_grab - functions to write and read information to/from the DB
"""
#****************************************************************

from __future__ import print_function
import file_struct, sqlite3, os, datetime
import MySQLdb

def gettime():
  return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def printer(strn): # Can't call the function print because it already exists in python
  if (int(file_struct.DEBUG) == 1) or (int(file_struct.DEBUG) == 2):
    print(strn)

def printer2(strn): # Can't call the function print because it already exists in python
  if (int(file_struct.DEBUG) == 2):
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
def grab_DB_data(table,dictionary,BatchID): #DB_name, table = str, dictionary = dict
    oldvals, newvals = [],[]
    for key in dictionary:
      strn = "SELECT {0} FROM {1} Where BatchID = {2};".format(dictionary[key],table,BatchID)
      value = sql3_grab(strn)[0][0]#Grabs value from list of tuples
      oldvals.append(key)
      newvals.append(value)
    return oldvals, newvals

#Add a field to an existing DB. Need to add error statements if DB or table does not exist
def add_field(tablename,field_name,field_type):
  strn = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(tablename,field_name, field_type)
  sql3_exec(strn)
  printer('In database {0}, table {1} has succesfully added field {2}'.format(file_struct.DB_name,tablename,field_name))

#Create a table in a database
def create_table(tablename,PKname,FKargs):
  strn = "CREATE TABLE IF NOT EXISTS {0}({1} integer primary key autoincrement {2})".format(tablename,PKname,FKargs)
  sql3_exec(strn)
  printer('In database {0}, table {1} has succesfully been created with primary key {2}'.format(file_struct.DB_name,
        tablename,PKname))

#Executes writing commands to DB. To return data from DB, use sql3_grab(), defined below
def sql3_exec(strn):
  if file_struct.use_mysql:
    DB = file_struct.MySQL_DB_path+file_struct.DB_name
    conn = MySQLdb.connect('jsubmit.jlab.org', user=file_struct.mysql_uname, password=file_struct.mysql_psswrd,database="CLAS12OCR")
    c = conn.cursor()
  else:
    DB = file_struct.SQLite_DB_path+file_struct.DB_name
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

#Executes reading commands to DB. Cannot currently be used to return data from DB
def sql3_grab(strn):
  if file_struct.use_mysql:
    DB = file_struct.MySQL_DB_path+file_struct.DB_name
    conn = MySQLdb.connect('jsubmit.jlab.org', user=file_struct.mysql_uname, password=file_struct.mysql_psswrd,database="CLAS12OCR")
  else:
    DB = file_struct.SQLite_DB_path+file_struct.DB_name
    conn = sqlite3.connect(DB)
  c = conn.cursor()
  printer2('Executing SQL Command: {0}'.format(strn)) #Turn this on for explict printing of all DB write commands
  c.execute(strn)
  return_array = c.fetchall()
  c.close()
  conn.close()
  return return_array
