# This file contains all local settings
# mlpipe directory containing cached data, working and storage directories
import os

#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MLPIPE_ROOT="/Users/cf/mlpipe"

resource_directory = os.path.join(MLPIPE_ROOT, "apps")
working_directory = os.path.join(MLPIPE_ROOT, "working")
cached_data_directory = os.path.join(MLPIPE_ROOT, "cached_data")
storage_directory = os.path.join(MLPIPE_ROOT, "storage")

local_storage = True
s3_storage = False
run_local = True

MLPIPE_MACHINE_NAME = "slave1"

#the following is an example of config mysql as the backend database

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         #'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'alpha',                      # Or path to database file if using sqlite3.
#         'TEST_NAME': 'test1',                      # for testing
#         'USER': 'mlusers',                      # Not used with sqlite3.
#         'PASSWORD': 'mlusers',                  # Not used with sqlite3.
#         'HOST': '172.31.41.137',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }