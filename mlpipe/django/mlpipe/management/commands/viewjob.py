import os

from django.core.management.base import BaseCommand, CommandError

from mlpipe.models import Pipe
from mlpipe.settings import *


class Command(BaseCommand):
    help = 'display the job running result'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('job_id', type = int, default=-1)

    def handle(self, *args, **options):
        if "job_id" in options and options["job_id"] != -1:
            working_dir = os.path.join(working_directory, "job", str(options["job_id"]))
            os.system("ls -l %s " % working_dir)
            print("working directory at %s" % working_dir)
        else:
            print("Please specify a job with a job id")
