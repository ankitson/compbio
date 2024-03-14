import itertools
import math
import random
import sys
from typing import Iterable, Iterator, Tuple

import pytest
import numpy as np
import pandas as pd
from numpy import ndarray
import constants
from util import print_highlight_motifs, print_sep

def freq_map_kmers(text: str, k: int) -> list[str]:
  n = len(text)
  freqs = {}
  for i in range(n-k+1):
    kmer = text[i:i+k]
    freqs[kmer] = freqs.get(kmer, 0) + 1
  return freqs

#1.2 - 12
#output all most frequent k-mers in text
def frequent_words(text: str, k: int) -> list[str]:
  freq_map = freq_map_kmers(text, k)
  max_freq = max(freq_map.values())
  freq_words = []
  for (kmer,freq) in freq_map.items():
    if freq == max_freq:
      freq_words.append(kmer)
  return freq_words

def reverse(text: str) -> str:
  return text[::-1]

def complement(text: str) -> str:
  return text.translate(str.maketrans(constants.BASES_COMPLEMENTS))

def reverse_complement(text: str) -> str:
  return complement(reverse(text))

def pattern_match(text: str,pattern: str) -> list[int]:
  starts = []
  for i in range(len(text) - len(pattern) + 1):
    if text[i:i+len(pattern)] == pattern:
      starts.append(i)
  return starts

# Optimized version using sliding windows
def find_clumps(text: str, k: int, L: int, t: int) -> list[str]:
  """Clump Finding Problem: Find patterns forming clumps in a string.
        Input: A string Genome, and integers k, L, and t.
        Output: All distinct k-mers forming (L, t)-clumps in Genome.
  """
  n = len(text)
  clump_kmers = set()
  kmer_dict = {}

  window = text[:L]
  kmer_dict = freq_map_kmers(window, k)
  kmers_above_t = [k for (k,v) in kmer_dict.items() if v >= t]
  clump_kmers.update(kmers_above_t)
  
  # Slide the window and update the frequency map
  for i in range(1,n-L+1):
    # Remove the first k-mer of the previous window
    prev_kmer = text[i-1:i-1+k]
    kmer_dict[prev_kmer] -= 1

    # Add the last k-mer of the current window
    curr_kmer = text[i+L-k:i+L]
    kmer_dict[curr_kmer] = kmer_dict.get(curr_kmer,0) + 1

    # Check for k-mers above threshold and update clumps
    if kmer_dict[curr_kmer] >= t:
      clump_kmers.add(curr_kmer)

  return sorted(list(clump_kmers))

def minimum_skew(text: str) -> list[int]:
  skew_map = {'G': 1, 'C': -1, 'A': 0, 'T': 0} #contribution to skew of each base
  min_skew = float('inf')
  indices = []
  skew = 0
  for i, base in enumerate(text):
    skew += skew_map[base]
    if skew < min_skew:
      indices = [i+1]
      min_skew = skew
    elif skew == min_skew:
      indices.append(i+1)
  return indices


def hamming_distance(s1: str, s2: str) -> int:
  """
  Hamming Distance Problem: Compute the Hamming distance between two strings.
    Input: Two strings of equal length.
    Output: The Hamming distance between these strings.
  (extended to work with unequal length strings)
  """
  l1 = len(s1)
  l2 = len(s2)
  dist = 0
  for i in range(min(l1,l2)):
    dist += 1 if s1[i] != s2[i] else 0
  dist += max(l1,l2) - min(l1,l2)
  return dist

def pattern_match_approx(text: str,pattern: str,d: int) -> list[int]:
  """
  Approximate Pattern Matching Problem: Find all approximate occurrences of a pattern in a string.
    * Input: Strings Pattern and Text along with an integer d.
    * Output: All starting positions where Pattern appears as a substring of Text with at most d mismatches.
  """
  starts = []
  for i in range(len(text) - len(pattern) + 1):
    if hamming_distance(text[i:i+len(pattern)],pattern) <= d:
      starts.append(i)
  return starts

def pattern_count_approx(text: str, pattern: str, d: int) -> int:
  return len(pattern_match_approx(text,pattern,d))

