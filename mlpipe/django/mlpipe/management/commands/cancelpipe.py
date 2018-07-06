from django.core.management.base import BaseCommand, CommandError
from durian.models import Pipe
import os

class Command(BaseCommand):
    help = 'run all jobs in a pipe'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pipe_id', type = int, default=-1)

    def cancel_pipe(self, pipe_id, dry_run = False):
            all_jobs = Job.objects.filter(pipe = pipe_id)
            for j in all_jobs:
               j.status = Job.CANCELED
               j.save()

    def handle(self, *args, **options):
        if "pipe_id" in options and options["pipe_id"] != -1:
           self.cancel_pipe(options["pipe_id"])
        else:
            print("no job can be found for pipe %d " % options["pipe_id"])
