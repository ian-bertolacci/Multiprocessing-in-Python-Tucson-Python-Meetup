#!/usr/bin/env python3
import random, time, operator, os, argparse, sys, queue
import multiprocessing as mp
from itertools import chain, repeat
from pprint import pprint
from numpy import inf, pi, cos
from functools import reduce

# Timer class
class Timer:
  def __init__( self ):
    self.begin = 0
    self.end = 0

  def start( self ):
    self.begin = time.time()

  def stop( self ):
    self.end = time.time()

  def elapsed( self ):
    return self.end - self.begin


# For printing without effects of the parallelism
stdout_lock = mp.Lock()
def parprint( *args, **kwargs ):
  pid = os.getpid()
  with stdout_lock:
    print( f"({pid}):", *args, **kwargs )

# hash function for a list
def lhash( l ):
  return reduce( operator.xor, map( hash, l ) )

# Function that makes work and puts it on queue
def make_work( work_queue, num_makers, decay, verbosity, seed ):
  if num_makers.value <= 0:
    raise RuntimeError( "Maker just starting num_makers <= 0" )

  if seed != None:
    random.seed( seed )

  probability = 1.0
  rand_check = 0.0
  while rand_check <= probability:
    time.sleep( random.uniform(0.01, 2.0) )

    work = [ random.uniform(0.0, 2*pi) for i in range(random.randrange(1,10)) ]

    if verbosity >= 2:
      parprint( f"About to put {lhash(work)}, {len(work)}" )

    work_queue.put( work )

    if verbosity >= 1:
      parprint( f"Put {lhash(work)}" )

    rand_check = random.uniform( 0.0, 1.0 )
    probability *= 1.0 - decay

    if verbosity >= 3:
      parprint( f"p={probability}, r={rand_check}" )

  if verbosity >= 1:
    parprint( f"make_work finished" )

  with num_makers.get_lock():
    num_makers.value -= 1


def do_work( work_queue, num_makers, work_function, timeout, verbosity, seed ):
  if seed != None:
    random.seed( seed )

  get_work_timeout_after_no_makers = 0
  while get_work_timeout_after_no_makers < 2:
    work = None

    if verbosity >= 2:
      parprint( f"Getting work" )

    try:
      work = work_queue.get( timeout=timeout )
    except queue.Empty:
      if verbosity >= 2:
        parprint( f"Timed-out" )
      if num_makers.value == 0:
        get_work_timeout_after_no_makers += 1
      continue

    if work != None:
      if verbosity >= 1:
        parprint( f"Got {lhash(work)}, {len(work)}" )

      if verbosity >= 2:
        parprint( f"Doing work" )

      for work_element in work:
        if verbosity >= 3:
          parprint( f"Working on {work_element}" )
        time.sleep( random.uniform(0.01, 2.0) )

        work_function( work_element )

      if verbosity >= 2:
        parprint( f"Done with work" )

  if verbosity >= 1:
    parprint( f"do_work finished" )


def main( argv ):
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "-d", "--decay", type=float, default=.01 )
  argparser.add_argument( "-m", "--maker-processes", type=int, default=int(mp.cpu_count()/2) )
  argparser.add_argument( "-w", "--worker-processes", type=int, default=int(mp.cpu_count()/2) )
  argparser.add_argument( "-t", "--timeout", type=float, default=.5 )
  argparser.add_argument( "-s", "--seed", type=int, default=None )
  argparser.add_argument( "-v", "--verbosity", type=int, default=1 )

  args = argparser.parse_args( argv )

  if args.decay <= 0 or 1 < args.decay:
    raise ValueError( f"--decay <value> must be in range (0, 1] (is {args.decay})" )

  timer = Timer()
  timer.start()

  with mp.Manager() as manager:
    work_queue = manager.Queue()
    makers_count = mp.Value( 'i', args.maker_processes )

    processes = \
      [ mp.Process( target=make_work, args=(work_queue, makers_count, args.decay, args.verbosity, args.seed) ) for _ in range(args.maker_processes) ] + \
      [ mp.Process( target=do_work, args=(work_queue, makers_count, cos, args.timeout, args.verbosity, args.seed) ) for _ in range(args.worker_processes) ]

    for process in processes:
      process.start()
    for process in processes:
      process.join()

  timer.stop()
  print( f"Elapsed: {timer.elapsed()}s" )

if __name__ == "__main__":
  main(sys.argv[1:])
