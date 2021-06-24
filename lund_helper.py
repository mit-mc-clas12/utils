#****************************************************************
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
#***************************************************************
from __future__ import print_function
import argparse, subprocess, os, sys
import utils, fs, html_reader
import glob 

def Lund_Entry(lund_location, lund_download_dir="lund_dir/"):
    valid_lund_extensions = ['.dat', '.txt', '.lund']

    #Make sure lund_download_dir ends with a /, and if not, add one.
    if lund_download_dir[-1] != "/":
                    lund_download_dir += "/"

    # A case used to work around not downloading for types 1/3
    if lund_location == "no_download":
        print('Not downloading files due to SCard type.')
        return lund_location
    elif os.path.exists(lund_download_dir):
        print('Lund directory already exists, not downloading again.')
        return lund_download_dir 

 
    # Create dir. to download / copy files into 
    try:
        subprocess.call(['mkdir', '-p', lund_download_dir])
    except Exception as e:
            print("WARNING: unable to make directory {}".format(lund_download_dir))
            print("The error encountered was: \n {}".format(e))
            f = open("lundException.txt", "a")
            f.write("\n an exception was encountered at {}, see below: \n".format(utils.gettime()))
            f.write(str(e))
            f.close()

    
    ##################################################################
    # Case 3/4 - download single / multiple files from online location
    ##################################################################
    if 'http' in lund_location:
        # Download single web file 
        if any([ext in lund_location for ext in valid_lund_extensions]): 
            lund_dir_unformatted = lund_location.split("/")
            lund_filename = lund_dir_unformatted[-1] # the gets the name of the lund file, assuming the format is http......./lund_file_name
            #Pass the location, file, and download dir to the downloader function
            Lund_Downloader(lund_url_base = lund_location,lund_download_dir = lund_download_dir, lund_filename = lund_filename)  
        # Download entire web directory
        else:
            try:
                #Read the given location to find all the lund files
                raw_html, lund_filenames = html_reader.html_reader(lund_location, valid_lund_extensions)
            except Exception as e:
                print("ERROR: unable to download lund files from {}".format(lund_location))
                print("The error encountered was: \n {}".format(e))
                f = open("lundException.txt", "a")
                f.write("\n an exception was encountered at {}, see below: \n".format(utils.gettime()))
                f.write(str(e))
                f.close()
                exit()

            if len(lund_filenames) == 0:
                print("No Lund files found (they must end in '{}'). Is the online repository correct?".format(valid_lund_extensions))
                exit()
            #Loop through downloading every LUND file in directory
            for lund_filename in lund_filenames:
                Lund_Downloader(lund_url_base = lund_location,lund_download_dir = lund_download_dir, lund_filename = lund_filename, single_file = False)  
   
   
    #######################################################################
    # Case 1/2 - Use RSync to copy files from a jlab location to OSG
    # RSYNC option: rlpgoD replaces -a (rlptgoD) so time is not preserved:
    # When copied, the files will have a new timestamp, which will play
    # nice with our autodeletion cronjobs
    ######################################################################
    else:
        # Single local file 
        if any([ext in lund_location for ext in valid_lund_extensions]):
            try:
                #print("Trying to copy Lund file from {}".format(lund_location))
                if lund_location[0] != "/":
                    lund_location = "/"+lund_location
                
                #Example full filepath: gemc@dtn1902-ib:/lustre19/expphy/volatile/clas12/robertej/testlund.txt
                lund_copy_path = 'gemc@dtn1902-ib:/lustre19/expphy'+lund_location
                subprocess.call(['rsync', '-rlpgoD', lund_copy_path, lund_download_dir])
            except Exception as e:
                print("ERROR: unable to copy lund files from {}".format(lund_location))
                print("The error encountered was: \n {}".format(e))
                f = open("lundException.txt", "a")
                f.write("\n an exception was encountered at {}, see below: \n".format(utils.gettime()))
                f.write(str(e))
                f.close()
        # Local directory, many files
        else:
            if lund_location[0] != "/":
                    lund_location = "/"+lund_location
            if lund_location[-1] != "/":
                    lund_location += "/"
            if "/lustre19/expphy" not in lund_location: 
                    lund_location ='/lustre19/expphy'+lund_location
            #print("trying to rsync {}".format(lund_location))
            lund_copy_path = 'gemc@dtn1902-ib:'+lund_location

            #subprocess.call(['rsync', '-a', lund_copy_path, lund_download_dir])
            subprocess.call(['rsync', '-zrlpgoDv','--prune-empty-dirs',"--include='*.dat'",
                    "--include='*.txt'","--exclude='*'",lund_copy_path, lund_download_dir])

            files = os.listdir(lund_download_dir)
            for f in files:
                if not any([ext in f for ext in valid_lund_extensions]):
                    os.remove(lund_download_dir+f)
                    
    return lund_download_dir


