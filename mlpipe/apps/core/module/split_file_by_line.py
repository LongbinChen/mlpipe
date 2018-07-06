import argparse
import gzip
import numpy
import os
import yaml
import types
import random

def run(args):
  random.seed(args.random_seed)
  with open(args.input_file, "rb") as f:
    with open(args.output_1, "w") as f1: 
      with open(args.output_2, "w") as f2: 
        for ln in f:
          if random.random() > args.ratio:
              f2.write(ln)
          else:
              f1.write(ln)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument( '--ratio', default=0.8, type=float, help='the ratio of the first file')
  parser.add_argument( '--random_seed', default=100, type=int, help='the randome_seed')
  parser.add_argument( 'input_file', type=str, help=' the input file')
  parser.add_argument( 'output_1', type=str, help=' the first file')
  parser.add_argument( 'output_2', type=str, help=' the 2nd file')

  args = parser.parse_args()
  run(args)
   

