#!/usr/bin/env python3
import time, random
import multiprocessing as mp

def printer( id, print_lock, array ):
  while True:
    time.sleep( random.uniform(0.0, 5.0) )
    # Aquire the print lock so printing can occur uninterrupted
    with print_lock:
      print( "=" * 20 )
      for v in array:
        print( f"({id}) {v}" )
      print( "=" * 20 )


def worker( id, array ):
  while True:
    array[id] += 1


printers = 4
workers = 4
array = mp.Array( 'i', workers )
print_lock = mp.Lock()

processes = [
  mp.Process( target=printer, args=(id, print_lock, array ) )
  for id in range(printers)
] + [
  mp.Process( target=worker, args=(id, array) )
  for id in range(workers)
]

for process in processes:
  process.start()

for process in processes:
  process.join()
