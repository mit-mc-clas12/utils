#!/usr/bin/env python

import os

def path_hierarchy(path):
    hierarchy = {}

    for contents in os.listdir(path):
        if os.path.isdir(os.path.join(path,contents)):
            subhierarchy = {}
            for contents2 in os.listdir(os.path.join(path, contents)):
                list = []
                if os.path.isdir(os.path.join(path, contents, contents2)):
                    subhierarchy[contents2] = list
                    for contents3 in os.listdir(os.path.join(path, contents, contents2)):
                        if os.path.isdir(os.path.join(path, contents, contents2,contents3)):
                            list.append(contents3)
            hierarchy[contents] = subhierarchy

    return hierarchy

if __name__ == '__main__':
    import json
    import sys

    try:
        directory = sys.argv[1]
    except IndexError:
        directory = "/work/osgpool/hallb/clas12/backgroundfiles/"

#    with open('xrootd.json', 'w') as f:
    with open('/group/clas/www/gemc/html/web_interface/xrootd/xrootd.json', 'w') as f:
        print(json.dump(path_hierarchy(directory), f, indent=2, sort_keys=False))
