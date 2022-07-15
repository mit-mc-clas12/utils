import json
import pandas as pd


def shouldBeSubmitted(user_name,json_file="/u/group/clas/www/gemc/html/web_interface/data/osgLog.json",idle_limit=50000):
    # Open JSON file and load as dictionary
    f = open(json_file,)
    data = json.load(f)
    f.close()

    # Convert the user info from a dict to a pandas Dataframe
    df = pd.DataFrame(data["user_data"])

    # The integer values were stored as strings, need to convert to floats
    df[["total", "done","run","idle","hold"]] = df[["total", "done","run","idle","hold"]].apply(pd.to_numeric)

    # Sum the number of idle jobs for each unique username
    users_idle_totals = df.groupby(['user'])['idle'].sum().to_frame()

    # Get a list of users with more than idle_limit number of idle jobs
    users_over_limit = users_idle_totals.query('idle > 10000').index.tolist()
    #print("Users with more than {} idle jobs are: \n {}".format(idle_limit,users_over_limit))

    if user_name in users_over_limit:
        return True
    else:
        return False

if __name__ == "__main__":
    idle_limit = 10000  # Set the threshold of idle jobs
    user_name = "testuser"
    bool_over_limit = shouldBeSubmitted(user_name,"example.json",idle_limit)
    print(("{} over {}: {}".format(user_name, idle_limit, bool_over_limit)))


