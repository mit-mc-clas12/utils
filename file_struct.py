#****************************************************************
"""
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

"""*****************************************************************************
------------------------ Submission File Specifications ------------------------
*****************************************************************************"""
#Create a class for all submission files. There are other ways to store this information
#But a class seemed like a reasonable way to go, so if we want to add more
#submission files we can just create a new submission file object.
#We don't need to decalre any fields in the class constructor but it helps code readability
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
tables = ['Users','Batches','Scards','Gcards','Submissions','JobsLog']

#Primary Key definitions:
PKs = ['UserID','BatchID','ScardID','GcardID','SubmissionID','JobID']

users_fields = (('domain_name','TEXT'),('JoinDateStamp','INT'),('Total_Batches','INT'),
                ('Total_Jobs','INT'),('Total_Events','INT'),('Most_Recent_Active_Date','INT'))


batches_fields = (('timestamp','FLOAT'),('scard','VARCHAR'))

#Since there is only 1 scard / batch, in princple this entire scard table should be deleted
#The submission scripts can be completely written using just the text in the VARCHAR 'scard' field in the Batches table
#Importantly, this is not yet implemented. It should be straightforward to do so, but time consuming
scards_fields = (('group_name','TEXT'),('farm_name','TEXT'),('Nevents','INT'),
                ('Generator','TEXT'),('genExecutable','TEXT'),('genOutput','TEXT'),
                ('GenOptions','TEXT'),('Gcards','TEXT'),('Jobs','INT'),
                ('Project','TEXT'),('Luminosity','INT'),('Tcurrent','INT'),('Pcurrent','INT'),
                ('Cores_Req','INT'),('Mem_Req','INT'),('timestamp','FLOAT'))


gcards_fields = (('gcard_text','VARCHAR'),)

submissions_fields = (('submission_pool','TEXT'),('submission_timestamp','INT'),
                      ('pool_node','TEXT'),
                      ('run_status','TEXT'),('completion_timestamp','INT'),
                      (runscript_file_obj.file_text_fieldname,'VARCHAR'),
                      (condor_file_obj.file_text_fieldname,'VARCHAR'),
                      (run_job_obj.file_text_fieldname,'VARCHAR'),
                      (cw_obj.file_text_fieldname,'VARCHAR'))

joblogs_fields = (('Job_Submission_Datestamp','INT'),
                  ('Job_Completion_Datestamp','TEXT'),('Output_file_directory','TEXT'),
                  ('Output_file_size','INT'),('Number_Job_failures','INT'))

table_fields = [users_fields,batches_fields, scards_fields, gcards_fields, submissions_fields, joblogs_fields]

#Below defines foreign key relations. There is a more succinet way to do this but as we have
#only a few relations, I did not spend the time to modifiy this code.
users_special_relations = """, User TEXT NOT NULL UNIQUE""" #Makes User field be UNIQUE, so we can use as FK
batches_foreign_keys = """, User TEXT,
                      FOREIGN KEY(User) REFERENCES Users(User)"""
scards_foreign_keys = """, BatchID INTEGER,
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)"""
gcards_foreign_keys = """, BatchID INTEGER,
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)"""
submissions_foreign_keys = """, BatchID INTEGER, GcardID INTEGER,
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)
                      FOREIGN KEY(GcardID) REFERENCES Gcards(GcardID)"""
joblogs_foreign_keys = """, UserID INTEGER, BatchID INTEGER, SubmissionID INTEGER,
                      FOREIGN KEY(UserID) REFERENCES Users(UserID)
                      FOREIGN KEY(BatchID) REFERENCES Batches(BatchID)
                      FOREIGN KEY(SubmissionID) REFERENCES Submissions(SubmissionID)"""
#create table yourtablename (_id  integer primary key autoincrement, column1 text not null unique, column2 text);

foreign_key_relations = [users_special_relations, batches_foreign_keys,
                        scards_foreign_keys, gcards_foreign_keys,
                        submissions_foreign_keys, joblogs_foreign_keys]
"""*****************************************************************************
-------------------- Scard and Runscripts Specifications -----------------------
*****************************************************************************"""
#This defines the ordering and items that need to be in scard.txt
scards_fields = (('group_name','TEXT'),('farm_name','TEXT'),('Nevents','INT'),
                ('Generator','TEXT'),('genExecutable','TEXT'),('genOutput','TEXT'),
                ('GenOptions','TEXT'),('Gcards','TEXT'),('Jobs','INT'),
                ('Project','TEXT'),('Luminosity','INT'),('Tcurrent','INT'),('Pcurrent','INT'),
                ('Cores_Req','INT'),('Mem_Req','INT'),('timestamp','FLOAT'))

scard_key = ('group','farm_name','nevents','generator',
            'genOptions',  'gcards', 'jobs',  'project',
            'luminosity', 'tcurrent',  'pcurrent','cores_req','mem_req')

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
"""Current path specifications are as follows: (only important files & dirs included)
clas12simulation(s)
  scard.txt
  database
    CLAS12_OCRDB.db
  submission_files
    condor_files
    condor_wrapper_files
    gcards
    run_job_files
    runscript_files
  src
     db_batch_entry.py
     db_user_entry.py
     sub_script_generator.py
     templates
        *.template
     utils
        create_database.py
        file_struct.py **** this file, all locations are referenced relative to this
        gcard_helper.py
        scard_helper.py
        utils.py
"""
import os #I would like to do this part differently, but dont have the time to do this right now.
#I would like to remove dirname entirely, and have everything run relatively, but right now this works.
dirname = os.path.dirname(os.path.abspath(__file__))#os.path.dirname(__file__)

#Specify the location of where all submission files live (runscripts, gcards,etc)
sub_files_path = dirname+'/../server/submission_files/generated_files/'
#Specify the location of the DB relative to here (This will get changed when moving to SQL RDBMS)
DB_path = dirname+"/../database/"
#Specify the location of the scard
scard_path = dirname+"/../client/"

#Specifiy Database name:
DBname = 'CLAS12_OCRDB.db'
#Specify scard name
scard_name = 'scard.txt'
#Specify the directory names of all submission files
gcards_dir = 'gcards/'
condor_file_obj.file_path = sub_files_path+'condor_files/'
runscript_file_obj.file_path = sub_files_path+'runscript_files/'
run_job_obj.file_path = sub_files_path+'run_job_files/'
cw_obj.file_path = sub_files_path+'condor_wrapper_files/' #This is not currently used / needed, but included for completeness

"""*****************************************************************************
---------------------------- Other Specifications ------------------------------
*****************************************************************************"""

# This defines a mapping between 'generator' in scard and the genOutput and genExecutable literals to be invoked
# the key 'dvcs' should be changed to dvcsgen
genOutput= {'clasdis': 'sidis.dat', 'dvcs': 'dvcs.dat','disrad':'dis-rad.dat'}
genExecutable =  {'clasdis': 'clasdis', 'dvcs': 'dvcsgen','disrad':'generate-dis'}

#This is for creating a default user in the database
default_user = 'admin'
default_hostname = 'admin.org'

#This is the debug variable for print statments - 0 = no messages, 1 = some, 2 = all messages. Initalized to 1
DEBUG = 0
debug_short = '-d'
debug_long = 'debug'
debug_longdash ='--'+debug_long
debug_default = DEBUG
debug_help = help = """0 (default) - no messages,1 - general messages,
                    2 - all messages, all reads and writes into and out of the database"""

gcard_identifying_text = '.gcard' #For use in gcard_helper.py
gcard_default = '/jlab/work/clas12.gcard'
