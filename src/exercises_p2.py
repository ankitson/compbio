import pytest
from lib import *
from util import *
import logging
import constants
import os

if __name__ == '__main__':
  log_level = "DEBUG"
  pytest.main(["-s", __file__ + "::test_part2", f"--log-cli-level={log_level}"],) #-s to not suppress prints

def test_part2():
  print_sep("""\nBioinformatics Part 2: Which DNA patterns play the role of molecular clocks?""")

  print_sep("""Implement Motif Enumeration            
    Input: Integers k and d, followed by a space-separated collection of strings Dna.
    Output: All (k, d)-motifs in Dna.""")
  assert(
    sorted(motif_enumerate_bruteforce(['ATTTGGC','TGCCTTA','CGGTATC', 'GAAAATT'],k=3,d=1)) ==
    ['ATA','ATT','GTT','TTT']
  )
  run_test('../debug_datasets/MotifEnumeration', motif_enumerate_bruteforce, lambda inp: (inp[1],inp[0][0],inp[0][1]), exp_out_transform=lambda s: [] if s==["nan"] else s)

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
  print(
    score_motif_profile_entropy(
      profile_motif_matrix(input_matrix).values
    )
  )

  print_sep("""Implement MedianString().
    Input: An integer k, followed by a space-separated collection of strings Dna.
    Output: A k-mer Pattern that minimizes d(Pattern, Dna) among all possible choices of k-mers. (If there are multiple such strings Pattern, then you may return any one.)""")

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
  print(median_strings(*input))
  # The spec says to return only 1 median string but my function returns all. Hence the out transform
  run_test('../debug_datasets/MedianString', median_strings, inp_transform=lambda t: (t[1], t[0]), out_transform=lambda t: t[0])

  print_sep("Profile-most probable k-mer")
  text = "CGTGTCGATTCTCTAGAGTATTAGGTTTGTATAGGCAAGGGTGGCGGGTAAATTGGAAGTCACTTCCTGGGACTATACGGCCGTCCGCGCTTTCAGCTACAAGTCATTTCCCCATGGCGATCGACCCCTTGATCGACAAGGCGTTAATACCAGTCTATCTGCTTACCTTTAATCAAAAGATCAATAACCACGGGGCTCAACCGCGAGTATGATATTATTATAACAATGCTCTGTGCAGAAAGGCTCTTAACGAGTCAAGCTGGGAGGTGCTTCCATCCGCAGGCCCTAAAAGGCCGTGTGTCAAGCGAATTTCCTGGTACCGGATATTACGAAGTAGACATACAGCTACGATATTAAGCCAAGCTGCTTCCAAAGCCTCCCCGCATATGCATCAATGCTTACACATCCGTACCACATCAACACTCCGCGGGCGCACCCGCAGGATGATCATATTCCTATACATGTTTATGAGCCAGTGCTGTTTTTTGGGCTCCTTCTCCGAATGTTCGGGATTTAGCGAAGGCGCGCACAGTCATACTTGCCTAAATGCCGAAATTGCTTATTGCAGATAACCGAAGCACCCGCTCCCTTGTCTCACCTAGAGGCGGCCCATCACCCCGATTAGACAATCATGCTACACTGCATTCAAGTATCGGTATCACGTATCACGCTTACGCTACGTAGTGACAAGCTTTGAGCAACGACTGTTTGTGGTCGAGGTGGCATCGCGGCACTTCTACGTCACAAGGTCTCCCTTCCCTAGCTTTATTGGGCATAGTAACGAATACCAATCGGGGACGTCTGTCATCTACACGGGGTATGGCACTGTCTGTCGTACACGGACACTGGCGTCAAACATTTAAGTCAAACAATATTGTAGCTGCCTTGCGAGCTCTTGAACCCCTTCAATCAATCCTCGGGAGCGCATTCGGTTTGACGCGGAATAGGGCTCATTACTAGAGATTGTAGTTAGCGCGGATGATATTCACTCATATCATAG"
  profile = profile_matrix_as_dataframe(np.array([
    [0.277,0.241,0.253,0.277,0.253,0.229,0.325,0.229,0.229,0.301,0.241,0.205],
    [0.181,0.241,0.313,0.229,0.241,0.277,0.253,0.205,0.229,0.337,0.229,0.241],
    [0.241,0.229,0.193,0.229,0.253,0.277,0.229,0.253,0.337,0.157,0.205,0.289],
    [0.301,0.289,0.241,0.265,0.253,0.217,0.193,0.313,0.205,0.205,0.325,0.265]]))
  k = 12
  print(f"Calculating most probable {k}-mer in {text} according to this matrix:\n{profile}")
  print(profile_most_probable_kmer(text, profile, k))
  def input_fix(inp):
    lines = inp[2:]
    npar = np.array(lines)
    profile = profile_matrix_as_dataframe(npar)
    return (inp[0],profile,inp[1])
  run_test('../debug_datasets/ProfileMostProbableKmer', profile_most_probable_kmer, inp_transform=input_fix)

  print_sep("Greedy Motif Search")
  input = (['GGCGTTCAGGCA','AAGAATCAGTCA','CAAGGAGTTCGC','CACGTCAATCAC','CAATAATATTCG'],3,False)
  assert(greedy_motif_search(*input) == ['CAG','CAG','CAA','CAA','CAA'])
  def input_fix(inp):
    return (inp[1],inp[0][0])
  run_test('../debug_datasets/GreedyMotifSearch', greedy_motif_search, inp_transform=input_fix, out_transform=lambda l: l)

  print_sep("Greedy Motif Search with pseudo-counts (probabilities never 0)")
  input = (['GGCGTTCAGGCA','AAGAATCAGTCA','CAAGGAGTTCGC','CACGTCAATCAC','CAATAATATTCG'], 3)
  assert(greedy_motif_search(*input,pseudo_counts=True) == ['TTC','ATC','TTC','ATC','TTC'])
  def input_fix(inp):
    return (inp[1],inp[0][0],True,False) #set pseudo-counts to True here
  run_test(f'../debug_datasets/GreedyMotifSearchPseudocounts', greedy_motif_search, inp_transform=input_fix, out_transform=lambda l: l)
  sys.exit(1)

  print_sep("Quiz")

  motif_matrix = [
    "CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC",
    "GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC",
    "GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG"
  ]
  print(f"Median strings: " + str(median_strings(motif_matrix, 7)))

  profile = np.array([
    [0.4,0.3,0.0,0.1,0.0,0.9], #A
    [0.2,0.3,0.0,0.4,0.0,0.1], #C
    [0.1,0.3,1.0,0.1,0.5,0.0], #G
    [0.3,0.1,0.0,0.4,0.5,0.0]]) #T 
  input = 'CAGTGA'
  rows = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
  prob = 1
  for (i,char) in enumerate(input):
    mult = profile[rows[char],i]
    prob *= mult
  print(f"Probability of {input} given profile = {prob}")
