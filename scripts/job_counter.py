import json


def shouldBeSubmitted(user_name,json_file="/u/group/clas/www/gemc/html/web_interface/data/osgLog.json",idle_limit=1000000):
    # Open JSON file and load as dictionary
    f = open(json_file,)
    data = json.load(f)
    f.close()

    #Convert json data into useable dictionary
    user_info = {}
    columns = ['total','done','run','idle','hold']

    for job in data['user_data']:
        if not job['user'] in user_info.keys():
            user_info[job['user']] = {}
            for c in columns:
                user_info[job['user']][c] = int(job[c])
        else:
            for c in columns:
                user_info[job['user']][c] += int(job[c])

    # Perform logic
    user = user_info[user_name]
    if (user['idle']+user['run'])>idle_limit:
        return True
    else:
        return False


if __name__ == "__main__":
    idle_limit = 10000  # Set the threshold of idle jobs
    user_name = "robertej"
    bool_over_limit = shouldBeSubmitted(user_name,"example.json",idle_limit)
    print("{} over {}: {}".format(user_name, idle_limit, bool_over_limit))


