#****************************************************************
"""
#This file inteacts with db_batch_entry and scard_helper to see from the scard
#if the user exists in the database. If not, the user gets added to the Database
#and the OS host is also added
"""
#****************************************************************

import sqlite3, time
import utils, fs, argparse, socket, subprocess
import datetime
from subprocess import PIPE, Popen
import os

def user_validation(args):
  #username = (subprocess.check_output('whoami'))[:-1]#The [:-1] is so we drop the implicit \n from the string
  #domain_name = subprocess.check_output(['hostname','-d'])#socket.getfqdn()  #socket.getdomain_name()
  username = Popen(['whoami'], stdout=PIPE).communicate()[0].split()[0]
  if username == 'gemc' or args.username != None:
    username = args.username

  is_travis = 'TRAVIS' in os.environ
  if is_travis == True:
  	print("We're at travis-ci environment")
  	fake_domain = "travis.dev"
  	domain_name = fake_domain
  else:
    #The following does not work on mac. This needs to get resolved, currently bridged over for testing
    #domain_name = Popen(['hostname',''-d'], stdout=PIPE).communicate()[0].split()[0]
    domain_name = "example_domain"

  strn = """SELECT 1 FROM Users WHERE EXISTS (SELECT 1 FROM Users WHERE User ="{0}"
          AND domain_name = "{1}")""".format(username,domain_name)
  user_already_exists = utils.db_grab(strn)
  if not user_already_exists:
    print("""\nThis is the first time {0} from {1} has submitted jobs. Adding user to database""".format(username,domain_name))
    strn = """INSERT INTO Users(User, domain_name, JoinDateStamp, Total_UserSubmissions,
              Total_Jobs, Total_Events, Most_Recent_Active_Date)
              VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}");""".format(
              username,domain_name,utils.gettime(),0,0,0,"Null")
    utils.db_write(strn)
  return username

def get_username():
  """Return the current users name as a string."""
  return Popen(['whoami'], stdout=PIPE).communicate()[0].split()[0]

def get_domain_name():
  """Return the current domain name as a string."""

  # Spit a dummy domain back 
  if 'TRAVIS' in os.environ:
    return 'travis.dev'

  else:
    return 'example_domain'
