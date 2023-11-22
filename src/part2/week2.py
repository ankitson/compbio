from collections import defaultdict
import sys
from typing import Iterable, List
import pytest

from lib import *
from util import *
import constants

def euler_tour(graph):
  """graph is a list of adjacency lists"""
  #EulerianCycle(Graph)
    # form a cycle Cycle by randomly walking in Graph (don't visit the same edge twice!)
    # while there are unexplored edges in Graph
        # select a node newStart in Cycle with still unexplored edges
        # form Cycle’ by traversing Cycle (starting at newStart) and then randomly walking 
        # Cycle ← Cycle’
    # return Cycle
  
  nodes = graph
  N = len(nodes)
  seen_edges = set()
  
  start = 0
  curr = start
  current_tour = []
  for v in nodes[curr]:
    if not (curr,v) in seen_edges:
      current_tour.append((curr,v))
      seen_edges.add((curr,v))
      curr = v
    if v == start:
      break
    
  return current_tour

def test_week2():
  print()
  print_sep("Bioinformatics II: Week 1 - How do we assemble genomes? (Part 2/2)")

  graph = [
    [1,2],
    [0,2],
    [0,1]
  ]
  tours = euler_tour(graph)
  print(tours)

if __name__ == '__main__':
  sys.exit(pytest.main(["-s", __file__ + "::test_week2"])) #-s to not suppress prints
 
