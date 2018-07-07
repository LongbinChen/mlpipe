import os

from django.core.management.base import BaseCommand, CommandError

from mlpipe.models import Pipe
from mlpipe.settings import *


class Command(BaseCommand):
    help = 'update job status'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('job_id', type = int, default=-1)

    def handle(self, *args, **options):
        if "job_id" in options: 
            j = Job.objects.get(id = options["job_id"])
            j.status = Job.CANCELED
            j.save()
            print("Canceled job %d from status %s." %  (j.id, j.status))
        else:
            print("Please specify a job with a job id")
