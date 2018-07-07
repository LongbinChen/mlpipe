# This file contains all local settings

# mlpipe directory containing cached data, working and storage directories

mlpipe_directory = '/data/mlpipe'
resource_directory =  BASE_DIR + "/../" + "resource/"
working_directory = os.path.join(mlpipe_directory, "working")
cached_data_directory = os.path.join(mlpipe_directory, "cached_data")

local_storage = True
s3_storage = False
storage_path = os.path.join(mlpipe_directory, "storage")

run_local = True
DJANGO_BOOTSTRAP_UI_THEME = 'bootswatch-cosmo'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        #'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'alpha',                      # Or path to database file if using sqlite3.
        'TEST_NAME': 'test1',                      # for testing
        'USER': 'mlusers',                      # Not used with sqlite3.
        'PASSWORD': 'mlusers',                  # Not used with sqlite3.
        'HOST': '172.31.41.137',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
mlpipe_MACHINE_NAME = "slave3"

resource_directory = '/home/ubuntu/mlpipe/resource'
