import os

from django.core.management.base import BaseCommand, CommandError

from durian.backend import *
from durian.models import Pipe
from durian.settings import *


class Command(BaseCommand):
    help = 'display the module definition info'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('module_id', type = int, default=-1)

    def handle(self, *args, **options):
        if "module_id" in options and options["module_id"] != -1:
           modules = get_modules()
           m = modules[options["module_id"]]
           m_yaml_file = os.path.join(resource_directory, m)
           print "file at: %s " % m_yaml_file
           print "file  content \n-----------------"
           os.system("cat %s " % m_yaml_file)
           print "-----------------\n end of yaml file"
