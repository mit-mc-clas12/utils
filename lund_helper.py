# ****************************************************************
"""
 Download or copy lund files and return the name of 
    the target directory. 

    Inputs: 
    -------
    lund_location - A string containing the directory or path to lund file(s).

    Returns: 
    --------
    lund_download_dir - A string containing the name of the downloaded directory.

    A few cases can occur: 

    1) One local file, extension will be .txt, .dat, or .lund and the string 
       will not contain http. 
    2) Several local files, no extension will be given.  The string will not 
       contain http. 
    3) One web file, extension will be .txt, .dat, or .lund and the string 
       will contain http. 
    4) Many web files, no extension will be given.  The string will contain http. 

    Example values for lund_location:
    Online Directory - 'https://userweb.jlab.org/~ungaro/lund/'
    Online Directory typo - 'https://userweb.jlab.org/~ungaro/lund'
    
    Online file -   'https://userweb.jlab.org/~ungaro/lund/clasdis1.txt'

    Local Directory - /volatile/clas12/robertej/trans_test/
    Local Directory typo 1 - /volatile/clas12/robertej/trans_test/
    Local Directory typo 2 - volatile/clas12/robertej/trans_test/
    Local Directory typo 3 - volatile/clas12/robertej/trans_test

    Local File - /volatile/clas12/robertej/trans_test/rad.lund
    Local File typo - volatile/clas12/robertej/trans_test/rad.lund
"""
# ***************************************************************

import argparse, subprocess, os, sys
import utils, fs, html_reader
import glob

env = os.environ.copy()
env["XDG_RUNTIME_DIR"] = "/run/user/6635"
env["BEARER_TOKEN_FILE"] = "/var/run/user/6635/bt_u6635"


def Lund_Entry(lund_location, lund_files="lund_files"):
	valid_lund_extensions = ['.dat', '.txt', '.lund']

	# A case used to work around not downloading for types 1/3
	if lund_location == "no_download":
		print('Not downloading files due to SCard type.')
		return lund_location

	#######################################################
	# Use pelican to copy files from a jlab location to OSG
	#######################################################
	if '/volatile/clas12' in lund_location:
		lund_pelican_path = lund_location

		# Swap 'volatile' and 'clas12' → '/clas12/volatile/...'
		#    Example: '/volatile/clas12/user2/exp1/exp2'
		#          →  '/clas12/volatile/user2/exp1/exp2'
		lund_pelican_path = lund_pelican_path.replace(
			"/volatile/clas12/", "/clas12/volatile/", 1
		)

		# Prefix 'osdf:///hello-osdf/' to lund_pelican_path
		#    Result: 'osdf:///hello-osdf/clas12/volatile/...'
		lund_pelican_path = "osdf:///jlab-osdf" + lund_pelican_path

		# write list of files, filter, and save to 'tmp_lund_files'
		result = subprocess.run(
			['pelican', 'object', 'ls', lund_pelican_path],
			env=env,
			stdout=subprocess.PIPE,
			text=True,
			check=True,
		)

		allowed_ext = {'.txt', '.lund', '.dat'}

		lines = result.stdout.splitlines()
		filtered = [
			line for line in lines
			if os.path.splitext(line)[1] in allowed_ext
		]

		with open(lund_files, 'w') as f:
			f.write('\n'.join(filtered) + '\n')


	else:
		raise ValueError(
			f"lund_location must contain /volatile/clas12/ "
		)
	return lund_files


def count_files(lund_location):
	"""
	Use `pelican object ls` on `lund_location` and return
	the number of entries ending in .txt, .lund, or .dat.
	"""
	# Run pelican ls
	result = subprocess.run(
		["pelican", "object", "ls", lund_location],
		stdout=subprocess.PIPE,
		text=True,
		check=True,
	)

	allowed_ext = {".txt", ".lund", ".dat"}

	lines = [
		line.strip()
		for line in result.stdout.splitlines()
		if line.strip()
	]

	filtered = [
		line for line in lines
		if os.path.splitext(line)[1] in allowed_ext
	]

	return len(filtered)


# Lund_Downloader() is a helper function which takes as input:
# lund_url_base - the full url to an online lund file directory (e.g. )
# lund_filename - the name of the lund file
# lund_download_dir - the full path to where the lund file should be downloaded to
# this should be done with pycurl
def Lund_Downloader(lund_url_base, lund_download_dir, lund_filename, single_file=True):
	lund_content = ""
	try:
		# print("Trying to download {} file from {}".format(lund_filename,lund_url_base))
		full_lund_path = lund_url_base
		if not single_file:
			full_lund_path += "/" + lund_filename
		lund_raw_text = html_reader.html_reader(full_lund_path)[
			0]  # This returns a tuple, we need the contents of the tuple
		lund_raw_text = str(lund_raw_text.decode(
			'ascii'))  # This might not be needed, converts from bytes to strings
		lund_content = lund_raw_text.replace('"',
		                                     "'")  # This isn't strictly needed but SQLite can't read " into data fields, only ' characters
	# print("Downloaded {}".format(full_lund_path))
	except Exception as e:
		print("Unable to download lund file sucessfully.")
		print("The error encountered was: \n {}".format(e))
		f = open("lundException.txt", "a")
		f.write("\n an exception was encountered at {}, see below: \n".format(utils.gettime()))
		f.write(str(e))
		f.close()
	if len(lund_content) > 0:
		try:
			# print("Trying to save {}".format(lund_filename))
			filename = lund_download_dir + "/" + lund_filename
			with open(filename, "a") as file:
				file.write(lund_content)
		# print("Saved {} to {}{}".format(lund_filename,lund_download_dir,lund_filename))
		except Exception as e:
			print("Unable to save lund file sucessfully.")
			print("The error encountered was: \n {}".format(e))
			f = open("lundException.txt", "a")
			f.write("\n an exception was encountered at {}, see below: \n".format(utils.gettime()))
			f.write(str(e))
			f.close()


if __name__ == '__main__':
	"""For testing purposes"""
	# https test, full directory
	# Lund_Entry('https://userweb.jlab.org/~ungaro/lund/')
	Lund_Downloader("https://userweb.jlab.org/~ungaro/lnd/", ".", "test.txt", single_file=True)
