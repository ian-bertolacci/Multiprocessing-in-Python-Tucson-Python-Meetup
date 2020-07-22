#!/usr/bin/env python3
import multiprocessing as mp
import time, argparse
import numpy as np

class Timer:
  unstarted_value = -np.inf
  def __init__( this ):
    this.begin = Timer.unstarted_value
    this.end = Timer.unstarted_value

  def start( this ):
    this.end = Timer.unstarted_value
    this.begin = time.time()

  def stop( this ):
    this.end = time.time()

  def elapsed( this ):
    return this.end - this.begin

def work_function( a, b ):
  return np.sqrt( np.sqrt(a) / np.sqrt(b) )

def run_serial_benchmark( N ):
  timer = Timer()

  l = [None]*N

  timer.start()
  for (i,(a,b)) in enumerate(zip( range(1, N+1), range(N, 0, -1) )):
    l[i] = work_function(a, b)
  timer.stop()
  return timer.elapsed()

def run_parallel_benchmark( N, P ):
  timer = Timer()
  with mp.Pool( P ) as pool:

    timer.start()
    result = pool.starmap(
      work_function,
      zip(
        range(1, N+1),  # [1,N]
        range(N, 0, -1) # [N,1]
      )
    )
    timer.stop()
  return timer.elapsed()

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument( "N", type=int, help="Number of work elements" )
  argparser.add_argument( "P", type=int, help="Number of processes" )
  argparser.add_argument( "--trials", type=int, default=10, help="Run multiple trials" )
  # argparser.add_argument( "--serial", action="store_true", default=False, help="Run in serial" )

  args = argparser.parse_args()

  trial_elapsed = [0] * args.trials
  for trial in range(args.trials):
    print(f"Trial {trial + 1}")
    if args.P == 1:
      trial_elapsed[trial] = run_serial_benchmark(args.N)
    else:
      trial_elapsed[trial] = run_parallel_benchmark(args.N, args.P)
    print( f"\t{trial_elapsed[trial]} seconds" )
    print( f"\t{args.N/trial_elapsed[trial]} elements/second" )

  if args.trials > 1:
    print( f"{np.mean(trial_elapsed)} seconds on average" )
    print( f"{args.N/np.mean(trial_elapsed)} elements/second on average" )

    print( f"{max(trial_elapsed)} seconds in worst case" )
    print( f"{args.N/max(trial_elapsed)} elements/second in worst case" )

if __name__ == "__main__":
  main()
