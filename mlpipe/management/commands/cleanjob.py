from django.core.management.base import BaseCommand, CommandError
from mlpipe.models import Pipe
import os
from mlpipe.settings  import * 

class Command(BaseCommand):
    help = "make all job which is in 'created' status to be canceled"

    #def add_arguments(self, parser):
        #parser.add_argument('job_id', type = int, default=-1)

    def handle(self, *args, **options):
        all = Job.objects.filter(status = Job.CREATED)
        cnt = 0
        for j in all:
           cnt += 1
           j.status = Job.CANCELED
           j.save()
        print((" %d jobs are canceled " % cnt))