# Lund_Downloader() is a helper function which takes as input:
# lund_url_base - the full url to an online lund file directory (e.g. )
# lund_filename - the name of the lund file
# lund_download_dir - the full path to where the lund file should be downloaded to
def Lund_Downloader(lund_url_base,lund_download_dir,lund_filename,single_file=True):
        lund_content = ""
        try:
            #print("Trying to download {} file from {}".format(lund_filename,lund_url_base))
            full_lund_path = lund_url_base
            if not single_file:
                full_lund_path += "/"+lund_filename
            lund_raw_text = html_reader.html_reader(full_lund_path)[0]#This returns a tuple, we need the contents of the tuple
            lund_raw_text = str(lund_raw_text) #This might not be needed, converts from bytes to strings
            lund_content = lund_raw_text.replace('"',"'") #This isn't strictly needed but SQLite can't read " into data fields, only ' characters
            #print("Downloaded {}".format(full_lund_path))
        except Exception as e:
            print("Unable to download lund file sucessfully.")
            print("The error encountered was: \n {}".format(e))
            f = open("lundException.txt", "a")
            f.write("\n an exception was encountered at {}, see below: \n".format(utils.gettime()))
            f.write(str(e))
            f.close()
        if len(lund_content)>0:
            try:
                #print("Trying to save {}".format(lund_filename))
                filename = lund_download_dir+"/"+lund_filename
                with open(filename,"a") as file: file.write(lund_content)
                #print("Saved {} to {}{}".format(lund_filename,lund_download_dir,lund_filename))
            except Exception as e:
                print("Unable to save lund file sucessfully.")
                print("The error encountered was: \n {}".format(e))
                f = open("lundException.txt", "a")
                f.write("\n an exception was encountered at {}, see below: \n".format(utils.gettime()))
                f.write(str(e))
                f.close()




#Comment regarding the count_files() function below:
#I'm not sure where or if this function is still used in the codebase,
#But I didn't touch it. robertej@mit.edu - 4/13/21
def count_files(url_dir):
    """ 
    We need to know how many files are going 
    to be downloaded before we do this job.  This 
    is used in the queue system.

    Inputs:
    -------
    - url_dir (str) - Specifies the location of the 
    lund files. 

    Returns:
    --------
    - nfiles (int) - The number of files to be downloaded. 

    """
    lund_extensions = ['.dat', '.txt', '.lund']

    # A case used to work around not downloading for types 1/3
    if url_dir == "no_download":
        print('Not downloading files due to SCard type.')
        return 0

    # Case 3/4
    if 'http' in url_dir:
        
        # Single web file 
        if any([ext in url_dir for ext in lund_extensions]):
            return 1 

        # Web directory 
        else:
            raw_html, lund_urls = html_reader.html_reader(url_dir, fs.lund_identifying_text)
            return len(lund_urls)

    # Case 1/2
    else:

        # Single local file 
        if any([ext in url_dir for ext in lund_extensions]):
            return 1 

        # Local directory, many files 
        else:
            lund_files = glob.glob(url_dir + '*')
            return len(lund_files)

    # Something weird happened. 
    return 0 

if __name__ == '__main__':
    """For testing purposes"""
    # https test, full directory
    #Lund_Entry('https://userweb.jlab.org/~ungaro/lund/')
    Lund_Downloader("https://userweb.jlab.org/~ungaro/lnd/",".","test.txt",single_file=True)
    
