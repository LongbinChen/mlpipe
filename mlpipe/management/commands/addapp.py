import os

from django.core.management.base import BaseCommand
from mlpipe.settings import *


class Command(BaseCommand):
    help = 'add an app using its absolute path, by default the app name is the last name at the path'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('app_path', type=str, default=None)
        parser.add_argument('--app_name', type=str, default=None)

    def handle(self, *args, **options):
        if not "app_path" in options:
            return
        app_path = options['app_path']
        app_name = options['app_name']
        if app_name == None:
            app_name = app_path.strip("/").split("/")[-1]
        print("adding app %s to mlpipe as %s, the app path is at %s." % (
                app_path, app_name, resource_directory))
        if os.path.exists(app_path):
            os.symlink(app_path, os.path.join(resource_directory, app_name))
