"""

Disk usage utility.

"""

import argparse
import json
import os
import subprocess
import shutil

# global dictionary to reduce runtime 
# on repeat file counts 
cached = {}

def sub_dirs(target_dir):
    return [d for d in os.listdir(target_dir) if os.path.isdir(target_dir + '/' + d)]

def folder_size(target_dir):
    """
    https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
    """

    total_size = os.path.getsize(target_dir)

    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)

        if os.path.isfile(item_path):
            if item_path in cached:
                total_size += cached[item_path]
            else:
                cached[item_path] = os.path.getsize(item_path)
                total_size += cached[item_path]

        elif os.path.isdir(item_path):
            if item_path in cached:
                total_size += cached[item_path]
            else:
                cached[item_path] = folder_size(item_path)
                total_size += cached[item_path]

    return total_size

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=str)
    args = parser.parse_args()

    target_dir = '/volatile/clas12/osg/'

    user_dirs = {} 
    for user_dir in sub_dirs(target_dir):
        user_dirs[user_dir] = folder_size(os.path.join(target_dir, user_dir))
        
    json_dict = {} 
    for user_dir, dir_size in user_dirs.items(): 
        json_dict[user_dir] = {} 
        json_dict[user_dir]['total_size'] = dir_size 
        json_dict[user_dir]['sub_directories'] = [] 
        
        for sub_dir in sub_dirs(os.path.join(target_dir, user_dir)):
            sub_dir_stats = {}
            sub_dir_stats['name'] = sub_dir
            sub_dir_stats['size'] = folder_size(os.path.join(target_dir, user_dir, sub_dir))
            json_dict[user_dir]['sub_directories'].append(sub_dir_stats)

    with open(args.output, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)
