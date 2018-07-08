# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group

class Pipe(models.Model):
    
    CREATED = 'created'
    DONE = 'done'
    PIPE_STATUS = ((CREATED, CREATED), (DONE, DONE))

    #fields
    owner = models.ForeignKey(User, to_field="username", null=True)
    group = models.ForeignKey(Group, to_field="name", null=True)
    pipe_name = models.CharField(max_length=255)
    pipe_def = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices = PIPE_STATUS)
    created_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(auto_now=True)
    end_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    desc = models.CharField(max_length=2000)

class Job(models.Model):
    '''
        an atom operation , like executing a script
    '''
    COMPLETED = "completed"
    CREATED = "created"
    LATCHED = "latched"
    CANCELED = "canceled"
    FAILED = "Failed"
    RUNNING = "Running"
    JOB_STATUS = ((COMPLETED, COMPLETED), (CREATED, CREATED), 
                  (LATCHED, LATCHED), (CANCELED, CANCELED),
                  (FAILED, FAILED), (RUNNING, RUNNING))

    pipe = models.ForeignKey(Pipe)
    job_name = models.CharField(max_length=255, null=True)
    module_id = models.CharField(max_length=255)
    module_idx = models.CharField(max_length=255)
    job_conf = models.TextField(blank=True, null=True)
    #json data to represent the input of the file
    #[{moduleid, terminal_id}, {moduleid, terminal_id}, ...]
    # result file is saved as pipe_id +  module_id + terminal_id
    job_input = models.CharField(max_length=2000)
    job_output = models.CharField(max_length=2000)
    status = models.CharField(max_length=255, choices = JOB_STATUS )
    created_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)
    job_hash = models.CharField(max_length=255)
    latched_to = models.CharField(max_length=20)
    process_id = models.CharField(max_length = 255, null = True)
    machine_name = models.CharField(max_length = 255, null = True)


class RunningLog(models.Model):
    cmd = models.CharField(max_length = 255, null = True)
    process_id = models.CharField(max_length = 255, null = True)
    job_id = models.CharField(max_length = 255, null = True)
    pipe_id = models.CharField(max_length = 255, null = True)
    status = models.CharField(max_length = 255, null = True)
    start_at = models.DateTimeField(auto_now=True)
    end_at = models.DateTimeField(auto_now=True)
    
# descripe the dependency between jobs
class JobDependency(models.Model):
    CREATED = "created"
    REMOVED = "removed"
    JD_STATUS = ((CREATED, CREATED), (REMOVED, REMOVED))

    job_name_src = models.CharField(max_length=255)
    job_name_tgt = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices = JD_STATUS)

class Data(models.Model):
    data_name = models.CharField(max_length=255)
    data_hash = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255)
    data_size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255)