def frequent_words_approx(text: str, k: int, d: int) -> dict[str, int]:
  """
  Frequent Words with Mismatches Problem: Find the most frequent k-mers with mismatches in a string.
    Input: A string Text as well as integers k and d.
    Output: All most frequent k-mers with up to d mismatches in Text.
  """
  def freq_map_kmers_approx(text, k, d):
    n = len(text)
    freqs = {}
    for i in range(n-k+1):
      kmer = text[i:i+k]
      freqs[kmer] = freqs.get(kmer, 0) + 1
    return freqs

#TODO: What is the runtime of this function? How can it be optimized?
def neighbors_lt(pattern: str, d: int) -> set[str]:
  """
  Neighbors: Find the d-neighborhood of a string (all dist < d).
    Input: A string Pattern and an integer d.
    Output: The collection of strings Neighbors(Pattern, d).
  """

  #T(n) = runtime for pattern of length n (fixed d)
  #H(n) = number of neighbors for length n (fixed d)
  #T(n) = H(n-1)*(n-1) + T(n-1) 
  #T(n) = H(n-1)*(n-1) + H(n-2)(n-2) + ...

  if d == 0:
    return [pattern]
  if len(pattern) == 1:
    return ['A', 'T', 'C', 'G']
  suffix_nbrs = neighbors_lt(pattern[1:], d) 
  nbrs = set([pattern])
  for snbr in suffix_nbrs:
    if hamming_distance(snbr, pattern[1:]) < d:
      for b in ['A', 'T', 'C', 'G']:
        nbrs.add(b + snbr)
    else:
      nbrs.add(pattern[0] + snbr)
  return nbrs

def neighbor_lt_complement(pattern: str, d: int) -> set[str]:
  nbrs = neighbors_lt(pattern, d)
  rcnbrs = neighbors_lt(reverse_complement(pattern),d)
  return set.union(nbrs,rcnbrs)

def frequent_words_with_mismatches(text: str, k: int, d: int) -> Tuple[list[str],int]:
  """
  Frequent Words with Mismatches Problem.
    Input: A string Text as well as integers k and d. (You may assume k ≤ 12 and d ≤ 3.)
    Output: All most frequent k-mers with up to d mismatches in Text.
  """
  freq_map = {}
  n = len(text)
  for i in range(n-k+1):
    pattern = text[i:i+k]
    nbrs = neighbors_lt(pattern, d)
    for nbr in nbrs:
      freq_map[nbr] = freq_map.get(nbr,0) + 1
  max_freq = max(freq_map.values())
  max_freq_kmers = [kmer for kmer in freq_map if freq_map[kmer] == max_freq]
  return max_freq_kmers, max_freq
    
def frequent_words_with_mismatches_complements(text: str, k: int, d: int, debug=False) -> Tuple[list[str],int]:
    """
    Find the most frequent k-mers (with mismatches and reverse complements) in a DNA string.
    O(4^k * (k + n))
    """
    kmers = [''.join(x) for x in itertools.product('ATGC', repeat=k)]
    counts = {}
    for kmer in kmers:
        count_pattern = pattern_count_approx(text, kmer, d)
        count_rc_pattern = pattern_count_approx(text, reverse_complement(kmer), d)
        total_count = count_pattern + count_rc_pattern
        counts[kmer] = total_count

    max_count = max(counts.values())
    max_freq_kmers = [kmer for kmer, count in counts.items() if count == max_count]

    if not debug:
      return max_freq_kmers
    else:
      return (max_freq_kmers, max_count)

# Does NOT work in all cases
# def optimized_freq(text, k, d, debug=False):
#     """
#     Find the most frequent k-mers (with mismatches and reverse complements) in a DNA string using an optimized approach.
#     """
#     counts = {}
#     for i in range(len(text) - k + 1):
#         pattern = text[i:i + k]
#         neighbors = neighbors_lt(pattern, d)
#         for neighbor in neighbors:
#             count_pattern = pattern_count_approx(text, neighbor, d)
#             count_rc_pattern = pattern_count_approx(text, reverse_complement(neighbor), d)
#             total_count = count_pattern + count_rc_pattern
#             counts[neighbor] = total_count

