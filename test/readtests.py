


class command_class:
	def __init__(self,command_name,command_string,expected_output):
		self.name = command_name
		self.command = command_string
		self.expect_out = expected_output


def create_commands():

    create_mysql_db = command_class('Create MySQL DB',
                                    ['python2', 'utils/create_database.py'],
                                    '0')

    create_mysql_db_test = command_class('Create MySQL Test DB',
                                    ['python2', 'utils/create_database.py','--test_database'],
                                    '0')

    create_sqlite_db = command_class('Create SQLite DB',
                                    ['python2', 'utils/create_database.py','--lite=utils/CLAS12OCR.db'],
                                    '0')

    submit_scard_1 = command_class('Submit scard 1 on client through sqlite',
                                    ['python2', 'client/src/SubMit.py','--lite=utils/CLAS12OCR.db','-u=robertej','client/scards/scard_type1.txt'],
                                    '0')
                                    
    submit_scard_1_mysql = command_class('Submit scard 1 on client through MySQL CLAS12OCR db',
                                    ['python2', 'client/src/SubMit.py','-u=robertej','client/scards/scard_type1.txt'],
                                    '0')

    submit_scard_1_mysql_test = command_class('Submit scard 1 on client through MySQL CLAS12TEST db',
                                    ['python2', 'client/src/SubMit.py','--test_database','-u=robertej','client/scards/scard_type1.txt'],
                                    '0')

    #submit_scard_2 = command_class('Create scard 2 on client',
    #								['python2', 'client/src/SubMit.py','--lite=utils/CLAS12OCR.db','-u=robertej','client/scard_type2.txt'],
    #								'0')

    verify_submission_success = command_class('Verify scard submission success',
                                    ['sqlite3','utils/CLAS12OCR.db','SELECT user FROM submissions WHERE user_submission_id=1'],
                                    'robertej\n')


    submit_server_jobs_test_db = command_class('Submit jobs from server on CLAS12TEST',
                                    ['python2', 'server/src/Submit_UserSubmission.py', '-b','1', '--test_database', '-w', '-s', '-t'],
                                    '0')

    submit_server_jobs_prod_db = command_class('Submit jobs from server on CLAS12OCR',
                                    ['python2', 'server/src/Submit_UserSubmission.py', '-b','1', '-w', '-s', '-t'],
                                    '0')

    submit_server_jobs_sqlite = command_class('Submit jobs from server',
                                    ['python2', 'server/src/Submit_UserSubmission.py', '-b','1', '--lite=utils/CLAS12OCR.db', '-w', '-s', '-t'],
                                    '0')

    command_sequence = [create_mysql_db,create_mysql_db_test,create_sqlite_db, 
			submit_scard_1, submit_scard_1_mysql, submit_scard_1_mysql_test,
			 verify_submission_success,submit_server_jobs_sqlite]

    return command_sequence