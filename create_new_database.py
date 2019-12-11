""" 

Create new database tables.

"""
import argparse 
import os 
import sys 

import database 
import fs 

def add_field(db, sql, tablename, field_name, field_type):
    strn = "ALTER TABLE {0} ADD COLUMN {1} {2}".format(
        tablename, field_name, field_type)
    print(strn)
    sql.execute(strn)
    db.commit()

def create_table(db, sql, tablename, PKname, FKargs):
    strn = ("CREATE TABLE IF NOT EXISTS {0}({1} "
            "INT AUTO_INCREMENT, PRIMARY KEY ({1}) {2});").format(
                tablename, PKname, FKargs)
    print(strn)
    sql.execute(strn)
    db.commit()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--lite', default=None, type=str)
    parser.add_argument('--test_database', action='store_true', default=False)
    args = parser.parse_args()
    
    cred_file = os.path.dirname(os.path.abspath(__file__)) + \
                '/../msqlrw.txt'
    cred_file = os.path.normpath(cred_file)
    username, password = database.load_database_credentials(cred_file)

    if args.lite is not None:
        database_name = args.lite
    else:
        if args.test_database:
            database_name = "CLAS12TEST"
        else:
            database_name = "CLAS12OCR"

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
            fs.new_tables, fs.new_pks, fs.new_foreign_keys,
            fs.new_table_fields):
        create_table(db_conn, sql, table, primary_key, foreign_keys)

        #for i, table in enumerate(fs.new_tables):
        for field, field_type in fields:
            add_field(db_conn, sql, table, field, field_type)

    db_conn.close()