#     max_count = max(counts.values())
#     max_freq_kmers = [kmer for kmer, count in counts.items() if count == max_count]
#     if not debug:
#       return max_freq_kmers
#     else:
#       return (max_freq_kmers, max_count)

def canonicalize_word(word: str) -> str:
  """Picks a canonical repr. between a word and its reverse complement"""
  return min(word, reverse_complement(word))

def canonicalize_freq_map(map: dict[str,int]) -> dict[str,int]:
  for key,val in map.items():
    revc = reverse_complement(key)
    if val == -1 or map[revc] == -1:
      continue
    
    canon = canonicalize_word(key)
    other = reverse_complement(canon)
    map[canon] += map[other]
    map[other] = -1

  for key, val in list(map.items()):
    if val == -1:
      del map[key]
  return map

def gc_skew_iter(genome: str) -> Iterator[int]:
  """Yields the #G-#C skew at each position as an iterator"""
  print(f"genome: {genome}")
  skew_map = {'G': 1, 'C': -1, 'A': 0, 'T': 0} #contribution to skew of each base
  skews = []
  curr = 0
  for char in genome:
    curr += skew_map[char]
    skews.append(curr)
    yield curr

#each string has n-k kmers
#each kmer has sum( (k choose i) * 3^i ) d-nbrs ~= 4^d
#for each nbr, check all strings
#for each string,nbr, pattern_count takes O(s*k) time s=length of string
#runtime = O(n * 4^d * s * k)
def motif_enumerate_bruteforce(strings, k, d):
  motifs = set()
  for string in strings:
    n = len(string)
    for i in range(n-k+1):
      pattern = string[i:i+k]
      dnbrs = neighbors_lt(pattern, d)
      for approx_pattern in dnbrs:
        appears_all = all([pattern_count_approx(string2,approx_pattern,d) > 0 for string2 in strings])
        if appears_all:
          motifs.add(approx_pattern)
  return list(motifs)

def profile_matrix_as_dataframe(matrix: ndarray) -> pd.DataFrame:
  """The rows of matrix must be in order of BASES - A,C,G,T"""
  assert(matrix.shape[0] == 4)
  return pd.DataFrame(matrix, index=constants.BASES)

def count_motif_matrix(motifs: ndarray, pseudo_counts=False) -> pd.DataFrame:
  """Count the number of bases at each position across the given motifs
  Input: motifs is a 4xN ndarray, pseudo_counts will add 1 to each count for non-zero probabilities
  """
  count_matrix = (
    np.ones((4, motifs.shape[1]), dtype=int) if pseudo_counts 
    else np.zeros((4, motifs.shape[1]), dtype=int)
  )
  # Iterate over each column of the motif matrix and count the occurrences of each nucleotide
  for j in range(motifs.shape[1]):
    for i, nucleotide in enumerate(constants.BASES):
        count_matrix[i, j] += np.sum(motifs[:, j] == nucleotide)
  return count_matrix

def profile_motif_matrix(motifs: ndarray, pseudo_counts=False) -> pd.DataFrame:
  count_matrix = count_motif_matrix(motifs, pseudo_counts)
  prob_matrix = count_matrix / np.sum(count_matrix, axis=0)
  labeled_matrix = pd.DataFrame(prob_matrix, index=constants.BASES)
  return labeled_matrix

def score_motif_profile_entropy(profile: ndarray) -> float:
  for i in range(profile.shape[0]):
    for j in range(profile.shape[1]):
      profile[i, j] = 0 if profile[i,j] == 0 else -1 * profile[i, j] * math.log(profile[i,j], 2)
  sum = np.sum(profile[:,:])
  return sum

def score_motif_counts(counts: pd.DataFrame, pseudo_counts=True) -> int:
  max_counts = np.max(counts, axis=0)
  col_sums = np.sum(counts, axis=0)
  col_scores = col_sums - max_counts
  total = np.sum(col_scores)
  return int(total) #convert numpy int to int for json serialization

