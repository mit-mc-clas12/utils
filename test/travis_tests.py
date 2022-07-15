import subprocess
import os
from . import readtests

def test_function(command):
	process = subprocess.Popen(command.command,
		stdout=subprocess.PIPE, 
		stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()


	if command.expect_out != '0':
		if stdout == command.expect_out:
			return(stdout,stderr)
		else:
			err_mess = str(stderr) + "unexpected sdtout of: " + str(stdout)
			return(stdout, err_mess)
	else:
		return(stdout,stderr)



test_folder= os.path.dirname(os.path.abspath(__file__))+'/clas12-test'
if os.path.isdir(test_folder):
	print('removing previous database file')
	subprocess.call(['rm','-rf',test_folder])
if os.path.isdir(test_folder):
	print('removing previous database file')
	subprocess.call(['rm','-rf',test_folder])
else:
	print((test_folder+" is not present, not deleteing"))



subprocess.call(['mkdir','-p',test_folder])
print((test_folder+" is now present"))



#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)+'/clas12-test'
os.chdir(test_folder)

f = open('msqlrw.txt',"w")
f.write("root\n")
f.write(" ")
f.close()


folders = ['utils','server','client']
for folder in folders:
	folder_name= os.path.dirname(os.path.abspath(__file__))+'/'+folder
	if not os.path.isdir(folder_name):
		print(('{0} not found, cloning from github'.format(folder)))
		substring = 'https://github.com/robertej19/{0}.git'.format(folder)
		subprocess.call(['git','clone',substring])



filename = os.path.dirname(os.path.abspath(__file__))+'/utils/CLAS12OCR.db'
if os.path.isfile(filename):
	print('removing previous database file')
	subprocess.call(['rm',filename])


command_sequence = readtests.create_commands()

def run_through_tests(command_sequence):
	err_sum = 0 
	for command in command_sequence:
		out, err = test_function(command)
		print(('Testing command: {0}'.format(command.name)))
		if not err:
			print('... success')
			#print(out)
		else:
			print(out)
			print('... fail, error message:')
			print(err)
			err_sum += 1
			
	return err_sum



status = run_through_tests(command_sequence)
if status > 0:
	exit(1)
else:
	exit(0)



"""
#which condor_submit if val = 0, do not submit, print not found message
"""
