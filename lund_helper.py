#****************************************************************
"""
### THE BELOW TEXT IS OUTDATED and needs to be updated

#This replaces a previous version of gcard_helper.py by using the HTMLParser class
#This allows for more robust parsing of the html mother directory to find gcard files
#Even better would be to use BeautifulSoup, which would allow for the code to be condensed as:
#```import requests
#from bs4 import BeautifulSoup
#page = requests.get('http://www.website.com')
#bs = BeautifulSoup(page.content, features='lxml')
#for link in bs.findAll('a'):
#    print(link.get('href'))```
#Unfortunately, this module must be imported and cannot be gaurannted that it will be on whatever
#server this software will live on, so it is safer to instead use HTMLParser which is more common
####
#This file takes in a UserSubmissionID and gcard url from db_batch_entry and passes it through
#a few functions to download the gcards from the specified location and to enter them into the
#appropriate gcard table in the database.
# Some effort should be developed to sanitize the gcard files to prevent
# against sql injection attacks
"""
#***************************************************************
from __future__ import print_function
import argparse, subprocess, os
import utils, fs, html_reader
import glob 

def Lund_Downloader(url_dir,lund_urls,lund_dir):
    if len(lund_urls) == 0:
        print("No Lund files found (they must end in '{0}'). Is the online repository correct?".format(fs.lund_identifying_text ))
        exit()
    else:
        for url_ending in lund_urls:
            utils.printer('Lund URL name is: '+url_ending)
            lund_text = html_reader.html_reader(url_dir+'/'+url_ending,'')[0]#This returns a tuple, we need the contents of the tuple
            utils.printer2('HTML from lund link is: {0}'.format(lund_text))
            lund_text_db = lund_text.replace('"',"'") #This isn't strictly needed but SQLite can't read " into data fields, only ' characters
            print("\t Gathered lund file '{0}'".format(url_ending))
            filename = lund_dir+"/"+url_ending
            with open(filename,"a") as file: file.write(lund_text_db)

def Lund_Entry(url_dir, target_dir):
    """ Download or copy lund files and return the name of 
    the target directory. 

    Inputs: 
    -------
    url_dir - A string containing the directory or path to lund file(s).

    Returns: 
    --------
    lund_dir - A string containing the name of the downloaded directory.

    A few cases can occur: 

    1) One local file, extension will be .txt, .dat, or .lund and the string 
       will not contain http. 
    2) Several local files, no extension will be given.  The string will not 
       contain http. 
    3) One web file, extension will be .txt, .dat, or .lund and the string 
       will contain http. 
    4) Many web files, no extension will be given.  The string will contain http. 

    """

    lund_extensions = ['.dat', '.txt', '.lund']
    lund_dir = target_dir

    if os.path.exists(lund_dir):
        print('Lund directory already exists, not downloading again.')
        return lund_dir 

    # Create dir. 
    subprocess.call(['mkdir', '-p', lund_dir])

    # Case 3/4
    if 'http' in url_dir:
        
        # Single web file 
        if any([ext in url_dir for ext in lund_extensions]):
            lund_dir_unformatted = url_dir.split("/")
            filename = lund_dir_unformatted[len(lund_dir_unformatted)-1]

            lund_text = html_reader.html_reader(url_dir,'')[0]#This returns a tuple, we need the contents of the tuple
            utils.printer2('HTML from lund link is: {0}'.format(lund_text))
            lund_text_db = lund_text.replace('"',"'") #This isn't strictly needed but SQLite can't read " into data fields, only ' characters
            print("\t Gathered lund file '{0}'".format(url_dir))
            with open(lund_dir+"/"+filename,"a") as file: 
                    file.write(lund_text_db)
                    
        # Web directory 
        else:
            raw_html, lund_urls = html_reader.html_reader(url_dir, fs.lund_identifying_text)
            lund_dir_unformatted = url_dir.split("//")[1]
            subprocess.call(['mkdir','-p',lund_dir])
            Lund_Downloader(url_dir,lund_urls,lund_dir)

    # Case 1/2
    else:

        # Single local file 
        if any([ext in url_dir for ext in lund_extensions]):
            subprocess.call(['cp', url_dir, lund_dir + '/'])

        # Local directory, many files 
        else:
            print('Downloading all files in {}'.format(url_dir))

            lund_files = glob.glob(url_dir + '*')
            print(lund_files)
            
            for lf in lund_files:
                if any([ext in lf for ext in lund_extensions]):
                    subprocess.call(['cp', lf, lund_dir+'/'])

    return lund_dir
                
