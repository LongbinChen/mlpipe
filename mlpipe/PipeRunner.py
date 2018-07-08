import json
import os
import shutil
import subprocess
import sys
import time
import types
from time import gmtime, strftime

import yaml
from django.contrib.auth.models import Group, User
from termcolor import colored

import durianutils
from durian.models import Data, Job, JobDependency, Pipe
from durian.settings import *
from JobRunner import JobRunner


class PipeRunner:
    debug = True

    def info(self, msg):
        if (self.debug):
            msg_str = "[Run Pipe] %s" % (msg)
            print(msg_str)

    def _is_job_completed(self, job):
        if job.status == Job.COMPLETED:
            return True
        if job.latched_to != None and job.latched_to != "":
            latched_to_job_id = int(job.latched_to)
            lj = Job.objects.get(id=latched_to_job_id)
            self.info("Job %d is latched to %s with status %s " % (job.id, job.latched_to, lj.status))
            if lj.status == Job.COMPLETED:
                return True
        return False

    def _run_pipe(self, pipe_id, dry_run=False):
        all_jobs = Job.objects.filter(pipe=pipe_id)
        cnt = 0
        job_names = {}
        job_done = {}
        for j in all_jobs:
            cnt += 1
            job_names[j.job_name] = j
            job_done[j.job_name] = False
            # print("job #%d: %s " %(j.id,  j.job_name))
        job_dep = JobDependency.objects.filter(job_name_tgt__in=job_names)
        done_cnt = 0
        while done_cnt < cnt:
            for j in all_jobs:
                if job_done[j.job_name]:
                    continue
                can_run = True
                for jd in job_dep:
                    if jd.job_name_tgt == j.job_name and job_done[jd.job_name_src] == False:
                        can_run = False
                if can_run:
                    jr = JobRunner(j)
                    if (dry_run):
                        if not self._is_job_completed(j):
                            print("job %d %s" % (j.id, j.job_name))
                        else:
                            print("job %d %s [%s]" % (j.id, j.job_name, colored('Completed', 'green')))
                    else:
                        if not self._is_job_completed(j):
                            jr.run()
                    done_cnt += 1
                    job_done[j.job_name] = True

    def __init__(self, pipe_id, dry_run_only=False):
        self._pipe_id = pipe_id
        self._dry_run_only = dry_run_only

    def run(self):
        print("We will run the pipe in the following orders")
        self._run_pipe(self._pipe_id, True)
        if not self._dry_run_only:
            self._run_pipe(self._pipe_id, False)
