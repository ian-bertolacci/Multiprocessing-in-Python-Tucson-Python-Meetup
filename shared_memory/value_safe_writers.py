#!/usr/bin/env python3
import time
import multiprocessing as mp

def safe_writer( counter, trigger ):
  # we need this to slow down the process to see if the race condition is still happening
  trigger.wait()
  # Acquire lock.
  # Value.get_lock simply returns the lock object.
  # The with statement is acquiring exclusive access to the lock.
  with counter.get_lock():
    counter.value += 1


num_processes = 6
counter = mp.Value('i', 0 )
trigger = mp.Event()

processes = [
  mp.Process( target=safe_writer, args=(counter, trigger) )
  for _ in range(num_processes)
]

for process in processes:
  process.start()

trigger.set()

for process in processes:
  process.join()

print( counter.value )
