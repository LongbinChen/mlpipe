import os

from django.core.management.base import BaseCommand, CommandError

from durian.durian_utils import durianutils
from durian.JobRunner import JobRunner

class Command(BaseCommand):
    help = 'run a job'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('job_id', type = int, default=-1)
        parser.add_argument('--clean_up', dest='clean_up', action='store_true',  default=False)
        parser.add_argument('--force', dest='force', action='store_true',  default=False)

    def handle(self, *args, **options):
        if "job_id" in options and options["job_id"] != -1:
            j = Job.objects.get(id = options["job_id"])
            if j.status == Job.RUNNING:
               print "Job %d (%s) is still running with process id %s." % ( j.id, j.job_name, j.process_id)
               print "Please make sure the other process is killed before a new run. You can use --force to run the job if you are sure the job is not running. " 
               if not options.get("force", False):
                 return 
            jr = JobRunner(j)
            if (options["clean_up"]): 
               jr.remove_working_dir()
            jr.run()
