#****************************************************************
"""
# File Description
"""
#****************************************************************


from . import utils, fs
import sqlite3, argparse

def get_args():
  utils.printer2("Getting arguments from command line")
  argparser = argparse.ArgumentParser()
  argparser.add_argument('-b','--UserSubmissionID', default='none', help = 'Enter the ID# of the batch you want to submit (e.g. -b 23)')
  argparser.add_argument('-t','--test', help = 'Use this flag (no arguments) if you are NOT on a farm node and want to test the submission flag (-s)', action = 'store_true')
  argparser.add_argument('-s','--submit', help = 'Use this flag (no arguments) if you want to submit the job', action = 'store_true')
  argparser.add_argument('-w','--write_files', help = 'Use this flag (no arguments) if you want submission files to be written out to text files', action = 'store_true')
  argparser.add_argument('-y','--scard_type', default='0', help = 'Enter scard type (e.g. -y 1 for submitting type 1 scards)')
  argparser.add_argument(fs.debug_short,fs.debug_longdash, default = fs.debug_default,help = fs.debug_help)
  argparser.add_argument('-l','--lite',help = "use -l or --lite to connect to sqlite DB, otherwise use MySQL DB", type=str, default=None)
  argparser.add_argument('-o','--OutputDir', default='none', help = 'Enter full path of your desired output directory, e.g. /u/home/robertej')
  argparser.add_argument('--test_database', action='store_true', default=False, help='Use testing database (MySQL)')
  args = argparser.parse_args()

  fs.DEBUG = getattr(args,fs.debug_long)
  fs.use_mysql = False if args.lite else True

  if not args.lite:
    with open(fs.dirname+'/../msqlrw.txt','r') as myfile: #msql.txt is a file that contains two line: first line is username, second line is password
    #This is a temporary fix, need to store the password information outside of github
      login=myfile.read().replace('\n', ' ')
      login_params = login.split()
      fs.mysql_uname = login_params[0]

      #Need to handle the case where the password is null
      if len(login_params) < 2:
        fs.mysql_psswrd = ""      
      else:
        fs.mysql_psswrd =  login_params[1]
  return args


def get_args_client():
  utils.printer2("Getting arguments from command line")
  argparser = argparse.ArgumentParser()
  argparser.add_argument('scard',help = 'relative path and name scard you want to submit, e.g. ../scard.txt',nargs='?',)
  argparser.add_argument(fs.debug_short,fs.debug_longdash, default = fs.debug_default,help = fs.debug_help)
  argparser.add_argument('-l','--lite',help = "use -l or --lite to connect to sqlite DB, otherwise use MySQL DB", action = 'store_true')
  argparser.add_argument('-u','--username', default=None, help = 'Enter user ID for web-interface, Only if \'whoami\' is \'gemc\'')
  args = argparser.parse_args()

  fs.DEBUG = getattr(args,fs.debug_long)
  fs.use_mysql = not args.lite

  if not args.lite:
    with open(fs.dirname+'/../msqlrw.txt','r') as myfile: #msql.txt is a file that contains two line: first line is username, second line is password
    #This is a temporary fix, need to store the password information outside of github
      login=myfile.read().replace('\n', ' ')
      login_params = login.split()
      fs.mysql_uname = login_params[0]
      fs.mysql_psswrd =  login_params[1]

  return args
