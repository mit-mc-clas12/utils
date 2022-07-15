""" 

Informal tests to be replaced.

"""


import subprocess
import unittest 

from .gcard_helper import get_valid_gcards

class GCardHelperTest(unittest.TestCase):

    def setUp(self):
        gcard_file = """List of valid gcards in CVMFS image
        one.gcard, description 1 
        two.gcard, description 2 

        """
        self.temp_filename = 'temp_test.txt'

        with open(self.temp_filename, 'w') as tfile:
            tfile.write(gcard_file)

    def tearDown(self):
        subprocess.call(['rm', self.temp_filename])

    def test_get_valid_gcards(self):
        gcards = get_valid_gcards(self.temp_filename)

        self.assertTrue('one.gcard' in gcards)
        self.assertTrue('two.gcard' in gcards)
        self.assertFalse('List of valid gcards in CVMFS image' in gcards)
        
        # Make sure it doesn't take the leading line 
        # or the trailing empty line 
        self.assertTrue(len(gcards) == 2)

        

if __name__ == '__main__':
    unittest.main()
