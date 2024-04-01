import pytest
from lib import *
from util import *
import logging
import constants
import os

if __name__ == '__main__':
  log_level = "INFO"
  pytest.main(["-s", __file__ + "::test_part1", f"--log-cli-level={log_level}"],) #-s to not suppress prints

def test_part1():
  print_sep("""\nBioinformatics Part 1: Where in the Genome Does Replication Begin?""")

  #1.2-5
  print_sep("""Implement pattern count
    Input: Strings Text and Pattern.
    Output: Count(Text, Pattern).""")
  assert(len(pattern_match("GCGCG", "GCG")) == 2)

  #1.2-12
  print_sep("""Frequent Words            
    Input: A string Text and an integer k.
    Output: All most frequent k-mers in Text.
  """)
  freq_words = frequent_words("ACGTTGCATGTCGCATGATGCATGAGAGCT",4)
  assert(sorted(freq_words) == ['CATG', 'GCAT'])
  run_test("../debug_datasets/FrequentWords", frequent_words)

  #1.3-2
  print_sep("""Reverse Complement            
    Input: A DNA string Pattern.
    Output: Patternrc , the reverse complement of Pattern.
  """)
  assert(reverse_complement('AAAACCCGGT') == 'ACCGGGTTTT')
  run_test("../debug_datasets/ReverseComplement", reverse_complement)

  #1.3-5
  print_sep("""Pattern Matching
    Input: Two strings, Pattern and Genome.
    Output: A collection of integers specifying all starting positions where Pattern appears as a substring of Genome.
  """)
  assert(pattern_match('GATATATGCATATACTT','ATAT') == [1,3,9])
  run_test("../debug_datasets/PatternMatching", pattern_match, inp_transform=lambda t: (t[1],t[0]))

  #1.3-6
  print_sep("""Return a space-separated list of starting positions (in increasing order) where CTTGATCAT appears as a substring in the Vibrio cholerae genome""")
  with open(constants.DATASETS['cholera']) as f: vibrio_cholera_genome = f.read()
  ans = pattern_match(vibrio_cholera_genome, 'CTTGATCAT')
  print(' '.join([str(x) for x in ans]))
  assert(ans == [60039,98409,129189,152283,152354,152411,163207,197028,200160,357976,376771,392723,532935,600085,622755,1065555])
  print_sep("""Positions for the reverse complement:""")
  ans = pattern_match(vibrio_cholera_genome, reverse_complement('CTTGATCAT'))
  print(' '.join([str(x) for x in ans]))

  #1.4-5
  print_sep("""Clump Finding Problem: Find patterns forming clumps in a string.
    Input: A string Genome, and integers k, L, and t.
    Output: All distinct k-mers forming (L, t)-clumps in Genome.""")
  ans = find_clumps('CGGACTCGACAGATGTGAAGAACGACAATGTGAAGACTCGACACGACAGAGTGAAGAGAAGAGGAAACATTGTAA', 5, 50, 4)
  assert(ans == ['CGACA', 'GAAGA'])
  run_test("../debug_datasets/ClumpFinding", find_clumps, lambda inp: (inp[0], inp[1][0], inp[1][1], inp[1][2]))

  #1.4-6
  print_sep("Find how many 9-mers form (500,3) clumps in the E. Coli Genome (4.6MB!)")
  with open(constants.DATASETS['e_coli']) as f: ecoli_genome = f.read()
  ans = find_clumps(ecoli_genome, k=9, L=500, t=3)
  write_temp(' '.join(ans))
  print(len(ans))

  #1.7-8
  print_sep("""Give all the values of Skew_i(GAGCCACCGCGATA) for i ranging from 0 to 14 as a collection of space-separated integers""")
  skews = [str(s) for s in gc_skew_iter("GAGCCACCGCGATA")]
  ans = ' '.join(skews)
  print(ans)
  
  print_sep("""Minimum Skew Problem: Find a position in a genome where the skew diagram attains a minimum.
    Input: A DNA string Genome.
    Output: All integer(s) i minimizing Skewi (Genome) among all values of i (from 0 to |Genome|).
  """)
  test = 'TAAAGACTGCCGAGAGGCCAACACGAGTGCTAGAACGAGGGGCGTAAACGCGGGTCCGAT'
  soln = minimum_skew(test)
  print(f"minimum_skew({test}) = {soln}")
  assert(soln == [11, 24])
  run_test("../debug_datasets/MinimumSkew", minimum_skew)


  print_sep("""Hamming Distance Problem: Compute the Hamming distance between two strings.
    Input: Two strings of equal length.
    Output: The Hamming distance between these strings.
  """)
  test = ("GGGCCGTTGGT", "GGACCGTTGAC")
  soln = hamming_distance(*test)
  print(f"hamming_distance({test}) = {soln}")
  assert(soln == 3)
  run_test("../debug_datasets/HammingDistance", hamming_distance)

  print_sep("""Approximate Pattern Matching""")
  test = ("CGCCCGAATCCAGAACGCATTCCCATATTTCGGGACCACTGGCCTCCACGGTACGGACGTCAATCAAAT","ATTCTGGA",3)
  soln = pattern_match_approx(*test)
  print(f"pattern_match_approx({test}) = {soln}")
  assert(soln == [6,7,26,27])
  run_test('../debug_datasets/ApproximatePatternMatching', pattern_match_approx, lambda t: (t[1], t[0], t[2]))

  print_sep("""Approximate Pattern Count""")
  test = ("AACAAGCTGATAAACATTTAAAGAG","AAAAA",2)
  soln = pattern_count_approx(*test) 
  print(f"pattern_count_approx({test}) = {soln}")
  assert(soln == 11)
  run_test('../debug_datasets/ApproximatePatternCount', pattern_count_approx, lambda t: (t[1], t[0], t[2]))

  print_sep("""String neighbors""")
  soln = neighbors_lt('AAT', d=1) 
  print(f"1-neighbors of AAT: {soln}")
  assert(soln ==  {'GAT', 'TAT', 'CAT', 'AAA', 'AAT', 'ATT', 'AAC', 'AAG', 'ACT', 'AGT'})

  print_sep("""Frequent words (k-mers) with mismatches""")
  test = ("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1)
  soln = sorted(frequent_words_with_mismatches(*test)[0])
  print(f"kmers_with_mismatches({test}) = {soln}")
  assert(soln == ['ATGC', 'ATGT', 'GATG'])
  assert(sorted(frequent_words_with_mismatches("AGGT", k=2, d=1)[0]) == ['GG'])
  assert(sorted(frequent_words_with_mismatches("AGGGT", k=2, d=0)[0]) == ['GG'])
  assert(sorted(frequent_words_with_mismatches("AGGCGG", k=3, d=0)[0]) == ['AGG','CGG','GCG','GGC'])
  run_test('../debug_datasets/FrequentWordsMismatches', frequent_words_with_mismatches, lambda t: (t[0], t[1][0], t[1][1]), lambda t: t[0])
  
  print_sep("Frequent words (k-mers) with mismatches and complements")
  test = ("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1)
  soln = frequent_words_with_mismatches_complements(*test)
  print(f"kmers_with_mismatches_complements({test}) = {soln}")
  assert(sorted(soln) == ['ACAT', 'ATGT'])

  run_test('../debug_datasets/FrequentWordsMismatchesReverseComplements', 
           frequent_words_with_mismatches_complements, 
           inp_transform=lambda t: (t[0], t[1][0], t[1][1]), 
           out_transform=lambda t: t)

  print_sep("Epilogue: Find a DnaA Box in Salmonella enterica!!")
  print("The skew diagram shows the minimum at around position 3,923,600")
  salmonella: str = constants.dataset('salmonella')
  ori_cands = minimum_skew(salmonella)
  print(f"Minimum skew positions computed: {ori_cands}")
  ori_cand = ori_cands[0]

  region = salmonella[ori_cand-1000:ori_cand+1000]
  compute = True

  most_freq = {}
  if compute:
    for k in range(7,13):
      for d in range(1,2):
        freq_words, count = frequent_words_with_mismatches_complements(region, k=k, d=d, debug=True)
        print(f"Most freq {k}mers at distance {d} with freq {count} are")
        print(freq_words)
        most_freq[k] = (freq_words,count)
  
  for k in range(7,13):
    print_sep(f"Most freq {k}mers at distance 1 with freq {most_freq[k][1]} are")
    print(f"exact matches:")
    print_highlight(region, most_freq[k][0], color="RED")
    print(f"matches with nbrs and complements:")
    all_sets = set().union(*[neighbor_lt_complement(kmer, 1) for kmer in most_freq[k][0]]).union(set(most_freq[k][0]))
    print_highlight(region, all_sets, color="RED")

  print("all assertions passed!")
