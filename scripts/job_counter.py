import json

# to execute:
# python /home/gemc/software/Submit/utils/scripts/job_counter.py
# called also by
# python /home/gemc/software/Submit/utils/update_priority.py -j /home/gemc/logs/osgLog.json -u 

def shouldBeSubmitted(user_name, json_file="/home/gemc/logs/osgLog.json", idle_limit=1000000):
    # Open JSON file and load as dictionary
    f = open(json_file,)
    data = json.load(f)
    f.close()

    # Convert json data into useable dictionary
    user_info = {}
    columns = ['total','done','run','idle','hold']

    for job in data['user_data']:
        if not job['user'] in user_info.keys():
            user_info[job['user']] = {}
            for c in columns:
                if job[c] != 'No data':
                    user_info[job['user']][c] = int(job[c])
                else:
                    user_info[job['user']][c] = 0
        else:
            for c in columns:
                user_info[job['user']][c] += int(job[c])

    # Perform logic
    if user_name in user_info:
        user = user_info[user_name]
        if (user['idle']+user['run'])>idle_limit:
            return False
        else:
            return True
    else:
        return True

if __name__ == "__main__":
    idle_limit = 10000  # Set the threshold of idle jobs
    user_name = "robertej"
    bool_submit = shouldBeSubmitted(user_name,"/home/gemc/logs/osgLog.json",idle_limit)
    print("{} over {}. Should submit: {}".format(user_name, idle_limit, bool_submit))
