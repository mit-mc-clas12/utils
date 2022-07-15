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
#This file takes in a UserSubmissionID, unixtimestamp, and gcard url from db_batch_entry and passes it through
#a few functions to download the gcards from the specified location and to enter them into the
#appropriate gcard table in the database.
# Some effort should be developed to sanitize the gcard files to prevent
# against sql injection attacks
"""
#***************************************************************

import utils, fs, html_reader

def db_gcard_write(UserSubmissionID,timestamp,gcard_text):
    strn = "INSERT INTO Gcards(UserSubmissionID) VALUES ({0});".format(UserSubmissionID)
    utils.db_write(strn)
    strn = """UPDATE Gcards SET {0} = "{1}" WHERE UserSubmissionID = {2};""".format('gcard_text',gcard_text,UserSubmissionID)
    utils.db_write(strn)
    utils.printer("GCard added to database corresponding to UserSubmissionID {0}".format(UserSubmissionID))


def GCard_Entry(UserSubmissionID,unixtimestamp,url_dir):
  print("Gathering gcards from {0} ".format(url_dir))
  if not 'http' in url_dir: #== fs.gcard_default:
    utils.printer('Using gcard from /jlab/work')
    gcard_text_db = url_dir
    db_gcard_write(UserSubmissionID,unixtimestamp,gcard_text_db)
  elif 'http' in url_dir:
    utils.printer('Trying to download gcards from online repository')
    if '.gcard' in url_dir:
      utils.printer('Gcard URL name is: '+url_dir)
      gcard_text = html_reader.html_reader(url_dir,'')[0]#This returns a tuple, we need the contents of the tuple
      utils.printer2('HTML from gcard link is: {0}'.format(gcard_text))
      gcard_text_db = gcard_text.replace('"',"'")
      print("\t Gathered gcard '{0}'".format(url_dir))
      db_gcard_write(UserSubmissionID,unixtimestamp,gcard_text_db)
    else:
      raw_html, gcard_urls = html_reader.html_reader(url_dir,fs.gcard_identifying_text)
      if len(gcard_urls) == 0:
        print("No gcard files found (they must end in '{0}'). Is the online repository correct?".format(fs.gcard_identifying_text))
        exit()
      else:
        for url_ending in gcard_urls:
          utils.printer('Gcard URL name is: '+url_ending)
          gcard_text = html_reader.html_reader(url_dir+'/'+url_ending,'')[0]#This returns a tuple, we need the contents of the tuple
          utils.printer2('HTML from gcard link is: {0}'.format(gcard_text))
          gcard_text_db = gcard_text.replace('"',"'")
          print("\t Gathered gcard '{0}'".format(url_ending))
          db_gcard_write(UserSubmissionID,unixtimestamp,gcard_text_db)

  # I don't think this block can ever be reached 
  else:
    print('gcard not recognized as default option or online repository, please inspect scard')
    exit()


def download_gcards(url):
    """Download the gcard, or gcards that are located 
    at the url provided.  

    Input: 
    ------ 
    url - Gcard URL provided in the scard.

    Returns: 
    --------
    gcards - List of gcards from collected from URL. 


    To Do: 
    ------
    - Add logging to replace utils.printer commands removed. 

    """
    gcards = [] 
    
    if '.gcard' in url:
        # This returns a tuple, we need the contents of the tuple
        gcard = html_reader.html_reader(url,'')[0]
        gcards.append(gcard)

    # There could be an online directory that contains gcards
    # specified by the scard, here we need to search for the 
    # gcards that it contains and add them to our list. 
    else:
        raw_html, gcard_urls = html_reader.html_reader(url, fs.gcard_identifying_text)

        for url_ending in gcard_urls:
            # This returns a tuple, we need the contents of the tuple
            gcard = html_reader.html_reader(url + '/' + url_ending, '')[0]
            gcards.append(gcard)

    return [g.replace('"',"'") for g in gcards]
