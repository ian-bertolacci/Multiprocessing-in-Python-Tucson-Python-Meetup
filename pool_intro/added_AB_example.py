#!/usr/bin/env python3
from multiprocessing import *
from itertools import chain
from pprint import pprint
import operator

A = list( range(  0, 10 ) )
B = list( range( 10, 20 ) )

with Pool( ) as pool:
  added_AB = pool.starmap(
              operator.add,
              zip( A, B )
            )

print( "  [ " + ', '.join( (f"{v:>2}" for v in A) ) + " ]" )
print( "+ [ " + ', '.join( (f"{v:>2}" for v in B) ) + " ]" )
print( "= [ " + ', '.join( (f"{v:>2}" for v in added_AB) ) + " ]" )
