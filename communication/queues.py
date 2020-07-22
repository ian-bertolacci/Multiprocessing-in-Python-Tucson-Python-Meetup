#!/usr/bin/env python3
import random, time, operator, os
import multiprocessing as mp
from itertools import chain, repeat
from pprint import pprint
from numpy import inf, pi, cos
from functools import reduce

stdout_lock = mp.Lock()
def parprint( *args, **kwargs ):
  pid = os.getpid()
  with stdout_lock:
    print( f"({pid}):", *args, **kwargs )

def make_work( queue, N ):
  for work in range(N):
    queue.put( work )
  queue.put( "nomorework")

def do_work( queue ):
  while True:
    work = queue.get()
    if isinstance(work,str) and work == "nomorework":
      break
    else:
      print( f"got {work}")


items = 100
work_queue = mp.Queue()

processes = [
  mp.Process( target=make_work, args=(work_queue, items) ),
  mp.Process( target=do_work, args=(work_queue, ) )
]

for process in processes: process.start()
for process in processes: process.join()
