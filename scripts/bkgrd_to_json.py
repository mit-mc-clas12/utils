#!/usr/bin/env python

import os

def path_hierarchy(path):
    hierarchy = {} #initialize main array

    for contents in os.listdir(path): #loop over the contents of the top directory
        if os.path.isdir(os.path.join(path,contents)): #check if content is directory (and not file)
            subhierarchy = {} #initialize an array of lists
            for contents2 in os.listdir(os.path.join(path, contents)): #loop over contents of daughter directory
                list = [] #initialize list of granddaughter directories
                if os.path.isdir(os.path.join(path, contents, contents2)): #check if content of daughter directory is a directory
                    subhierarchy[contents2] = list
                    for contents3 in os.listdir(os.path.join(path, contents, contents2)): #loop over contents of granddaughter directory
                        if os.path.isdir(os.path.join(path, contents, contents2,contents3)): #check if content of granddaughter directory is a directory
                            list.append(contents3) #add granddaughter directory to list
            hierarchy[contents] = subhierarchy #add daughter array to main array

    return hierarchy

if __name__ == '__main__':
    import json
    import sys
    import argparse

    parser = argparse.ArgumentParser() #parser for command line options

    #define command line options
    parser.add_argument("-b", "--bkgrd", help="background files location", default="/work/osgpool/hallb/clas12/backgroundfiles/")
    parser.add_argument("-test", "--outdir", help="output directory location", default="/group/clas/www/gemc/html/web_interface/xrootd/")

    #collect command line options
    args = parser.parse_args()

<<<<<<< Updated upstream:scripts/bkgrd_to_json.py
#    try:
#        directory = sys.argv[1]
#        directory = args.outdir
#    except IndexError:
#        directory = "/work/osgpool/hallb/clas12/backgroundfiles/"

    

<<<<<<< HEAD:bkgrd_to_json.py
#    with open('xrootd.json', 'w') as f:
    with open(os.path.join(args.outdir,'xrootd.json'), 'w') as f:
        print(json.dump(path_hierarchy(args.bkgrd), f, indent=2, sort_keys=False))
=======
    with open('/group/clas/www/gemc/html/web_interface/data/xrootd.json', 'w') as f:
        print(json.dump(path_hierarchy(directory), f, indent=2, sort_keys=False))
>>>>>>> upstream/master:scripts/bkgrd_to_json.py
=======
    with open(os.path.join(args.outdir,'xrootd.json'), 'w') as f: #open xrootd.json
        print(json.dump(path_hierarchy(args.bkgrd), f, indent=2, sort_keys=False)) #call main function and print output in json format
>>>>>>> Stashed changes:bkgrd_to_json.py
