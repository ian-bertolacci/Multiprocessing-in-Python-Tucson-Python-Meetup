#!/usr/bin/env python3
import time
import multiprocessing as mp

def safe_writer( id, array, barrier, writer_event ):
  while True:
    writer_event.wait()
    while writer_event.is_set():
      array[id].value += 1
    barrier.wait()


def safe_reader( N, array, semaphore, writer_event ):
  while True:
    time.sleep( 10 )
    writer_event.clear()
    barrier.wait()
    total = sum( [ array[i] for i in range(N) ] )
    print( total )
    writer_event.set()

# Note: this is only safe with
writers = 4
array = mp.Array('i', writers )
trigger = mp.Event()
barrier = mp.Barrier( writers + readers )

processes = [
  mp.Process( target=safe_writer, args=(counter, trigger) )
  for _ in range(writers)
] + [
  mp.Process( target=safe_reader, args=(counter, trigger) )
]

for process in processes:
  process.start()

trigger.set()

for process in processes:
  process.join()
