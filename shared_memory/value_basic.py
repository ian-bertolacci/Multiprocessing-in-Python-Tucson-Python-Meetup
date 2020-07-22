#!/usr/bin/env python3
import multiprocessing as mp

def reader( obj ):
  while True:
    print( f"{obj.value}" )
    time.sleep(.2)

def unsafe_writer( obj ):
  while True:
    obj.value += 1


shared_value = mp.Value('i', 0 )

processes = [
  mp.Process( target=reader,        args=(shared_value,) ),
  mp.Process( target=unsafe_writer, args=(shared_value,) )
]

for process in processes:
  process.start()
for process in processes:
  process.join()
