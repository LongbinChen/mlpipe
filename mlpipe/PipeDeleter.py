import os

from durian.models import Data, Job, JobDependency, Pipe
from durian.settings import *


class PipeDeleter:

    def _delete_pipe(self, pipe_id, dry_run = True):
        try:
          pipe = Pipe.objects.get(id = pipe_id)
        except Pipe.DoesNotExist:
          print "pipe with %d  doesnt exist" % pipe_id
          return 
        pipe_name = pipe.pipe_name
        jobs = Job.objects.filter(pipe = pipe_id)
        job_names = [j.job_name for j in jobs]

        # check running jobs
        has_running = False
        for j in jobs:
            if j.status == Job.RUNNING:
                has_running = True
                print('Please cancel or complete the running job {} before deleting this pipe.'.format(j.id))
            same_jobs = Job.objects.filter(job_hash = j.job_hash)
            for sj in same_jobs:
                if sj.status == Job.RUNNING:
                    has_running = True
                    print('Please cancel or complete the running job {}, which is the same as job {}, before deleting this pipe.'.format(sj.id, j.id))
        if has_running:
            return

        # delete jobs
        for j in jobs:
            job_id = j.id
            print('job db entry {}'.format(job_id))
            if not dry_run:
                j.delete()
            job_working_directory = os.path.join(working_directory, 'job', str(job_id))
            print('    and its corresponding working directory {}'.format(job_working_directory))
            if not dry_run:
                cmd = 'rm -r {}'.format(job_working_directory)
                os.system(cmd)
            print('    and other jobs are no longer latched to with it.')
            if not dry_run:
                Job.objects.filter(latched_to = job_id).update(latched_to = "")

        # delete job dependencies
        job_deps = JobDependency.objects.filter(job_name_tgt__in = job_names)
        for jd in job_deps:
            print('job dependency db entry from {} to {}'.format(jd.job_name_src, jd.job_name_tgt))
            if not dry_run:
                jd.delete()

#        # do not delete data since it could be shared by other jobs
#        data = Data.objects.filter(data_name__startswith = pipe_name)
#        for d in data:
#            print('data db entry {}'.format(data_name))
#            storage_file = os.path.join(storage_path, d.data_hash)
#            print('    and its corresponding storage file {}'.format(storage_file))

        # delete pipe
        print('pipe db entry {}.'.format(pipe_id))
        if not dry_run:
            pipe.delete()

    def __init__(self, pipe_id, dry_run_only = False):
        self._pipe_id = pipe_id
        self._dry_run_only = dry_run_only

    def run(self):
        print("We will delete the following items")
        self._delete_pipe(self._pipe_id, self._dry_run_only)
