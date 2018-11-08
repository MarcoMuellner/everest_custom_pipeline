from os import listdir,mkdir
from os.path import isfile, join
from shutil import copyfile
from typing import List,Dict,Union
from jobs import Job
import numpy as np


root_path = "/var/everest/"
results_path = root_path+"/results/"
jobs_path = root_path+"/jobs/"

jobs = []

def add_job(job : Dict[str,Union[str,np.ndarray,List]]):
    job_obj = Job(**job)
    job_obj.run()

def start():
    job_files = [f for f in listdir(jobs_path) if isfile(join(jobs_path, f))]

    for job in job_files:
        if not job.endswith(".job"):
            continue

        jobList = np.loadtxt(jobs_path+job,dtype=int)
        jobPath = results_path+job.replace(".job","/")

        try:
            mkdir(jobPath) #try to create the folder, if it does exist, doesn't matter
        except FileExistsError:
            pass

        copyfile(jobs_path+job,jobPath+job)

        job_description = {
            "name":job,
            "jobList":jobList,
            "doneJobs":[],
            "jobPath":jobPath
        }

        add_job(job_description)







