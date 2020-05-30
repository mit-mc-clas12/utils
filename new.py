"""
Logfile jsonification for monitoring.
"""
import htcondor
import classad


def get_htcondor_q():
    schedd = htcondor.Schedd()

    batch_ids = []
    total_jobs_auto_counter = []
    total_jobs_manual_counter = []
    idle_jobs_counter = []
    running_jobs_counter = []
    jobs_start_dates = []

    for job in schedd.xquery(): #look through all jobs in condor
            if job.get("owner") == "gemc": #look only at jobs submitted by gemcRunning
                batch_id = str(job.get("ClusterID")) #get cluster id (batch ID) and convert from Long to string
                job_status = job["JobStatus"] #gets if the job is running (2) or idle (1)

                if batch_id in batch_ids:
                    total_jobs_manual_counter[batch_ids.index(batch_id)] += 1
                    if job_status == 1:
                        idle_jobs_counter[batch_ids.index(batch_id)] += 1
                    if job_status == 2:
                        running_jobs_counter[batch_ids.index(batch_id)] += 1
                    else:
                        print("anomylous job status of {0}, investigate more".format(job_status))
                else:
                    print("found new batch: {0}".format(batch_id))
                    total_jobs_for_batch = job.get("TotalSubmitProcs") #Get total number of jobs in batch submitted
                    start_date_unix = job.get("QDate")  #Get submitted date

                    batch_ids.append(batch_id)
                    total_jobs_auto_counter.append(total_jobs_for_batch)
                    jobs_start_dates.append(start_date_unix)

                    total_jobs_manual_counter.append(1) #initialzie entry for manual job counting
                    if job_status ==1:
                        idle_jobs_counter.append(1)
                    if job_status == 2:
                        running_jobs_counter.append(1)
                    else:
                        print("anomylous job status of {0}, investigate more".format(job_status))


    print(batch_ids)
    print(total_jobs_auto_counter)
    print(total_jobs_manual_counter)
    print(idle_jobs_counter)
    print(running_jobs_counter)
    print(jobs_start_dates)

    return batch_ids, num_jobs

get_htcondor_q()
