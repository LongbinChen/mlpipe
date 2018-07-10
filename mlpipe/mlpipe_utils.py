import errno
import hashlib
import json
import os
import subprocess
import sys
import time
import types
import uuid
from time import gmtime, strftime

import yaml
from django.contrib.auth.models import Group, User
from mlpipe.models import Data, Job, JobDependency, Pipe
from mlpipe.settings import *

SQL_GET_NEXT_EXCUTABLE_JOB = ''' 
    SELECT * FROM mlpipe_job j 
    WHERE j.status = 'created' 
        AND j.latched_to = "" 
        AND j.job_name not in 
        ( 
            SELECT job_name_tgt 
            FROM mlpipe_jobdependency 
            WHERE status = "created" 
            ) 
    '''


def get_next_excutable_job():
    executable_jobs = Job.objects.raw(SQL_GET_NEXT_EXCUTABLE_JOB)
    count = 0
    first_job = None
    for j in executable_jobs:
        first_job = j
        count += 1
    if (first_job):
        print("%d job can be executed now while job %d is picked to be run " % (
            count, first_job.id))
    return first_job


def get_full_data_name(pipe_name, data_name):
    return pipe_name + "." + data_name


def get_full_job_name(pipe_name, job_name):
    return pipe_name + ">" + job_name


def create_uuid(self):
    return uuid.uuid4()


def get_config_by_path(file_path):
    full_path = get_full_path(file_path)
    if not file_path.endswith(".yaml"):
        full_path += ".yaml"
    with open(full_path, 'r') as f:
        try:
            config_data = yaml.load(f)
            print "init config data is"
            print config_data
            for inc in config_data.get("includes", []):
                inc_path = os.path.join(resource_directory, inc)
                inc_data = yaml.load(open(inc_path))
                print "file ", inc
                print inc_data
                config_data['jobs'].update(inc_data.get('jobs', {}))
            print "final config data is"
            print config_data
        except yaml.YAMLError as exc:
            print(exc)
            return None
    return config_data


def get_full_path(file_path):
    return os.path.join(resource_directory, file_path)


def get_md5(input_str):
    m = hashlib.md5()
    m.update(input_str)
    return m.hexdigest()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_main_file_md5(file_path):
    md5_py = ""
    main_file_name = get_full_path(file_path)
    if not main_file_name.endswith(".py"):
        main_file_name += ".py"
    if os.path.exists(main_file_name):
        md5_py = md5(main_file_name)
    else:
        print(("[Warning] can not find file %s " % (main_file_name)))

    md5_yaml = ""
    yaml_file_name = get_full_path(file_path)
    if not yaml_file_name.endswith(".yaml"):
        yaml_file_name += ".yaml"
    if os.path.exists(yaml_file_name):
        md5_yaml = md5(yaml_file_name)
    else:
        print(("[Warning] can not find file %s " % (yaml_file_name)))

    return md5_py + "." + md5_yaml


def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e


def hardlink_force(target, link_name):
    try:
        os.link(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.link(target, link_name)
        else:
            raise e


def get_apps():
    return [o for o in os.listdir(resource_directory)
            if os.path.isdir(os.path.join(resource_directory, o))]


def get_modules():
    module_list = []
    for root, dirs, files in os.walk(resource_directory, followlinks=True):
        path = root.split(os.sep)
        if (len(path) < 2):
            continue
        if path[-1] == "module":
            for file in files:
                if file.endswith(".yaml"):
                    py_file = file[:-5] + ".py"
                    if os.path.exists(os.path.join(root, py_file)):
                        module_list.append(os.path.join(path[-2], path[-1], file))
    return module_list
