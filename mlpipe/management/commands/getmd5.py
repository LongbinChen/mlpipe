from django.core.management.base import BaseCommand, CommandError
from mlpipe.models import Pipe
import mlpipe.mlpipe_utils as mlpipeutils
from mlpipe.JobRunner import JobRunner
import os

class Command(BaseCommand):
    help = 'get the md5 for a string'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('inputstring')

    def handle(self, *args, **options):
        if "inputstring" in options: 
            print mlpipeutils.get_md5(options["inputstring"])
