#!/usr/bin/env python3
import multiprocessing as mp
from itertools import chain
from pprint import pprint

def function( *args, **kwargs ):
  arguments_str = ', '.join(
    [ str(i) for i in args ] +
    [ f'{key} = {value}' for key, value in kwargs.items() ]
  )
  ret_value = f"function( {arguments_str} )"
  print( ret_value )
  return ret_value

number_of_processes = 10

with mp.Pool( number_of_processes ) as pool:
  print( "Calling function on work:" )
  values = pool.starmap(
              function, # What we are calling
              enumerate( "Hello world" ) # The iterable object
            )
  print( "Result:")
  pprint(values)
