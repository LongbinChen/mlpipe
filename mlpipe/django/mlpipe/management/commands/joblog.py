import os

from django.core.management.base import BaseCommand, CommandError

from durian.models import Pipe
from durian.settings import *


class Command(BaseCommand):
    help = 'display the job running log'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--job_id', type = int, default=-1)

    def handle(self, *args, **options):
        if "job_id" in options and options["job_id"] != -1:
            working_dir = os.path.join(working_directory, "job", str(options["job_id"]))
            logfile = os.path.join(working_dir, "__log__.txt")
            print("log file is at : %s " % logfile) 
            os.system("cat %s" % logfile)
        else:
            print("Please specify a job with a job id")
