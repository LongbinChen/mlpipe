from django.core.management.base import BaseCommand, CommandError
from mlpipe.pipe_utils import PipeDeleter
import re

class Command(BaseCommand):
    help = 'delete all jobs in a pipe, or a range of pipes'
    
    #pipe_id format 
    # single pipe id, e.g. 4
    # pipe_id range, e.g., 4-10 
    # list of pipe_id,  e.g, 3,4,5
    def parse_pipe_id(self, pipe_id):
      if re.match("^[\d]+$", pipe_id): 
         return [int(pipe_id)]
      if re.match("^[\d]+-[\d]+$", pipe_id):
         st, end = pipe_id.split("-")
         return range(int(st), int(end) + 1)
      if re.match("^\d+(,\d+)+$", pipe_id):
         return [int(t) for t in pipe_id.split(",")]
      print "can not recognize %s ." % (pipe_id)
      return []

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pipe_id', type=str, default='')
        parser.add_argument('--dry_run', action = 'store_true',  default=False)

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        if "pipe_id" in options and options["pipe_id"] != '':
           r = self.parse_pipe_id(options["pipe_id"])
           print "will delete pipe ", r
           for pid in r:
               pd = PipeDeleter(pid, dry_run)
               pd.run()
        else:
            print("no job can be found for pipe %d " % options["pipe_id"])