def median_strings(texts, k):
  """Computes all median strings
Input: An integer k, followed by a space-separated collection of strings Dna.
Output: A k-mer Pattern that minimizes d(Pattern, Dna) among all possible choices of k-mers.
  """
  all_kmers = [''.join(x) for x in itertools.product(constants.BASES, repeat=k)]
  min_d, best_kmers = float('inf'), []
  for kmer in all_kmers:
    d = 0
    for text in texts:
      patterns = [text[i:i+k] for i in range(len(text)-k+1)]
      dist = min([hamming_distance(kmer,pattern) for pattern in patterns])
      d += dist
    if d < min_d:
      min_d, best_kmers = d, [kmer]
    elif d == min_d:
      best_kmers.append(kmer)
  return sorted(best_kmers)

def profile_most_probable_kmer(text: str, profile_df: pd.DataFrame, k: int):
  """Profile-most Probable k-mer Problem: Find a Profile-most probable k-mer in a string.
  Ties are broken by returning the first most probable k-mer
    Input: A string text, an integer k, and a 4 × k dataframe profile_df.
    Output: A Profile-most probable k-mer in Text.
  """
  n = len(text)
  best_prob,best_kmer = 0, text[:k]
  profile_matrix = profile_df.values
  locs = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
  for i in range(n-k+1):
    pattern = text[i:i+k]
    prob_list = [profile_matrix[locs[c]][pi] for (pi,c) in enumerate(pattern)]
    prob = np.prod(prob_list)
    if prob > best_prob:
      best_prob,best_kmer = prob,pattern
  return best_kmer

def greedy_motif_search(texts: list[str],k: int, pseudo_counts=True) -> ndarray:
  """Greedy Motif Search
    Input: Integers k and t, followed by a space-separated collection of strings Dna.
    Output: A collection of strings BestMotifs resulting from applying GreedyMotifSearch(Dna, k, t). If at any step you find more than one Profile-most probable k-mer in a given string, use the one occurring first.
  """
  t,n = len(texts),len(texts[0])
  best_motifs, best_score = np.array([list(seq[:k]) for seq in texts]), float('inf')
  for motif in [texts[0][i:i+k] for i in range(n-k+1)]:
    motifs = np.array([list(motif)])
    for j in range(1,t):
      profile = profile_motif_matrix(motifs,pseudo_counts) 
      kmers = np.array(list(profile_most_probable_kmer(texts[j], profile, k)))
      motifs = np.vstack((motifs, kmers))
    if score_motif_counts(count_motif_matrix(motifs)) < best_score:
      best_motifs = motifs
      best_score = score_motif_counts(count_motif_matrix(motifs))
  
  best_motifs_1d = [''.join(row) for row in best_motifs]
  return best_motifs_1d, best_score

def randomized_motif_search(texts, k, pseudo_counts=True, iterations=1000, debug=False):
  t,n = len(texts), len(texts[0])
  best_motifs, best_score = None, float('inf')
  for i in range(iterations):
    if debug and i%50==0: print_sep(f"Iteration {i}")
    motifs = []
    for seq in texts:
      start = random.randint(0,n-k) #N=10, k=5 -> max start = 5
      kmer = list(seq[start:start+k])
      motifs.append(kmer)
    motifs = np.array(motifs)
    current_score = score_motif_counts(count_motif_matrix(motifs))
    if debug and i%50 == 0: 
      print(f"Chose collection of motifs with score {current_score}:")
      print_highlight_motifs(texts, [''.join(kmer) for kmer in motifs], color="RED")
    while True:
      profile = profile_motif_matrix(motifs, pseudo_counts)
      new_motifs = np.array([list(profile_most_probable_kmer(text, profile, k)) for text in texts])
      new_score = score_motif_counts(count_motif_matrix(new_motifs))
      if new_score < current_score:
        motifs = new_motifs
        current_score = new_score
      else:
        break
    if debug and i%50 == 0:
      print_sep()
      print(f"Iterated to improve motifs with score {current_score}")
      print_highlight_motifs(texts, [''.join(kmer) for kmer in motifs], color="RED")
    if current_score < best_score:
      best_score = current_score
      best_motifs = motifs
  best_motifs_1d = [''.join(row) for row in best_motifs]
  return best_motifs_1d, best_score

def weighted_die(weights: Iterable[float]):
  return random.choices(range(len(weights)), weights=weights)[0]

