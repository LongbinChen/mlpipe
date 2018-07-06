import argparse
import os
import tarfile
import uuid
import hashlib


#  if local_file is a directory, create a zip tar file first


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def calculate_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def run(args):
  if os.path.isdir(args.local_file):
     if args.zip_dir != None:
        if not os.path.exists(args.zip_dir):
           os.mkdir (args.zip_dir)
        _tmp_file = os.path.join(args.zip_dir, str(uuid.uuid()) + ".tar.gz")
     else:
        _tmp_file = str(uuid.uuid4()) + ".tar.gz"
     print "making tar.gz file %s " % _tmp_file
     make_tarfile(_tmp_file, args.local_file)
     data_md5 = calculate_md5(_tmp_file)
     _tmp_file_md5 = _tmp_file + ".md5"
     
     with open(_tmp_file_md5, "w") as fmd5:
        fmd5.write(data_md5)
  
     print "uplaoding % s to %s " % (_tmp_file, args.s3_path)
     os.system("s3cmd put %s %s" % (_tmp_file, args.s3_path))
     if args.clean: 
       os.system("rm %s" % (_tmp_file))
     return True
  if os.path.isfile(args.local_file):
     os.system("s3cmd put -F %s %s" % (args.local_file, args.s3_path))
     return True
  return False

def create_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--zip_dir', dest='zip_dir',  default = None, 
      help='parameters, local temp directory to hold the temp zip file, used when large .tar.gz file is created ')
  parser.add_argument('--clean', dest='clean',  default = True, action="store_false", 
                      help='parameters, remove temp file')
  parser.add_argument('local_file', help='input, the config file')
  parser.add_argument('s3_path',  default=None, type=str, help='parameters, the s3 location to upload to')
  return parser

if __name__ == '__main__':
  parser = create_parser()
  args = parser.parse_args()
  run(args)

