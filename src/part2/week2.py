from collections import defaultdict
import copy
import sys
from typing import Iterable, List
import pytest
import random

from lib import *
from util import *
import constants

def eulerian_cycle(graph, start=None):
  my_graph = copy.deepcopy(graph)
  def visit(node):
      while my_graph[node]:
          next_node = my_graph[node].pop()
          visit(next_node)
      cycle.append(node)

  cycle = []
  start_node = start if start else 0
  visit(start_node)

  # The result is reversed because the visit function appends nodes in reverse order
  return list(reversed(cycle))

def eulerian_path(graph):
  incomings = {}
  for (k,vs) in graph.items():
      for v in vs:
         incomings[v] = incomings.get(v,[]) + [k]
      if not k in incomings:
         incomings[k] = []
  start, end = None, None
  print(incomings)
  for k,v in incomings.items():
    if len(v) == len(graph[k]) + 1:
      end = k
    if len(v) == len(graph[k]) - 1:
      start = k
    
  print(dotviz_graph(graph))
  assert start != None, "no start node for eulerian path"
  assert end != None, "no end node for eulerian path"
  new_graph = copy.deepcopy(graph)
  new_graph[end] = graph[end] + [start]
  return eulerian_cycle(new_graph, start=start)[:-1]
  
def test_week2():
  print()
  print_sep("Bioinformatics II: Week 1 - How do we assemble genomes? (Part 2/2)")

  print_sep("Finding Eulerian Cycles")
  graph1 = parse_graph(open('../inputs/part2/in1.txt').read())
  cycle1 = eulerian_cycle(graph1)
  print(f"In graph: {graph1}\nFound cycle: {cycle1}")
  expected_out = parse_list(open('../inputs/part2/out1.txt').read(),int)
  assert rotation_eq(cycle1[1:], expected_out[1:]), f"Expected {expected_out[1:]} but got {cycle1[1:]}"

  graph2 = parse_graph(open('../inputs/part2/in2.txt').read())
  cycle2 = eulerian_cycle(graph2)
  print(f"Found cycle: {str(cycle2):.100}..")
  write_iter(cycle2, "../inputs/part2/out2.txt") #TODO: Change paths to make sense
  
  print_sep("Finding Eulerian Paths")
  graph1 = parse_graph(open('../inputs/part2/in3.txt').read())
  path1 = eulerian_path(graph1)
  print(f"In graph {graph1}\nFound path: {str(path1):.100}")
  assert path1 == parse_list(open('../inputs/part2/out3.txt').read(), int)

  graph2 = parse_graph(open('../inputs/part2/in4.txt').read())
  path2 = eulerian_path(graph2)
  print(f"In graph {graph2}\nFound path: {str(path2):.100}")
  write_iter(path2, "../inputs/part2/out4.txt")
  # assert path2 == parse_list(open('../inputs/part2/out4.txt').read(), int)





def rotation_eq(l1:list, l2:list):
  """Tests if two lists are rotations of each other"""
  start_indexes = [i for i, x in enumerate(l2) if x == l1[0]]
  for start_index in start_indexes:
    rotated_l2 = l2[start_index:] + l2[:start_index]
    if rotated_l2 == l1:
        return True
  return False

if __name__ == '__main__':
  sys.exit(pytest.main(["-s", __file__ + "::test_week2"])) #-s to not suppress prints
 
