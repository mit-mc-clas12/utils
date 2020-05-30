import htcondor
import classad

users = []
jobs = []

sched = htcondor.Schedd()

for job in schedd.xquery():
        if job.get("owner") == "gemc":
            user = str(job.get("ClusterID"))
            if user in users:
                jobs[users.index(user)] +=1
            else:
                users.append(user)
                jobs.append(1)
