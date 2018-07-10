from django.core.management.base import BaseCommand, CommandError
from mlpipe.models import Pipe
from mlpipe.job_utils import JobRunner
import os
from mlpipe.settings  import *

class Command(BaseCommand):
    help = 'list all available pipe'

    def add_arguments(self, parser):
        # Positional arguments
        #parser.add_argument('--pipe_type', type = str, default=None)
        parser.add_argument('--directory', type=str, default=None)
        pass

    def handle(self, directory=None, *args, **options):
        for root, dirs, files in os.walk(resource_directory, followlinks=True):
          path = root.split(os.sep)
          if (len(path) < 2): continue
          if path[-1] == "pipe" and (directory is None or path[-2] == directory):
             for file in files:
                print(os.path.join(path[-2], path[-1], file))
   
