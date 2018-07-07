# This file contains all local settings

# mlpipe directory containing cached data, working and storage directories
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mlpipe_directory = '/Users/cf/mlpipe'
resource_directory =  '/Users/cf/mlpipe/apps'
working_directory = os.path.join(mlpipe_directory, "working")
cached_data_directory = os.path.join(mlpipe_directory, "cached_data")
storage_path = os.path.join(mlpipe_directory, "storage")

run_local = True
DJANGO_BOOTSTRAP_UI_THEME = 'bootswatch-cosmo'

mlpipe_MACHINE_NAME = "slave1"

