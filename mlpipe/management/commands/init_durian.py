from django.core.management.base import BaseCommand, CommandError
from mlpipe.models import Pipe
from django.contrib.auth.models import User; 
import os
from mlpipe.settings  import * 


from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'create user mlpipe and group mlpipe'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--job_id', type = int, default=-1)

    def handle(self, *args, **options):
       new_group, created = Group.objects.get_or_create(name='mlpipe')
       User.objects.create_superuser('mlpipe', 'mlpipe@example.com', 'mlpipeadmin')
