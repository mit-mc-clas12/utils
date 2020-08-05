#****************************************************************
"""
# File Structure (fs)
# This file is the central location for this software information. It includes:
# - Submission file specifications, including:
#        - submission file class definition
#        - submission file objects for all submission files needed for Tier 2 submission
# - database schema, including:
#        - database name
#        - tables & table fields
#        - primary and foreign keys
# - scard and running scripts specifications, including:
#        - all fields that are necessary and sufficient to define a valid scard
#        - all values that will be overwritten in creating run scripts
# - relative directory mapping, including:
#        - layout of expected directory structure
#        - relative path variable names
# - other specifications, including:
#      - mapping between scard generator keyword and genOutput & genExecutable
"""
#****************************************************************

from __future__ import print_function
import sqlite3, os, datetime

import gcard_helper

"""*****************************************************************************
------------------------ Submission File Specifications ------------------------
*****************************************************************************"""
# Create a class for all submission files. There are other ways to store this information
# But a class seemed like a reasonable way to go, so if we want to add more
# submission files we can just create a new submission file object.
# We don't need to declare any fields in the class constructor but it helps code readability

class sub_file():
  def __init__(self,name):
    self.name = name
    self.file_path = -1
    self.file_base = -1
    self.file_end = -1
    self.overwrite_vals = -1
    self.file_text_fieldname = -1

# There might be a more succient way to create these objects, but for now this works
runscript_file_obj = sub_file('runscript.sh')
runscript_file_obj.file_base = 'runscript'
runscript_file_obj.file_end = '.sh'
runscript_file_obj.file_text_fieldname = 'runscript_text'

condor_file_obj = sub_file('clas12.condor')
condor_file_obj.file_base = 'clas12'
condor_file_obj.file_end = '.condor'
condor_file_obj.file_text_fieldname = 'clas12_condor_text'

#run_job_obj = sub_file('run_job')
#run_job_obj.file_base = 'run_job'
#run_job_obj.file_end = '.sh'
#run_job_obj.file_text_fieldname = 'run_job_text'
#
#cw_obj = sub_file('condor_wrapper')
#cw_obj.file_base = 'condor_wrapper'
#cw_obj.file_end = ''
#cw_obj.file_text_fieldname = 'condor_wrapper_text'

"""*****************************************************************************
-------------------------  DB Schema Specification -----------------------------
*****************************************************************************"""
MySQL_Prod_DB_Name = "CLAS12OCR"
MySQL_Test_DB_Name = "CLAS12TEST"
SQLite_Test_DB_Name = "CLAS12OCR.db"

db_hostname = 'jsubmit.jlab.org'
prod_db_cred_file = '/../msqlrw.txt'
test_db_cred_file = '/../msqlrw.txt'


tables = ['users', 'submissions', 'job_queue']
pks = ['user_id', 'user_submission_id', 'entry']
user_fields = (('user','TEXT'), ('domain_name','TEXT'), ('join_date','TEXT'),
               ('priority','INT'), ('total_running_jobs','INT'),
               ('priority_weight','FLOAT'), ('condor_rank','INT'))
submissions_fields = (
  ('user','TEXT'), ('client_time','TEXT'), ('scard','TEXT'),
  ('client_ip','TEXT'), ('server_time','TEXT'),
  ('pool_node','TEXT'), ('run_status','TEXT'),
  (runscript_file_obj.file_text_fieldname,'TEXT'),
  (condor_file_obj.file_text_fieldname,'TEXT')
)
job_queue_fields = (('total','INT'), ('update_time','TEXT'),
                        ('run', 'INT'), ('hold', 'INT'), ('idle', 'INT'),
                        ('done', 'INT'), ('osg_id', 'INT'), ('submitted', 'INT'))

user_foreign_keys = ""
submission_foreign_keys = """, user_id INT, FOREIGN KEY(user_id) REFERENCES users(user_id)"""
job_queue_keys = """, user_id INT, FOREIGN KEY(user_id) REFERENCES users(user_id)"""
foreign_keys = [user_foreign_keys, submission_foreign_keys, job_queue_keys]
table_fields = [user_fields, submissions_fields, job_queue_fields]

"""*****************************************************************************
-------------------- Scard and Runscripts Specifications -----------------------
*****************************************************************************"""
#This defines the ordering and items that need to be in scard.txt

scard_key = ('scardID', 'userSubmissionID', 'project',   'farm_name', 'generator',
            'genOptions', 'nevents',  'configuration',    'luminosity',
				'tcurrent',   'pcurrent', 'cores_req',' mem_req','jobs', 'fields', 'bkmerging','client_ip',)

