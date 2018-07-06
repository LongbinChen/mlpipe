from django.core.management.base import BaseCommand, CommandError
from durian.models import Pipe
from django.contrib.auth.models import User; 
import os
from durian.settings  import * 


from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'create user durian and group durian'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('--job_id', type = int, default=-1)

    def handle(self, *args, **options):
       new_group, created = Group.objects.get_or_create(name='durian')
       User.objects.create_superuser('durian', 'durian@example.com', 'durianadmin')
