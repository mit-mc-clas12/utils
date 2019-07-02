#****************************************************************
"""
# This file facilitates the construction of the database. In a perfect world, once everything is
#up and running, it will only be run once. However, it was clear from the beginning of the project
#that for testing purposes, the DB will have to be made many many times as the schema and goals change.
#This takes in the database structure as specified in file_struct and passes the structure
#as arguements to create_table and add_field functions defined in utils
"""
#****************************************************************

import utils, file_struct
import sqlite3, argparse

def create_database(args):
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
  argparser = argparse.ArgumentParser()
  argparser.add_argument(file_struct.debug_short,file_struct.debug_longdash,
                      default = file_struct.debug_default,help = file_struct.debug_help)
  argparser.add_argument('-l','--lite',help = "use -l or --lite to connect to sqlite DB, otherwise use MySQL DB", action = 'store_true')
  args = argparser.parse_args()

  file_struct.DEBUG = getattr(args,file_struct.debug_long)
  file_struct.use_mysql = not args.lite

  if args.lite:
    print("USING ARGS LITE")

  create_database(args)