#This defines the variables that will be written out to submission scripts and maps to DB values
condor_file_obj.overwrite_vals = {'project_scard':'project','jobs_scard':'jobs',
                          'cores_req_scard':'cores_req','mem_req_scard':'mem_req','nevents_scard': 'nevents'}

#This does not go through the database, but instead just replaces runscript.overwrite with the file location
#Note that the value here is unimportant, as the overwrite value that is used is generated in sub_script_generator.py
# obsolete?
#run_job_obj.overwrite_vals  = {'runscript.overwrite': 'rs_overwrite_unused'}

#This is unused currently as the condor_wrapper does not need any unique filenames
# cw_obj.overwrite_vals = {}

"""*****************************************************************************
------------------------- File Path Specifications -----------------------------
*****************************************************************************"""

dirname = os.path.dirname(os.path.abspath(__file__))#os.path.dirname(__file__)

#Specify the location of where all submission files live (runscripts, gcards,etc)
sub_files_path = dirname+'/../server/submission_files/generated_files/'
#Specify the location of the DB relative to here (This will get changed when moving to SQL RDBMS)

# To Do: the sql lite database should be used only in "test" mode
# This variable can bet set with a command line argument, for example: -testDB=../CLAS12_OCRDB.db
# The argument should be handled by both the client and server

use_mysql = True
mysql_uname  = "Null_User"
mysql_psswrd =  "Null_Password"
MySQL_DB_path  = "jsubmit.jlab.org"
SQLite_DB_path = dirname + '/../tests/test.sqlite'

# Specify the location of the scard
scard_path = dirname+"/../client/"


# Specify scard name
scard_name = 'scard.txt'

# Specify the directory names of all submission files
gcards_dir = 'gcards/'
condor_file_obj.file_path    = sub_files_path+'condor_files/'
runscript_file_obj.file_path = sub_files_path+'runscript_files/'
#run_job_obj.file_path        = sub_files_path+'run_job_files/'
# cw_obj.file_path             = sub_files_path+'condor_wrapper_files/' # This is not currently used / needed, but included for completeness

"""*****************************************************************************
---------------------------- Other Specifications ------------------------------
*****************************************************************************"""
# Definition of valid scard types. Explainations for these types can be found in the documentation.
valid_scard_types = [1, 2, 3, 4]

#Below is for gemc json logging
default_osg_json_log = "osgLog.json"
user_data_keys = ["user",  "job id","submitted", "total", "done", "run", "idle", "hold","osg id"]
null_user_info = ["No user", "No ID", "No data", "No data","No data" ,"No data","No data","No data","No ID"]


# This defines a mapping between 'generator' in scard, the genOutput and genExecutable
#genOutput     =  {'clasdis': 'sidis.dat', 'dvcs': 'dvcsgen1.dat', 'disrad':'dis-rad.dat' , 'genKYandOnePion': 'genKYandOnePion.dat', 'gemc': 'gemc'}
#genExecutable =  {'clasdis': 'clasdis'  , 'dvcs': 'dvcsgen'     , 'disrad':'generate-dis', 'genKYandOnePion': 'eg_ky'              , 'gemc': 'gemc'}
genOutput     =  {'clasdis': 'clasdis.dat', 'claspyth': 'claspyth.dat', 'dvcsgen': 'dvcsgen.dat', 'genKYandOnePion': 'genKYandOnePion.dat', 'inclusive-dis-rad':'inclusive-dis-rad.dat' , 'jpsigen': 'jpsigen.dat', 'tcsgen': 'tcsgen.dat', 'gemc': 'gemc'}
genExecutable =  {'clasdis': 'clasdis'  ,   'claspyth': 'claspyth',     'dvcsgen': 'dvcsgen'    , 'genKYandOnePion': 'genKYandOnePion'    , 'inclusive-dis-rad':'inclusive-dis-rad',      'jpsigen': 'jpsigen',     'tcsgen': 'tcsgen',     'gemc': 'gemc'}

# This is the debug variable for print statments - 0 = no messages, 1 = some, 2 = all messages. Initalized to 1
DEBUG = 0
debug_short = '-d'
debug_long = 'debug'
debug_longdash ='--'+debug_long
debug_default = DEBUG
debug_help = help = """0 (default) - no messages,1 - general messages,
                    2 - all messages, all reads and writes into and out of the database"""

gcard_identifying_text = '.gcard' # For use in gcard_helper.py
gcard_default = '/jlab/clas12Tags/gcards/clas12-default.gcard'

lund_identifying_text = '.txt' #For use in gcard_helper.py
lund_default = ""
