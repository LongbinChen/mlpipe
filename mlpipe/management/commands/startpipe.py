from django.core.management.base import BaseCommand, CommandError
from mlpipe.models import Pipe
from mlpipe.pipe_utils import PipeParser
import os

class Command(BaseCommand):
    help = 'start running a pipe'

    def add_arguments(self, parser):
        parser.add_argument('pipe_id',  type=str)

    def handle(self, *args, **options):
        pipe_id = options['pipe_id']
        lp = PipeParser()
        succ = lp.load_pipe(pipe_id)
        if succ :
           self.stdout.write(self.style.SUCCESS('Successfully start pipe %s' % (pipe_id)))
        else:
           self.stdout.write(self.style.ERROR('can not start pipe %s' % (pipe_id)))
 
