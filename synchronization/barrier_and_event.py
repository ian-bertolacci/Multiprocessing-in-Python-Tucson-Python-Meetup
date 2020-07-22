#!/usr/bin/env python3
import time
import multiprocessing as mp

def safe_writer( id, array, barrier, writers_safe_event ):
  while True:
    # Wait for it to be ok for writers to worker
    writers_safe_event.wait()
    # Check if signaled to stop
    while writers_safe_event.is_set():
      array[id] += 1
    # Wait for everyone to stop
    barrier.wait()


def safe_reader( array, barrier, writers_safe_event ):
  while True:
    time.sleep( 1 )
    # Tell writers to stop working
    writers_safe_event.clear()
    # Wait for everyone to stop
    barrier.wait()
    # Read the array
    local_copy = [ v for v in array ]
    # Tell writers to continue
    writers_safe_event.set()
    # print information
    total = sum( local_copy )
    for pid in range(len(local_copy)):
      print( f"{pid}: {local_copy[pid]}/{total}" )
    print( "========" )


# Note: this is only safe with one reader!
writers = 4
array = mp.Array('i', writers )
writers_safe_event = mp.Event()
barrier = mp.Barrier( writers + 1 )

processes = [
  mp.Process( target=safe_writer, args=(pid, array, barrier, writers_safe_event) )
  for pid in range(writers)
] + [
  mp.Process( target=safe_reader, args=(array, barrier, writers_safe_event) )
]

for process in processes:
  process.start()

writers_safe_event.set()

for process in processes:
  process.join()

print( counter.value )
