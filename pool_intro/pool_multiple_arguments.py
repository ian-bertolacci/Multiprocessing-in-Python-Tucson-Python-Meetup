#!/usr/bin/env python3
import multiprocessing as mp


def function( a, b ):
  # print( f"function({a}, {b})" )
  return a / b

number_of_processes = 4
iterations = 10
pool = mp.Pool( number_of_processes )
result = pool.starmap(
  function,
  zip(
    range(iterations),
    range(iterations, 0, -1)
  )
)

print( result )
