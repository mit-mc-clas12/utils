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

#There might be a more succient way to create these objects, but for now this works
runscript_file_obj = sub_file('runscript.sh')
runscript_file_obj.file_base = 'runscript'
runscript_file_obj.file_end = '.sh'
runscript_file_obj.file_text_fieldname = 'runscript_text'

condor_file_obj = sub_file('clas12.condor')
condor_file_obj.file_base = 'clas12'
condor_file_obj.file_end = '.condor'
condor_file_obj.file_text_fieldname = 'clas12_condor_text'

run_job_obj = sub_file('run_job')
run_job_obj.file_base = 'run_job'
run_job_obj.file_end = '.sh'
run_job_obj.file_text_fieldname = 'run_job_text'

cw_obj = sub_file('condor_wrapper')
cw_obj.file_base = 'condor_wrapper'
cw_obj.file_end = ''
cw_obj.file_text_fieldname = 'condor_wrapper_text'

"""*****************************************************************************
-------------------------  DB Schema Specification -----------------------------
*****************************************************************************"""

new_tables = ['users', 'submissions']
new_pks = ['user_id', 'user_submission_id']
new_user_fields = (('user','TEXT'), ('domain_name','TEXT'), ('join_date','TEXT'),
                   ('total_submissions','INT'), ('total_jobs','INT'),
                   ('total_events','INT'), ('most_recent_active_date','TEXT'))
new_submissions_fields = (
  ('user','TEXT'), ('timestamp','TEXT'), ('scard','TEXT'),
  ('client_ip','TEXT'), ('submission_pool','TEXT'), ('submission_timestamp','TEXT'),
  ('pool_node','TEXT'), ('run_status','TEXT'), ('completion_timestamp','TEXT'),
  (runscript_file_obj.file_text_fieldname,'TEXT'),
  (condor_file_obj.file_text_fieldname,'TEXT'),
  (run_job_obj.file_text_fieldname,'TEXT'),
  (cw_obj.file_text_fieldname,'TEXT'),
  ('job_submission_date','TEXT'),
  ('job_completion_date','TEXT'),
  ('output_file_directory','TEXT'),
  ('output_file_size', 'INT'),
  ('number_job_failures', 'INT')
)
new_user_foreign_keys = ""
new_submission_foreign_keys = """, user_id INT, FOREIGN KEY(user_id) REFERENCES users(user_id)"""
new_foreign_keys = [new_user_foreign_keys, new_submission_foreign_keys]
new_table_fields = [new_user_fields, new_submissions_fields]

tables = ['Users','UserSubmissions','Scards','Gcards','FarmSubmissions','JobsLog']

#Primary Key definitions:
PKs = ['UserID','UserSubmissionID','ScardID','GcardID','FarmSubmissionID','JobID']

users_fields = (('domain_name','TEXT'),('JoinDateStamp','TEXT'),('Total_UserSubmissions','INT'),
                ('Total_Jobs','INT'),('Total_Events','INT'),('Most_Recent_Active_Date','TEXT'))


UserSubmissions_fields = (('User','TEXT'),('timestamp','TEXT'),('scard','TEXT'),('client_ip','TEXT'))

# Since there is only 1 scard / UserSubmission, in princple this entire scard table should be deleted
# The submission scripts can be completely written using just the text in the VARCHAR 'scard' field in the UserSubmissions table
# Importantly, this is not yet implemented. It should be straightforward to do so, but time consuming
scards_fields = (('group_name','TEXT'),('farm_name','TEXT'),('Nevents','INT'),
                ('Generator','TEXT'),('genExecutable','TEXT'),('genOutput','TEXT'),
                ('GenOptions','TEXT'),('Gcards','TEXT'),('Jobs','INT'),
                ('Project','TEXT'),('Luminosity','INT'),('Tcurrent','INT'),('Pcurrent','INT'),
                 ('Cores_Req','INT'),('Mem_Req','INT'),('timestamp','TEXT'), 
                 ('generatorOUT','TEXT'), ('reconstructionOUT','TEXT'), ('gemcEvioOUT','TEXT'), 
                 ('gemcHipoOUT','TEXT'), ('dstOUT', 'TEXT'))

gcards_fields = (('gcard_text','TEXT'),)

FarmSubmissions_fields = (('submission_pool','TEXT'),('submission_timestamp','TEXT'),
                      ('pool_node','TEXT'),
                      ('run_status','TEXT'),('completion_timestamp','TEXT'),
                      (runscript_file_obj.file_text_fieldname,'TEXT'),
                      (condor_file_obj.file_text_fieldname,'TEXT'),
                      (run_job_obj.file_text_fieldname,'TEXT'),
                      (cw_obj.file_text_fieldname,'TEXT'))

