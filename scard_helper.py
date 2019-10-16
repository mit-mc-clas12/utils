#****************************************************************
"""
# This file reads the text of the scard, validates the information,
# and writes it into the scard table in the database.
# Some effort should be developed to sanitize the scard to prevent
# against sql injection attacks
"""
#****************************************************************

from __future__ import print_function
import sqlite3, time
import utils, fs

class scard_class:
    def __init__(self,scard_text):
        self.name = 'scard.txt'
        self.data = {}
        self.parse_scard(scard_text)

    def parse_scard(self, scard_text):
        scard_lines = scard_text.split("\n")
        for linenum, line in enumerate(scard_lines):
            if not line:
              print("Reached end of scard")
              break
            pos_delimeter_colon = line.find(":")
            pos_delimeter_hash = line.find("#")
            key   =  line[:pos_delimeter_colon].strip()
            value =  line[pos_delimeter_colon+1:pos_delimeter_hash].strip()
            if key == "generator" and not 'http' in value:
              if key != fs.scard_key[linenum]:
                utils.printer("ERROR: Line {0} of the steering card has the key '{1}''.".format(linenum+1,key))
                utils.printer("That line must have the key '{0}'.".format(fs.scard_key[linenum]))
            self.data[key] = value

    def validate_scard_line(self, linenum, line):
        if line.count("#") ==0:
            utils.printer("Warning: No comment in line {0}.".format(linenum+1))
        elif line.count("#")>1:
            utils.printer("ERROR: number of hashes>1 in line {0}".format(linenum+1))
            utils.printer("# can be used only as a delimeter and only once per line. Edit scard to fix.")
            exit()
        if line.count(":") ==0:
            utils.printer("ERROR: No colon in line {0}".format(linenum+1))
            utils.printer("The data cannot be interpreted. Stopped.")
            exit()

def SCard_Entry(UserSubmissionID,timestamp,scard_dict):
    strn = """INSERT INTO Scards(UserSubmissionID,timestamp) VALUES ("{0}","{1}");""".format(UserSubmissionID,timestamp)
    utils.db_write(strn)
    for key in scard_dict:
      strn = "UPDATE Scards SET {0} = '{1}' WHERE UserSubmissionID = {2};".format(key,scard_dict[key],UserSubmissionID)
      utils.db_write(strn)
    utils.printer("SCard record added to database corresponding to UserSubmissionID {0}".format(UserSubmissionID))
