from collections import defaultdict
import sys
from typing import Iterable, List
import pytest

from lib import *
from util import *
import constants

def string_composition(s: str, k: int):
  return [s[i:i+k] for i in range(len(s)-k+1)]

def kmer_path_to_string(path: Iterable[str]):
  s = [path[0]]
  for comp in path[1:]:
    s.append(comp[-1])
  print(s[0:10])
  print(''.join(s[0:10]))
  return ''.join(s)

def overlap_graph(reads: Iterable[str]):
  n = len(reads[0])
  nodes = defaultdict(list)
  for read in reads:
    suffix = read[1:]
    for read2 in reads:
      if read2[0:n-1] == suffix:
        nodes[read].append(read2)
  return nodes

def de_bruijn_graph_from_string(s: str, k: int):
  kmers = string_composition(s, k)
  nodes = defaultdict(list)
  for kmer in kmers:
    prefix = kmer[:k-1]
    suffix = kmer[1:]
    nodes[prefix].append(suffix)
  return nodes

def de_bruijn_graph_from_kmers(kmers: List[str], k: int = None):
  if not k:
    k = len(kmers[0])
  nodes = defaultdict(list)
  for kmer in kmers:
    prefix = kmer[0:k-1]
    suffix = kmer[1:]
    nodes[prefix].append(suffix)
  return nodes

def test_week1():
  print()
  print_sep("Bioinformatics II: Week 1 - How do we assemble genomes? (Part 1/2)")

  print_sep("String Composition")
  print("""Solve the String Composition Problem.
    Input: An integer k and a string Text.
    Output: Compositionk(Text) (the k-mers can be provided in any order).
  """)
  test_string_composition()
  input = (read_from_db("string_composition_input"),100)
  soln = string_composition(*input)
  write_to_db("string_composition_output", soln)

  print_sep("String Spelled by a Genome Path")
  test_kmer_path_to_string()
  input = read_from_db("kmer_path_to_string_input")
  soln = kmer_path_to_string(input)
  write_to_db("kmer_path_to_string_output", soln)

  print_sep("Overlap Graph")
  print("""Solve the Overlap Graph Problem (restated below).
    Input: A collection Patterns of k-mers.
    Output: The overlap graph Overlap(Patterns), in the form of an adjacency list. (You may return the nodes and their edges in any order.)
Note: You don't need to account for repeated elements in Patterns﻿ in this problem.""")
  test_overlap_graph()
  input = read_from_db("overlap_graph_input")
  soln = overlap_graph(input)
  write_to_db("overlap_graph_output", soln)

  print_sep("De Bruijn Graph from a String")
  print("""In general, given a genome Text, PathGraphk(Text) is the path consisting of |Text| - k + 1 edges, where the i-th edge of this path is labeled by the i-th k-mer in Text and the i-th node of the path is labeled by the i-th (k - 1)-mer in Text. The de Bruijn graph DeBruijnk(Text) is formed by gluing identically labeled nodes in PathGraphk(Text).
De Bruijn Graph from a String Problem: Construct the de Bruijn graph of a string.
    Input: An integer k and a string Text.
    Output: DeBruijnk(Text).""")
  test_de_bruijn_graph()
  input = read_from_db("de_bruijn_graph_from_string_input")
  soln = de_bruijn_graph_from_string(input, 12)
  write_to_db("de_bruijn_graph_from_string_output", soln)

  print_sep("De Bruijn Graph from k-mers")
  print("""Construct the de Bruijn graph from a set of k-mers.
    Input: A collection of k-mers Patterns.
    Output: The adjacency list of the de Bruijn graph DeBruijn(Patterns).""")
  input = read_from_db("de_bruijn_graph_from_kmers_input")
  soln = de_bruijn_graph_from_kmers(input)
  write_to_db("de_bruijn_graph_from_kmers_output", soln)

def test_string_composition():
  input = ('CAATCCAAC',5)
  output = string_composition(*input)
  assert sorted(output) == sorted(["CAATC","AATCC","ATCCA","TCCAA","CCAAC"])
  print(c("GREEN","PASSED"))

def test_kmer_path_to_string():
  path = ['ATG', 'TGC', 'GCA']
  assert kmer_path_to_string(path) == 'ATGCA'

  path = ['ACCGA','CCGAA','CGAAG','GAAGC','AAGCT']
  assert kmer_path_to_string(path) == 'ACCGAAGCT'

def test_overlap_graph():
  input = (['ATGCG','GCATG','CATGC','AGGCA','GGCAT','GGCAC'],)
  output = overlap_graph(['ATGCG','GCATG','CATGC','AGGCA','GGCAT','GGCAC'])
  assert output == {'GCATG': ['CATGC'], 'CATGC': ['ATGCG'], 'AGGCA': ['GGCAT', 'GGCAC'], 'GGCAT': ['GCATG']}

def test_de_bruijn_graph():
  input = ("AAGATTCTCTAAGA", 4)
  output = de_bruijn_graph_from_string(*input)
  assert output == {'AAG': ['AGA', 'AGA'], 'AGA': ['GAT'], 'GAT': ['ATT'], 'ATT': ['TTC'], 'TTC': ['TCT'], 'TCT': ['CTC', 'CTA'], 'CTC': ['TCT'], 'CTA': ['TAA'], 'TAA': ['AAG']}

def test_de_bruijn_graph_from_kmers():
  input = (['GAGG','CAGG','GGGG','GGGA','CAGG','AGGG','GGAG'], 4)
  output = de_bruijn_graph_from_kmers(*input)
  assert output == {'GAG': ['AGG'], 'CAG': ['AGG', 'AGG'], 'GGG': ['GGG', 'GGA'], 'AGG': ['GGG'], 'GGA': ['GAG']}

if __name__ == '__main__':
  init_db()
  sys.exit(pytest.main(["-s", __file__ + "::test_week1"])) #-s to not suppress prints
