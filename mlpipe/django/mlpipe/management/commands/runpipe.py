import os

from django.core.management.base import BaseCommand, CommandError

from durian.job_utils import JobRunner
from durian.models import Pipe
from durian.pipe_utils import PipeParser, PipeRunner


class Command(BaseCommand):
    help = 'run all jobs in a pipe'
    def is_number(self, s):
      try:
        int(s)
        return int(s)
      except ValueError:
        return None
 

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pipe_id', type = str, default="")
        parser.add_argument('--dry_run', action = 'store_true',  default=False)

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False) 
        
        if "pipe_id" in options and self.is_number(options["pipe_id"]):
           pr = PipeRunner(options["pipe_id"], dry_run)
           pr.run()
        else:
           pipe_id = options['pipe_id']
           lp = PipeParser()
           succ = lp.load_pipe(pipe_id)
           if succ :
              self.stdout.write(self.style.SUCCESS('Successfully start pipe %s' % (pipe_id)))
              pr = PipeRunner(succ, dry_run)
              pr.run() 
           else:
              self.stdout.write(self.style.ERROR('can not start pipe %s' % (pipe_id))) 
