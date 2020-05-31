"""
Logfile jsonification for monitoring.
"""
import htcondor
import classad

import get_args
import utils

def get_htcondor_q():
    schedd = htcondor.Schedd()

    batch_ids = []
    total_jobs_submitted = []
    total_jobs_running = []
    idle_jobs_counter = []
    running_jobs_counter = []
    jobs_start_dates = []

    for job in schedd.xquery(): #look through all jobs in condor
            if job.get("owner") == "gemc": #look only at jobs submitted by gemcRunning
                batch_id = str(job.get("ClusterID")) #get cluster id (batch ID) and convert from Long to string. Can also turn to int if want.
                job_status = int(job["JobStatus"]) #gets if the job is running (2) or idle (1)
		#print(type(job_status))
		#print(job_status)
                if batch_id in batch_ids:
                    total_jobs_running[batch_ids.index(batch_id)] += 1
                    if job_status == 1:
                        idle_jobs_counter[batch_ids.index(batch_id)] += 1
                    elif job_status == 2:
                        running_jobs_counter[batch_ids.index(batch_id)] += 1
                    else:
                        print("anomylous job status of {0}, investigate more".format(job_status))
                else:
                    printer("found new batch: {0}".format(batch_id),1)
                    total_jobs_for_batch = job.get("TotalSubmitProcs") #Get total number of jobs in batch submitted
                    start_date_unix = job.get("QDate")  #Get submitted date

                    batch_ids.append(batch_id)
                    total_jobs_submitted.append(int(total_jobs_for_batch)) #convert from long to int
                    jobs_start_dates.append(int(start_date_unix)) #convert from long to int

                    total_jobs_running.append(1) #initialzie entry for manual job counting
                    if job_status == 1:
                        idle_jobs_counter.append(1)
                        running_jobs_counter.append(0)
                    elif job_status == 2:
                        running_jobs_counter.append(1)
                        idle_jobs_counter.append(0)
                    else:
                        print("XXX anomylous job status of {0}, investigate more".format(job_status))

    """
    print(batch_ids)
    print(total_jobs_submitted)
    print(total_jobs_running)
    print(idle_jobs_counter)
    print(running_jobs_counter)
    print(jobs_start_dates)
    """

    condor_info = [batch_ids, total_jobs_submitted, total_jobs_running,
                    idle_jobs_counter, running_jobs_counter, jobs_start_dates]

    return condor_info


def get_htcondor_q_simulated():

    #This is just for testing purposes when not on an osg node

    batch_ids = [2131234, 2131237, 2131238, 2131239, 2131240, 2103366]
    total_jobs_submitted = [1000, 1000, 1000, 621, 1000, 1]
    total_jobs_running = [9, 4, 436, 604, 992, 1]
    idle_jobs_counter = [4, 4, 436, 604, 985, 1]
    running_jobs_counter = [5, 0, 0, 0, 7, 0]
    jobs_start_dates = [1590774145, 1590779217, 1590779518, 1590779702, 1590838003, 1589819944]

    #might make this into a dictionary
    condor_info = [batch_ids, total_jobs_submitted, total_jobs_running,
                    idle_jobs_counter, running_jobs_counter, jobs_start_dates]

    return condor_info

def check_condor_info(condor_info):

    total_jobs_running = condor_info[2]
    idle_jobs = condor_info[3]
    running_jobs = condor_info[4]

    #error post processing
    for index,total_jobs in enumerate(total_jobs_running):
        unaccounted_for_jobs = total_jobs - idle_jobs[index]-running_jobs[index]
        if unaccounted_for_jobs != 0:
            print("error, there is a mismatch between total jobs in condor and idle+running jobs: {0}".format(unaccounted_for_jobs))

    #Should add other tests if can think of some (empty lists, etc)

def get_condor_q(args):
    if args.test:
        data = get_htcondor_q_simulated()
        #print(data)
    else:
        data = get_htcondor_q()

    check_condor_info(data)

    return(data)

if __name__ == '__main__':
    args = get_args.get_args()

    get_condor_q(args)