def gibbs_sampling_motif_search(texts: Iterable[str], k: int, iters: int, pseudo_counts=True):
  t,n = len(texts), len(texts[0])
  motifs = []
  for seq in texts:
    start = random.randint(0,n-k)
    kmer = list(seq[start:start+k])
    motifs.append(kmer)
  motifs = np.array(motifs)
  best_motifs = motifs
  curr_score = score_motif_counts(count_motif_matrix(motifs))
  for i in range(iters):
    remove = random.randint(0,t-1)
    removed_motifs = np.delete(motifs, remove, axis=0)
    profile = profile_motif_matrix(removed_motifs, pseudo_counts)
    kmers = [texts[remove][i:i+k] for i in range(n-k+1)]
    kmer_probs = []
    for kmer in kmers:
      locs = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
      prob_list = [profile.values[locs[c]][pi] for (pi,c) in enumerate(kmer)]
      prob = np.prod(prob_list)
      kmer_probs.append((kmer,prob))
    roll = weighted_die([t[1] for t in kmer_probs])
    new_motifs = np.vstack((motifs[:remove], np.array(list(kmers[roll])), motifs[remove+1:]))
    new_score = score_motif_counts(count_motif_matrix(new_motifs))
    motifs = new_motifs
    if new_score < curr_score:
      best_motifs = new_motifs
      curr_score = new_score
  best_motifs_1d = [''.join(row) for row in best_motifs]
  return (best_motifs_1d,curr_score)

## TESTS
def test_frequent_words_with_mismatches_complements():
  input = ('AAA',2,1) #compl = 'TTT'
  f = frequent_words_with_mismatches_complements(*input)
  assert sorted(f) == ['AT', 'TA']

  input = ('AGTCAGTC',4,2) #compl = 'GACTGACT'
  f = frequent_words_with_mismatches_complements(*input)
  assert sorted(f) == ['AATT', 'GGCC']

  input = ('AATTAATTGGTAGGTAGGTA',4,0) #compl = 'TACCTACCTACCAATTAATT'
  f = frequent_words_with_mismatches_complements(*input)
  assert sorted(f) == ['AATT']

  input = ('ATA',3,1) #compl = 'TAT'
  f = frequent_words_with_mismatches_complements(*input)
  assert sorted(f) == ['AAA','AAT','ACA','AGA','ATA','ATC',
                       'ATG','ATT','CAT','CTA','GAT','GTA',
                       'TAA','TAC','TAG','TAT','TCT','TGT',
                       'TTA','TTT']

  input = ('AAT',3,0) #compl = 'ATT'
  f = frequent_words_with_mismatches_complements(*input)
  assert sorted(f) == ['AAT','ATT']

  input = ('TAGCG',2,1) #compl = 'CGCTA'
  f = frequent_words_with_mismatches_complements(*input)
  assert sorted(f) == ['CA','CC','GG','TG']

  input = ('ACGTTGCATGTCGCATGATGCATGAGAGCT',4,1) #compl = 'AGCTCTCATGCATCATGCGACATGCAACGT'
  f = frequent_words_with_mismatches_complements(*input)
  assert sorted(f) == ['ACAT','ATGT']

def test_hamming_distance():
  assert hamming_distance('ACT','AGT') == 1
  assert hamming_distance('ACT','AG') == 2
  assert hamming_distance('ACGT','ACG') == 1
  assert hamming_distance('ACT','CAT') == 2

def test_motif_score():
  counts = np.array([
    [5,3,2,4,1],
    [1,2,3,5,3],
    [4,7,8,2,1],
    [4,2,1,3,9]
  ])
  assert(score_motif_counts(counts) == 36)

  counts = np.array([
    [1,2,3,4],
    [1,2,3,4],
    [1,2,3,4]
  ])
  assert(score_motif_counts(counts) == 2*(1+2+3+4))

  counts = np.array([
    [5,5,0,0],
    [0,0,5,0],
    [0,0,0,5],
  ])
  assert(score_motif_counts(counts) == 0)

         
def test_motif_enumerate():
  assert(
    sorted(motif_enumerate_bruteforce(['ATTTGGC','TGCCTTA','CGGTATC', 'GAAAATT'],k=3,d=1)) ==
    ['ATA','ATT','GTT','TTT']
  )

