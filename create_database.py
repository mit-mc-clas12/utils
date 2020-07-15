"""

Create new database tables.

"""
import argparse
import os
import sqlite3
import sys

import database
import fs
import get_args

def add_field(db, sql, tablename, field_name, field_type):
    strn = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(
        tablename, field_name, field_type)
    print(strn)
    sql.execute(strn)
    db.commit()

def create_table(db, sql, tablename, PKname, FKargs):
    if isinstance(db, sqlite3.Connection):
        strn = ("CREATE TABLE IF NOT EXISTS {0}({1} "
                "integer primary key autoincrement {2});").format(
                    tablename, PKname, FKargs)
    else:
        strn = ("CREATE TABLE IF NOT EXISTS {0}({1} "
                "INT AUTO_INCREMENT, PRIMARY KEY ({1}) {2});").format(
                    tablename, PKname, FKargs)

    print(strn)
    sql.execute(strn)
    db.commit()

if __name__ == '__main__':

    args = get_args.get_args()


    if not args.lite:
        cred_file = os.path.dirname(os.path.abspath(__file__)) + \
                    '/../../msqlrw.txt'
        cred_file = os.path.normpath(cred_file)
        username, password = database.load_database_credentials(cred_file)
    else:
        username, password = "none", "none"

    #if args.lite is not None:
    #    database_name = args.lite
    #else:
    #    if args.test_database:
    #        database_name = "CLAS12TEST"
    #    else:
    #        database_name = "CLAS12OCRtest"

    database_name = "CLAS12TEST"
    
    use_mysql = False if args.lite else True
    db_conn, sql = database.get_database_connection(
        use_mysql=use_mysql,
        database_name=database_name,
        username=username,
        password=password,
        hostname='jsubmit.jlab.org'
    )

    # Create tables
    for table, primary_key, foreign_keys, fields in zip(
            fs.tables, fs.pks, fs.foreign_keys,
            fs.table_fields):
        create_table(db_conn, sql, table, primary_key, foreign_keys)

        for field, field_type in fields:
            add_field(db_conn, sql, table, field, field_type)

    db_conn.close()
