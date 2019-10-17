#****************************************************************
"""
# This file facilitates the construction of the database. In a perfect world, once everything is
# up and running, it will only be run once. However, it was clear from the beginning of the project
# that for testing purposes, the DB will have to be made many many times as the schema and goals change.
# This takes in the database structure as specified in fs and passes the structure
# as arguements to create_table and add_field functions defined in utils
"""
#****************************************************************
from __future__ import print_function
import os
import utils, fs, get_args
import sqlite3

def create_database(args):
  if args.lite:
    if not os.path.exists(fs.SQLite_DB_path):
      os.mkdir(fs.SQLite_DB_path)
    if os.path.exists(fs.SQLite_DB_path+"/"+fs.DB_name):
      print("{0} already exists in {1}, exiting".format(fs.DB_name,fs.SQLite_DB_path))
      exit()

  print("Creating {0} now".format(fs.DB_name))

  fs.DEBUG = getattr(args,fs.debug_long)
  #Create tables in the database
  for i in range(0,len(fs.tables)):
    utils.create_table(fs.tables[i],
                      fs.PKs[i],fs.foreign_key_relations[i],args)

  #Add fields to each table in the database
  for j in range(0,len(fs.tables)):
    for i in range(0,(len(fs.table_fields[j]))):
      utils.add_field(fs.tables[j],
                      fs.table_fields[j][i][0],fs.table_fields[j][i][1],args)

if __name__ == "__main__":
  args = get_args.get_args()
  create_database(args)
