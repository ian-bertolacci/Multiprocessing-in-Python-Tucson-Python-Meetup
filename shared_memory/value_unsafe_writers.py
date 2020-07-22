#!/usr/bin/env python3
import time
import multiprocessing as mp

def unsafe_writer( counter, barrier ):
  # we need this to slow down the process so the race condition is apparent
  trigger.wait()
  # Unprotected, non-atomic increment
  counter.value += 1


num_processes = 6
counter = mp.Value('i', 0 )
trigger = mp.Event()

processes = [
  mp.Process( target=unsafe_writer, args=(counter, trigger) )
  for _ in range(num_processes)
]

for process in processes:
  process.start()

trigger.set()

for process in processes:
  process.join()

print( counter.value )
