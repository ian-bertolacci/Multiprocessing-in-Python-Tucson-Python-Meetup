#!/usr/bin/env python3
import multiprocessing as mp
from itertools import chain
from pprint import pprint
from math import *
import operator, sys, argparse, time

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

def debug_calling_function( *args, **kwargs ):
  arguments_str = ', '.join(
    [ str(i) for i in args ] +
    [ f'{key} = {value}' for key, value in kwargs.items() ]
  )
  ret_value = f"debug_calling_function( {arguments_str} )"
  print( ret_value )
  return ret_value

def chunk_list( list_arg, chunks=None, chunk_size=None ):
  if chunks == None and chunk_size == None:
    raise ValueError( "Must specify either chunks or chunk_size." )
  elif chunks != None and chunk_size != None:
    raise ValueError( "My only specify either chunks or chunk_size, but not both." )
  elif chunks != None:
    chunk_size = int( ceil( len(list_arg)/chunks ) )

  for i in range(0, len(list_arg), chunk_size):
      yield list_arg[i:i + chunk_size]


def main( argv ):
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "-n", type=int, default=10 )
  argparser.add_argument( "-p", "--processes", type=int, default=mp.cpu_count() )
  argparser.add_argument( "-q", "--quiet", default=False, action="store_true" )
  args = argparser.parse_args( argv )

  init_timer, add_timer, partial_sum_timer, sum_timer = ( Timer() for i in range(4) )

  init_timer.start()

  A = list( range( 0, args.n  ) )
  B = list( range( args.n, 2*args.n ) )

  init_timer.stop()

  with mp.Pool( args.processes ) as pool:
    add_timer.start()

    added_AB = \
      pool.starmap(
        operator.add,
        zip( A, B )
      )

    add_timer.stop()

    partial_sum_timer.start()

    partial_sum_AB = pool.map(
      sum,
      chunk_list( added_AB, chunks=args.processes )
    )

    partial_sum_timer.stop()

    sum_timer.start()

    sum_AB = sum( partial_sum_AB )

    sum_timer.stop()

  if not args.quiet:
    print( "  [ " + ', '.join( (f"{v:>2}" for v in A) ) + " ]" )
    print( "+ [ " + ', '.join( (f"{v:>2}" for v in B) ) + " ]" )
    print( "= [ " + ', '.join( (f"{v:>2}" for v in added_AB) ) + " ]" )
    print( f"sum: {sum_AB}" )

  print( f"Initialization took: {init_timer.elapsed(): 6.5} seconds" )
  print( f"Adding A + B took:   {add_timer.elapsed(): 6.5} seconds" )
  print( f"Partial sum took:    {partial_sum_timer.elapsed(): 6.5} seconds" )
  print( f"Final sum took:      {sum_timer.elapsed(): 6.5} seconds" )

if __name__ == "__main__":
  main( sys.argv[1:] )
