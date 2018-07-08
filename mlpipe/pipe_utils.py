import json
import os
import sys
import time
import types
from time import gmtime, strftime

import yaml
from django.contrib.auth.models import Group, User
from termcolor import colored

import mlpipe.mlpipe_utils as mlpipeutils
from mlpipe.job_utils import JobRunner, mlpipeBuildinJob
from mlpipe.models import Data, Job, JobDependency, Pipe
#from mlpipe.settings import *


class PipeDeleter(object):
    '''
        class to delete a pipe
    '''
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
#            storage_file = os.path.join(storage_directory, d.data_hash)
#            print('    and its corresponding storage file {}'.format(storage_file))

        # delete pipe
        print('pipe db entry {}.'.format(pipe_id))
        if not dry_run:
            pipe.delete()

    def __init__(self, pipe_id, dry_run_only = False):
        self._pipe_id = pipe_id
        self._dry_run_only = dry_run_only

    def run(self):
        '''
        delete a pipe from database
        '''
        print("We will delete the following items")
        self._delete_pipe(self._pipe_id, self._dry_run_only)


class PipeRunner(object):
    '''
    The class to run a pipe
    '''
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

class PipeParser:
    '''
        parsing a pipe (a yaml file) into database; 
        create jobs and job dependency
    '''
    # to check if there is anything wrong with the pipe
    job_keys = []  # list of job names
    job_list = {}  # dictionary of job name to Job db object
    data_hash = {}  # mapping data name to its hash value
    is_data_file = {}  # true/false for each data ;
    output_map = {}
    dp_list = []
    pipe_name = ""
    pipe = None
    debug = True

    def info(self, msg, task=""):
        if (self.debug):
            msg_str = "[Parsing Pipe] %s" % (msg)
            print(msg_str)

    def _validate_pipe(self):
        self.job_keys = [k for k in self.pipe['jobs'].keys() if 'module' in self.pipe["jobs"][k]
                         and 'template' not in self.pipe["jobs"][k]]
        # first check if the outputs are unique
        for j in self.job_keys:
            for k, v in self.pipe["jobs"][j]['output'].items():
                if v in self.output_map:
                    self.info("ERROR, duplicate name of outputs for job %s and %s" % (self.output_map[v], j))
                    return False
                self.output_map[v] = j
        return True

    def _update_job_hash(self, job, job_hash):
        job.job_hash = job_hash
        latching_job = Job.objects.filter(latched_to="", job_hash=job_hash, status__in=[Job.CREATED, Job.COMPLETED])
        for lj in latching_job:
            self.info("job %d is latched to with id %d, job_name:%s, status: %s " %
                      (job.id, lj.id, lj.job_name, lj.status))
            job.latched_to = lj.id
            job.status = lj.status
            if (job.status == Job.COMPLETED):
                JobDependency.objects.filter(job_name_src=job.job_name).update(status='removed')
                break
        job.save()

    def _generate_dependency_pairs(self):
        for i in self.job_list:
            for k, v in self.pipe["jobs"][i]['input'].items():
                if '::' in v:
                    continue
                if not isinstance(v, types.ListType):
                    v = [v]
                for va in v:
                    if va in self.output_map:
                        dp = JobDependency(job_name_src=mlpipeutils.get_full_job_name(
                            self.pipe_name, self.output_map[va]),
                            job_name_tgt=mlpipeutils.get_full_job_name(self.pipe_name, i),
                            status=JobDependency.CREATED)
                        dp.save()
                        self.dp_list.append((self.output_map[va], i))
        return True

    def _generate_job_list(self):
        for idx, j in enumerate(self.job_keys):
            full_job_name = mlpipeutils.get_full_job_name(self.pipe_name, j)
            jj = Job(pipe=self.pp, job_name=full_job_name, module_id=self.pipe["jobs"][j]['module'],
                     module_idx=idx, job_conf=json.dumps(self.pipe["jobs"][j]), status=Job.CREATED)
            jj.save()
            self.info("Job %d created, named %s " % (jj.id, full_job_name))
            self.job_list[j] = jj
        return True

    def _generate_data_hash(self):
        job_cnt = len(self.job_keys)
        job_depends_on_it = {}
        job_it_depends = {}
        for j in self.job_keys:
            job_depends_on_it[j] = []
            job_it_depends[j] = []
        for src, tgt in self.dp_list:  # tgt depends on src
            job_depends_on_it[src].append(tgt)
            job_it_depends[tgt].append(src)
        cnt = 0
        done_job = {}
        while cnt < job_cnt:
            # find a job without dependency
            for k, v in job_it_depends.items():
                if (len(v) == 0) and (k not in done_job):
                    # remove depends on k
                    for j1 in job_depends_on_it[k]:
                        # remove k from j1
                        job_it_depends[j1].remove(k)
                    done_job[k] = 1
                    self._get_job_and_data_hash(self.job_list[k])
                    cnt += 1
        return True

    def _load_pipe_in_json(self, pipe):
        self.pipe = pipe
        if not self._validate_pipe():
            self.info("the pipe has errors. ")
            return False

        self.pp = Pipe(pipe_name=self.pipe_name,
                       pipe_def=json.dumps(pipe),
                       status="created")
        self.pp.save()
        self._generate_job_list()
        self._generate_dependency_pairs()
        self._generate_data_hash()
        pipe["datafile"] = self.data_hash
        self.pp.pipe_def = json.dumps(pipe)
        self.pp.save()
        self.info(
            "New Pipe is created  with %d. you can use command 'ml runpipe %d' to start running the pipe" %
            (self.pp.id, self.pp.id))
        return self.pp.id

    # job_hash = md5( module_name + input_parameters)
    # output_data_hash = md5 ( module_name + input_parameters + output_name)
    def _lookup_input_data(self, job_conf, module_conf, input_name):
        input_name_conf = job_conf["input"][input_name]
        concat_name = ""
        is_data_by_config = module_conf["input"].get("datafile", False)
        if not isinstance(input_name_conf, types.ListType):
            input_name_conf = [input_name_conf]
        for inn in input_name_conf:
            if self.is_data_file.get(
                    inn, False) or is_data_by_config:  # check if it is data by config or by smart search
                concat_name += self.data_hash(inn)
            else:
                concat_name += inn
        return concat_name

    def _get_job_and_data_hash(self, job):
        info_list = []
        module_name = job.module_id
        module_conf = mlpipeutils.get_config_by_path(module_name)
        job_conf = json.loads(job.job_conf)
        if module_conf.get("input_from_job_config", None) == True:
            module_conf["input"] = job_conf["input"]
        if module_conf.get("output_from_job_config", None) == True:
            module_conf["output"] = job_conf["output"]

        info_list.append(module_name)
        code_check_sum = mlpipeutils.get_main_file_md5(module_name)
        info_list.append(code_check_sum)
        inputs_sorted = job_conf["input"].keys()
        inputs_sorted.sort()
        for inp in inputs_sorted:
            input_data_name = job_conf["input"][inp]
            if not isinstance(input_data_name, types.ListType):
                input_data_name = [input_data_name]
            for idn in input_data_name:
                if "://" in idn:
                    self.data_hash[idn] = mlpipeutils.get_md5(idn)
                info_list.append(self.data_hash.get(idn, idn))
        param_conf = job_conf.get("parameters", {})
        param_sorted = param_conf.keys()
        param_sorted.sort()
        for p in param_sorted:
            info_list.append(str(param_conf[p]))

        # update job hash at the same time
        job_hash = mlpipeutils.get_md5("\t".join(info_list))
        self._update_job_hash(job, job_hash)

        outputs_sorted = job_conf["output"].keys()
        outputs_sorted.sort()
        for o in outputs_sorted:
            output_data_name = job_conf["output"][o]
            tmp_str = "\t".join(info_list + [o])
            output_full_data_path = mlpipeutils.get_full_data_name(self.pipe_name,  output_data_name)
            dd = Data(data_name=output_full_data_path,
                      data_hash=mlpipeutils.get_md5(tmp_str),
                      tag="",
                      data_type="",
                      data_size=0,
                      description="intermediate data")
            dd.save()
            self.data_hash[output_data_name] = mlpipeutils.get_md5(tmp_str)

    def load_pipe(self, pipe_id):
        '''
          load pipe from a yaml file
          the pipe id format is like  [REPO_NAME]::pipe::[PIPE_NAME]], e.g. mlpipeml::pipe::mnist
        '''
        current_timestamp = int(time.time())
        pipe_origin = mlpipeutils.get_config_by_path(pipe_id)
        if (pipe_origin == None):
            self.info("cant get pipe config from %s " % pipe_id)
            sys.exit(1)
        lb = mlpipeBuildinJob()
        pipe = lb.compile_pipe(pipe_origin)
        if (pipe == None):
            return False
        self.pipe_name = pipe_id + ".%d" % (current_timestamp)
        return self._load_pipe_in_json(pipe)

    def create_pipe(self, pipe):
        '''
            create a pipe by a json obj
        '''
        self.pipe_name = "pipe_%d" % (self.create_uuid())
        return self._load_pipe_in_json(pipe)
