import argparse
import gzip
import os
import yaml
import types


# an iterator to iterate all parameters


def find_min(config):
  print(config)
  search_file = config["parameters"]["search_result_file"]
  if not search_file in config["input"]: 
     print(config["input"])
     print("%s is not part of input %s " % ( search_file, ",".join(config["input"])))
     return False
  #find min value
  if not isinstance(config["input"][search_file], types.ListType):
     print("Expecting the input '%s' to be a list. " % (search_file))
     return False
  min_value = None
  values = [float(open(f, "r").readline()) for f in config["input"][search_file]]
  min_idx = values.index(min(values))
  for o in config["output"]:
    src_file = config["input"][o][min_idx]
    os.system('cp %s %s ' % (src_file, o))
  return True

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument( '--config', default="_default_config", type=str, help='the config file')

  params  = parser.parse_args()
  with open(params.config, "r") as cf:
    config = yaml.load(cf) 
    find_min(config)

