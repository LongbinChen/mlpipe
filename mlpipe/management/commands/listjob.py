from django.core.management.base import BaseCommand, CommandError
from mlpipe.models import Pipe, Job
from mlpipe.JobRunner import JobRunner
import os
import datetime
from django.utils import timezone
from termcolor import colored

class Command(BaseCommand):
    help = 'run a job'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--job_type', type = str, default=None)
        parser.add_argument('--count', type = int, default = 25)
        parser.add_argument('--full', action="store_true", default=False)

    def get_status_text(self, status):
        if status == Job.RUNNING:
          return colored(status, 'green')
        return status

    def handle(self, *args, **options):
      
        limit = options.get("count", 25)
        if "job_type" in options  and options["job_type"] == None:
           all_job = Job.objects.order_by("-id")[:limit]
        else:
           all_job = Job.objects.filter(status = options["job_type"]).order_by("-created_at")[:limit]
        template = '{:<5}  {:<6}  {:<25}  {:<5}  {:<10}  {:<10}  {:<10}  {:<7}  {:<20}  {:<40}'
        print(template.format("jobId", "pipeId", "jobName", "proId", "status", "start time", "duration", "latched", "Create at", "PipeName"))
        for j in all_job:
           start_at_str = j.start_at.strftime('%H:%M:%S') if j.start_at != None else "None    "
           end_at_str = j.end_at.strftime('%H:%M:%S') if j.end_at != None else "None     "
           dur_str = ""
           j_name = j.job_name.split("/")[-1]
           j_jname = j_name.split(">")[-1]
           j_pname = j_name.split(">")[0]
           if j.start_at != None and j.end_at == None and j.status == Job.RUNNING:
             s = (timezone.now() - j.start_at).total_seconds()
             hours, remainder = divmod(s, 3600)
             minutes, seconds = divmod(remainder, 60)
             dur_str = '%dhr %dm' % (hours, minutes)
           elif j.start_at != None and j.end_at != None:
             s = (j.end_at - j.start_at).total_seconds()
             hours, remainder = divmod(s, 3600)
             minutes, seconds = divmod(remainder, 60)
             dur_str = '%dhr %dm' % (hours, minutes)
           
           print(template.format(j.id, j.pipe.id, j_jname[:25], str(j.process_id or ""), self.get_status_text(j.status), start_at_str, dur_str, j.latched_to or "", j.created_at.strftime("%m-%d-%Y %a %H:%M"), j_pname[-40:]))
