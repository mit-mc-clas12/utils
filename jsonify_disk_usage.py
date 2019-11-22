"""

Disk usage utility.

"""

import argparse
import json


def tokenize(line):
    return line.strip().split()

def line_is_accepted(line):
    tokens = tokenize(line)
    
    if len(tokens) != 2:
        return False 
    if tokens[1] == '.':
        return False

    return True

def is_subdir(folder_name):
    return (len(folder_name.split('/')) == 3)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--logfile', required=True, type=str)
    parser.add_argument('--output', required=True, type=str)
    args = parser.parse_args()

    json_dict = {}

    with open(args.logfile, 'r') as log_file:
        log = log_file.readlines() 

    lines = [tokenize(line) for line in log if line_is_accepted(line)]
    for line in lines:
        size = line[0]
        user_dir = line[1]
        user = user_dir.split('/')[1]
        
        if user not in json_dict:
            json_dict[user] = {} 
            json_dict[user]['sub_directories'] = [] 

        if is_subdir(user_dir):
            json_dict[user]['sub_directories'].append(
                {'name': user_dir.split('/')[2], 'size': size}
            )
        else:
            json_dict[user]['total_size'] = size
            
    with open(args.output, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)
