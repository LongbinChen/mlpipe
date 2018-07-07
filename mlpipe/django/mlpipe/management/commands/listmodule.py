import os

from django.core.management.base import BaseCommand, CommandError
from mlpipe.settings import *
import mlpipe.mlpipe_utils as mlpipeutils


class Command(BaseCommand):
    help = 'list all available module'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        app_dict = mlpipeutils.get_apps()
        module_list = mlpipeutils.get_modules()
        print "%d app(s) found : %s " % (len(app_dict) , ",".join(app_dict))
        print "%d modules  found :" % (len(module_list) )
        for i, k in  enumerate(module_list):
            print  "%d : %s " %(i, k)
