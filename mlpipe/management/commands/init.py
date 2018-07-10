from django.core.management.base import BaseCommand, CommandError
from mlpipe.models import Pipe
from django.contrib.auth.models import User; 
import os
from mlpipe.settings  import * 
import mlpipe.apps.core as mlpipe_core 
from django.core.management import call_command
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'create user mlpipe and group mlpipe'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--job_id', type = int, default=-1)

    def _ensure_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(("[init] directory %s created" % directory))
        else:
            print(("[init] directory %s exists" % directory))

    def handle(self, *args, **options):

        if os.environ.get('MLPIPE_HOME') == None:
            print("Please set the environment variable 'MLPIPE_HOME' first.")
            print("such as export MLPIPE_HOME=~/mlpipe  and put it in ~/.bash_profile")
            return 
        MLPIPE_HOME = os.environ.get('MLPIPE_HOME')

        #create directories
        self._ensure_dir(MLPIPE_HOME)
        self._ensure_dir(working_directory)
        self._ensure_dir(cached_data_directory)
        self._ensure_dir(storage_directory)
        self._ensure_dir(resource_directory)
        with open(os.path.join(MLPIPE_HOME, "mlconfig.py"), "w") as fconfig:
            fconfig.write("#please write the config here")



        print("[init] createing database ...")
        call_command('makemigrations', 'mlpipe')
        call_command('migrate','mlpipe')

        #create user and group
        try:
            new_group, created = Group.objects.get_or_create(name='mlpipe')
            User.objects.create_superuser('mlpipe', 'mlpipe@example.com', 'mlpipeadmin')
            print("[init] user, group are created.")
        except:
            print("[init] user, group seems exist")
            

        #create core app
        app_path =  os.path.dirname(mlpipe_core.__file__)
        app_name = 'core'
        target_link = os.path.join(resource_directory, app_name)
        if os.path.exists(app_path):
            if os.path.exists(target_link):
                print("[init] ml core app exists.")
            else:
                os.symlink(app_path, target_link)
                print("[init] ml core app is linked.")