joblogs_fields = (('Job_Submission_Datestamp','TEXT'),
                  ('Job_Completion_Datestamp','TEXT'),('Output_file_directory','TEXT'),
                  ('Output_file_size','INT'),('Number_Job_failures','INT'))

table_fields = [users_fields,UserSubmissions_fields, scards_fields, gcards_fields, FarmSubmissions_fields, joblogs_fields]

#Below defines foreign key relations. There is a more succinet way to do this but as we have
#only a few relations, I did not spend the time to modifiy this code.
users_special_relations = """, User TEXT NOT NULL"""
UserSubmissions_foreign_keys = """, UserID INT,
                      FOREIGN KEY(UserID) REFERENCES Users(UserID)"""
scards_foreign_keys = """, UserSubmissionID INTEGER,
                      FOREIGN KEY(UserSubmissionID) REFERENCES UserSubmissions(UserSubmissionID)"""
gcards_foreign_keys = """, UserSubmissionID INTEGER,
                      FOREIGN KEY(UserSubmissionID) REFERENCES UserSubmissions(UserSubmissionID)"""
FarmSubmissions_foreign_keys = """, UserSubmissionID INTEGER, GcardID INTEGER,
                      FOREIGN KEY(UserSubmissionID) REFERENCES UserSubmissions(UserSubmissionID),
                      FOREIGN KEY(GcardID) REFERENCES Gcards(GcardID)"""
joblogs_foreign_keys = """, UserID INTEGER, UserSubmissionID INTEGER, FarmSubmissionID INTEGER,
                      FOREIGN KEY(UserID) REFERENCES Users(UserID),
                      FOREIGN KEY(UserSubmissionID) REFERENCES UserSubmissions(UserSubmissionID),
                      FOREIGN KEY(FarmSubmissionID) REFERENCES FarmSubmissions(FarmSubmissionID)"""
#create table yourtablename (_id  integer primary key autoincrement, column1 text not null unique, column2 text);

foreign_key_relations = [users_special_relations, UserSubmissions_foreign_keys,
                        scards_foreign_keys, gcards_foreign_keys,
                        FarmSubmissions_foreign_keys, joblogs_foreign_keys]
"""*****************************************************************************
-------------------- Scard and Runscripts Specifications -----------------------
*****************************************************************************"""
#This defines the ordering and items that need to be in scard.txt

scard_key = ('scardID', 'userSubmissionID', 'project',   'group',    'farm_name', 'generator',
            'genOptions', 'nevents',  'gcards',    'luminosity',
				'tcurrent',   'pcurrent', 'cores_req',' mem_req','jobs')

#This defines the variables that will be written out to submission scripts and maps to DB values
condor_file_obj.overwrite_vals = {'project_scard':'project','jobs_scard':'jobs',
                          'cores_req_scard':'cores_req','mem_req_scard':'mem_req','nevents_scard': 'nevents'}

#This does not go through the database, but instead just replaces runscript.overwrite with the file location
#Note that the value here is unimportant, as the overwrite value that is used is generated in sub_script_generator.py
run_job_obj.overwrite_vals  = {'runscript.overwrite': 'rs_overwrite_unused'}

#This is unused currently as the condor_wrapper does not need any unique filenames
cw_obj.overwrite_vals = {}

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

# Specifiy Database name:
DB_name = 'CLAS12_OCRDB.db'

# Specify scard name
scard_name = 'scard.txt'

# Specify the directory names of all submission files
gcards_dir = 'gcards/'
condor_file_obj.file_path    = sub_files_path+'condor_files/'
runscript_file_obj.file_path = sub_files_path+'runscript_files/'
run_job_obj.file_path        = sub_files_path+'run_job_files/'
cw_obj.file_path             = sub_files_path+'condor_wrapper_files/' # This is not currently used / needed, but included for completeness

"""*****************************************************************************
---------------------------- Other Specifications ------------------------------
*****************************************************************************"""
# Definition of valid scard types. Explainations for these types can be found in the documentation.
valid_scard_types = [1, 2, 3, 4]

# This defines a mapping between 'generator' in scard, the genOutput and genExecutable
genOutput     =  {'clasdis': 'sidis.dat', 'dvcs': 'dvcsgen1.dat', 'disrad':'dis-rad.dat' , 'genKYandOnePion': 'genKYandOnePion.dat', 'gemc': 'gemc'}
genExecutable =  {'clasdis': 'clasdis'  , 'dvcs': 'dvcsgen'     , 'disrad':'generate-dis', 'genKYandOnePion': 'eg_ky'              , 'gemc': 'gemc'}

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
container_gcards = gcard_helper.get_valid_gcards(
  os.path.dirname(os.path.abspath(__file__)) + '/valid_gcards.txt'
)
lund_identifying_text = '.txt' #For use in gcard_helper.py
lund_default = ""
