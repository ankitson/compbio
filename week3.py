import pytest
import math

from lib import *
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

  print("all assertions passed!")

if __name__ == '__main__':
  pytest.main(["-s", __file__]) #-s to not suppress prints