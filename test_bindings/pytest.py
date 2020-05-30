
set = [222,222,222,223,224,225,222,223,225,255,225,242]


users = []
jobs = []
for item in set:
    if item in users:
        print("item already in users")
        jobs[users.index(item)] = jobs[users.index(item)] +1
    else:
        users.append(item)
        jobs.append(1)

print(jobs)
print("final users list")
print(users)
print(users[users.index(223)])
