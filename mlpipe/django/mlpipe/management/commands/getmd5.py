from django.core.management.base import BaseCommand, CommandError
from durian.models import Pipe
import durian.durian_utils as durianutils
from durian.JobRunner import JobRunner
import os

class Command(BaseCommand):
    help = 'get the md5 for a string'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('inputstring')

    def handle(self, *args, **options):
        if "inputstring" in options: 
            print durianutils.get_md5(options["inputstring"])