def test_median_string():
  soln = median_strings(['AAATTGACGCAT','GACGACCACGTT','CGTCAGCGCCTG','GCTGAGCACCGG','AGTTCGGGACAG'], k=3)
  assert(soln == ['GAC'])

  soln = median_strings(['ACGT','ACGT','ACGT'], k=3)
  assert(soln == ['ACG', 'CGT'])

  soln = median_strings(['ATA','ACA','AGA','AAT','AAC'], k=3)
  assert(soln == ['AAA'])

  soln = median_strings(['AAG','AAT'], k=3)
  assert (soln == ['AAG', 'AAT'])

  soln = median_strings(['ATTTGGC','TGCCTTA','CGGTATC', 'GAAAATT'], k=3)
  assert (soln == ['ATT'])

def test_profile_most_probable_kmer():
  text = 'ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT'
  k = 5
  profile_matrix = np.array([
    [0.2,0.2,0.3,0.2,0.3], #A
    [0.4,0.3,0.1,0.5,0.1], #C
    [0.3,0.3,0.5,0.2,0.4], #G
    [0.1,0.2,0.1,0.1,0.2], #T
  ])
  profile_df = profile_matrix_as_dataframe(profile_matrix)
  assert (profile_most_probable_kmer(text,profile_df,k) == 'CCGAG')

def test_motif_search():
  input = (['GGCGTTCAGGCA','AAGAATCAGTCA','CAAGGAGTTCGC','CACGTCAATCAC','CAATAATATTCG'],3)
  print(f"k={input[1]}-Motif search on {input[0]}")
  gsoln = greedy_motif_search(*input,pseudo_counts=False)
  print(f"\tgreedy soln = {gsoln}")
  assert (list(gsoln[0]) == ['CAG','CAG','CAA','CAA','CAA'])

  rsoln = randomized_motif_search(*input,pseudo_counts=False)
  print(f"\trandomized soln after 1000 iterations: {rsoln}")
  assert (rsoln[1] <= gsoln[1]) #TODO: not deterministic

  gibbs = gibbs_sampling_motif_search(*input, iters=500)
  print(f"\tgibbs soln after 500 iterations: {gibbs}")

  input = (['GGCGTTCAGGCA','AAGAATCAGTCA','CAAGGAGTTCGC','CACGTCAATCAC','CAATAATATTCG'],3)
  print(f"k={input[1]}-Motif search on {input[0]}")
  gsoln = greedy_motif_search(*input, pseudo_counts=True)
  print(f"\tgreedy soln = {gsoln}")
  assert (list(gsoln[0]) == ['TTC','ATC','TTC','ATC','TTC'])

  rsoln = randomized_motif_search(*input, pseudo_counts=True)
  print(f"\trandomized soln after 1000 iterations: {rsoln}")
  assert (rsoln[1] <= gsoln[1]) #TODO: not deterministic

  input = (['CGCCCCTCTCGGGGGTGTTCAGTAAACGGCCA','GGGCGAGGTATGTGTAAGTGCCAAGGTGCCAG','TAGTACCGAGACCGAAAGAAGTATACAGGCGT','TAGATCAAGTTTCAGGTGCACGTCGGTGAACC','AATCCACCAGCTCCACGTGCAATGTTGGCCTA'], 8)
  print(f"k={input[1]}-motif search on {input[0]}")
  soln = randomized_motif_search(*input)
  print(soln)

  gibbs = gibbs_sampling_motif_search(*input, iters=500)
  print(f"\tGibbs sampling soln after 500 iters: {gibbs}")

def test_weighted_die():
  num_rolls = 100000
  wts = [1,1,1,10]
  probs = [1/13,1/13,1/13,10/13]
  rolls = [weighted_die(wts) for i in range(num_rolls)]
  #print(rolls)
  counts = [rolls.count(i) for i in range(4)]
  fracns = [count/num_rolls for count in counts]
  print(probs)
  print(fracns)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    exit_code = pytest.main(["-s", sys.argv[1]]) #-s to not suppress prints
  else:
    exit_code = pytest.main(["-s",__file__]) #-s to not suppress prints
  sys.exit(exit_code)