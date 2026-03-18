"""
Logfile jsonification for monitoring.
"""
import htcondor2
import classad2

from . import get_args
from . import utils

def get_htcondor_q():
    schedd = htcondor2.Schedd()

    batch_ids = []
    total_jobs_submitted = []
    total_jobs_running = []
    jobs_start_dates = []

    unexpanded_jc = []
    idle_jc = []
    running_jc = []
    removed_jc = []
    completed_jc = []
    held_jc = []
    submission_err_jc = []

    valid_job_stati = [0, 1, 2, 3, 4, 5, 6]
    job_counting_set = [
        unexpanded_jc, idle_jc, running_jc, removed_jc,
        completed_jc, held_jc, submission_err_jc
    ]

    jobs = schedd.query(
        constraint='Owner == "gemc"',
        projection=["ClusterID", "JobStatus", "TotalSubmitProcs", "QDate"],
    )

    for job in jobs:
        batch_id = str(job.get("ClusterID"))
        job_status = int(job["JobStatus"])

        if job_status not in valid_job_stati:
            print(f"HTCondor returned an invalid job status of {job_status}, investigate more")
            continue

        if batch_id not in batch_ids:
            utils.printer(f"found new batch: {batch_id}")
            total_jobs_for_batch = job.get("TotalSubmitProcs", 0)
            start_date_unix = job.get("QDate", 0)

            batch_ids.append(batch_id)
            total_jobs_submitted.append(int(total_jobs_for_batch))
            jobs_start_dates.append(int(start_date_unix))
            total_jobs_running.append(1)

            job_counting_set[job_status].append(1)
            for jc in [0, 1, 2, 3, 4, 5, 6]:
                if jc != job_status:
                    job_counting_set[jc].append(0)
        else:
            idx = batch_ids.index(batch_id)
            total_jobs_running[idx] += 1
            job_counting_set[job_status][idx] += 1

    condor_info = [batch_ids, total_jobs_submitted, total_jobs_running, jobs_start_dates, job_counting_set]
    return condor_info


def get_htcondor_q_simulated():

    #This is just for testing purposes when not on an osg node

    batch_ids = [2131234, 2131237, 2131238, 2131239, 2131240, 2103366]
    total_jobs_submitted = [1000, 1000, 1000, 621, 1000, 1]
    total_jobs_running = [9, 5, 436, 604, 992, 1]


    unexpanded_jc = [0, 0, 0, 0, 0, 0]
    idle_jc = [4, 4, 436, 604, 985, 1]
    running_jc = [5, 0, 0, 0, 7, 0]
    removed_jc = [0, 0, 0, 0, 0, 0]
    completed_jc = [0, 0, 0, 0, 0, 0]
    held_jc = [0, 1, 0, 0, 0, 0]
    submission_err_jc = [0, 0, 0, 0, 0, 0]


    jobs_start_dates = [1590774145, 1590779217, 1590779518, 1590779702, 1590838003, 1589819944]




    job_counting_set = [unexpanded_jc, idle_jc, running_jc, removed_jc, completed_jc, held_jc, submission_err_jc]

    #might make this into a dictionary
    condor_info = [batch_ids, total_jobs_submitted, total_jobs_running, jobs_start_dates, job_counting_set]

    return condor_info

def check_condor_info(condor_info):

    total_jobs_running = condor_info[2]
    jc_set = condor_info[4]

    #error post processing
    for index,total_jobs in enumerate(total_jobs_running):
        unaccounted_for_jobs = total_jobs - jc_set[1][index] - jc_set[2][index] - jc_set[5][index]
        if unaccounted_for_jobs != 0:
            print(("error, there is a mismatch between total jobs in condor and idle+running jobs: {0}".format(unaccounted_for_jobs)))

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
