#****************************************************************
"""
# This file facilitates the construction of the database. In a perfect world, once everything is
#up and running, it will only be run once. However, it was clear from the beginning of the project
#that for testing purposes, the DB will have to be made many many times as the schema and goals change.
#This takes in the database structure as specified in file_struct and passes the structure
#as arguements to create_table and add_field functions defined in utils
"""
#****************************************************************
from __future__ import print_function
import os
import utils, file_struct, get_args
import sqlite3

def create_database(args):
  filename = 'database'
  if os.path.isfile(filename):
    print(filename)
  else:
    os.mkdir(filename)

  file_struct.DEBUG = getattr(args,file_struct.debug_long)
  #Create tables in the database
  for i in range(0,len(file_struct.tables)):
    utils.create_table(file_struct.tables[i],
                      file_struct.PKs[i],file_struct.foreign_key_relations[i],args)

  #Add fields to each table in the database
  for j in range(0,len(file_struct.tables)):
    for i in range(0,(len(file_struct.table_fields[j]))):
      utils.add_field(file_struct.tables[j],
                      file_struct.table_fields[j][i][0],file_struct.table_fields[j][i][1],args)

if __name__ == "__main__":
  args = get_args.get_args()
  create_database(args)
