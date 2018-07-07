import os

from django.core.management.base import BaseCommand
from mlpipe.settings import *


class Command(BaseCommand):
    help = 'list all configs'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print "============================="
        print "data_directory: %s " % mlpipe_directory
        print "    job_directory: %s " % working_directory
        print "    cache_directory: %s " % cached_data_directory
        print "    storage_directory: %s " % storage_path
        print "app_directory: %s" % resource_directory
        print "You can config the settings by adding a file at :  %s" % SETTING_FILE_DIR.replace('settings.py', 'extra_settings.py')
        print "You can also config the settings by update the file at:  %s" % SETTING_FILE_DIR
        

