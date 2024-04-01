import pytest
import math

from lib import *
from util import *
import constants

def test_week2():
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
  salmonella = constants.dataset('salmonella')
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

  print_sep("Week 2 Quiz")
  s = 'CTTGAAGTGGACCTCTAGTTCCTCTACAAAGAACAGGTTGACCTGTCGCGAAG'
  t = 'ATGCCTTACCTAGATGCAATGACGGACGTATTCCTTTTGCCTCAACGGCTCCT'
  print(f"Hamming distance = {hamming_distance(s,t)}")

  s = 'GATACACTTCCCGAGTAGGTACTG'
  skews = enumerate(list(gc_skew_iter(s)))
  min_skew = min(skews, key=lambda t: t[1])
  min_skew_index = min_skew[0]+1
  print(f"Min skew at position {min_skew_index}")

  soln = pattern_count_approx("CATGCCATTCGCATTGTCCCAGTGA", "CCC", d=2)
  print(f"Pattern count (CATGCCATTCGCATTGTCCCAGTGA, CCC, d=2) = {soln}")

  print(f"How many 4-mers are in the 3-neighborhood of ACGT?")
  soln = 1 + 4*3 + math.comb(4,2) * 3 * 3 + math.comb(4,3) * 3 * 3 * 3
  print(soln)
  nbrs = neighbors_lt('ACGT', 3)
  assert soln == len(nbrs)
  
  print(f"How many 5-mers are in the 2-neighborhood of pattern TGCAT?")
  soln = 1 + 5 *3 + math.comb(5,2) * 3 * 3
  print(soln) # 5 choose 0 -> dont mutate. 1 kmer.  5 choose 1 -> mutate only 1. (5 choose 1) * 3. 5 choose 2 -> mutatle both. (5 choose 2) * 3 * 3
  nbrs = neighbors_lt("TGCAT", 2)
  assert soln == len(nbrs)


  print("all assertions passed!")

if __name__ == '__main__':
  log_level = "INFO"
  pytest.main(["-s", __file__ + "::test_week2", f"--log-cli-level={log_level}"],) #-s to not suppress prints
