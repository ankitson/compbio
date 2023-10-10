import pytest
import math

from lib import *
from util import *
import constants

def test_week3():
  print_sep("Motif Enumeration Bruteforce")

  assert(
    sorted(motif_enumerate_bruteforce(['ATTTGGC','TGCCTTA','CGGTATC', 'GAAAATT'],k=3,d=1)) ==
    ['ATA','ATT','GTT','TTT']
  )

  print_iter(sorted(motif_enumerate_bruteforce(
    ['TTCAGACCATTAATACAGGGCGCCA','GTTGAACTGACAACATGTTCGACTA','GACCGTGCCGCAAAAGGGGGTCCTG','ATTCCTAATAAGCCTCAAGAGCGAA','GAAAATGCATTTTAATAAGAGGGCG','GGTTCATGAAAACATAAATATTACG'],
    k=5,d=2
  )))

  print_sep("Motif Matrix Entropy")

  motifs="""TCGGGGGTTTTT
  CCGGTGACTTAC
  ACGGGGATTTTC
  TTGGGGACTTTT
  AAGGGGACTTCC
  TTGGGGACTTCC
  TCGGGGATTCAT
  TCGGGGATTCCT
  TAGGGGAACTAC
  TCGGGTATAACC"""
  rows = [row.strip() for row in motifs.split('\n')]
  input_matrix = np.array([list(row) for row in rows])

  print("Scoring this matrix: ")
  print(input_matrix)
  print(score_motif_profile_entropy(profile_motif_matrix(input_matrix)))

  print_sep("Median String")

  input = (['AGCACTATAACGAGCTTGGCTATATGACAAGCGAGGGGGCTA',
'TAAACCATACCGGCCCCATGCAATGTGGAGGCCGATAATGCC',
'ATAATGCCATTTACGTTCGGGTGAGATCTGCACAAGATAGCG',
'AGAAATTCAACGGTATCTCATTCACATGCGATATCGACGGGT',
'CCCGACATCGCAAGGTCCAGTACACACAGTGAGGCGATAGCG',
'GCACCTCTATGAATAGCGCAATTTTCACTATGTAATTAGCCG',
'GATTACATAACGCCACTTTCGTCTCAGCGTAGCGCAAAGCTC',
'AGCGACCGGATCTTCAGATCGAAATACAACATTCGCATAACG',
'GGTCCGGCACAGATGAGCGCGTCACCCAGAATATCGCATCGT',
'AGGTGTCAACCAATAGCGGCGAGTCCTTCCTCAAACAGGCCC'],6)
  print(median_string(*input))

if __name__ == '__main__':
  pytest.main(["-s", __file__]) #-s to not suppress prints