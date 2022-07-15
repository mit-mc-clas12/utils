"""

Disk usage utility.

"""

import argparse
import json
from collections import OrderedDict 

def tokenize(line):
    return line.strip().split()

def line_is_accepted(line):
    tokens = tokenize(line)
    
    if len(tokens) != 1:
        return False 
    if tokens[0] == '.':
        return False

    return True

def is_subdir(folder_name):
    return (len(folder_name.split('/')) == 3)

def create_ordered_dict(data, sort_key='total_size'):

    def giga_stripper(line):
        return int(line[:-1])

    output = OrderedDict()    
    users = list(data.keys()) 
    sizes = [giga_stripper(d[sort_key]) for d in list(data.values())]
    
    for size, user in sorted(zip(sizes, users))[::-1]:
        output[user] = data[user]
        output[user]['sub_directories'] = sorted(data[user]['sub_directories'], 
                                                 key=lambda x: giga_stripper(x['size']))[::-1]

    return output 

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
        user_dir = line[0]
        user = user_dir.split('/')[1]
        
        if user not in json_dict:
            json_dict[user] = {} 
            json_dict[user]['sub_directories'] = [] 

        if is_subdir(user_dir):
            json_dict[user]['sub_directories'].append(
                {'name': user_dir.split('/')[2]}
            )

    with open(args.output, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)
#        json.dump(create_ordered_dict(json_dict), json_file, indent=4)
