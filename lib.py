import itertools
import math
from typing import Iterable, Iterator, Tuple

import pytest
import numpy as np
import pandas as pd
from numpy import ndarray
import constants

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
    else:
      pass
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

def pattern_count_approx(text: str, pattern: str, d: int) -> list[int]:
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

def profile_motif_matrix(motifs: ndarray) -> pd.DataFrame:
  count_matrix = np.zeros((4, motifs.shape[1]), dtype=int)
  # Iterate over each column of the motif matrix and count the occurrences of each nucleotide
  for j in range(motifs.shape[1]):
    for i, nucleotide in enumerate(constants.BASES):
        count_matrix[i, j] = np.sum(motifs[:, j] == nucleotide)
  prob_matrix = count_matrix / np.sum(count_matrix, axis=0)
  labeled_matrix = pd.DataFrame(prob_matrix, index=constants.BASES)
  return labeled_matrix

def score_motif_profile_entropy(profile: ndarray) -> float:
  for i in range(profile.shape[0]):
    for j in range(profile.shape[1]):
      profile[i, j] = 0 if profile[i,j] == 0 else -1 * profile[i, j] * math.log(profile[i,j], 2)
  sum = np.sum(profile[:,:])
  return sum

def median_string(texts, k):
  """Computes the median string
Input: An integer k, followed by a space-separated collection of strings Dna.
Output: A k-mer Pattern that minimizes d(Pattern, Dna) among all possible choices of k-mers. (If there are multiple such strings Pattern, then you may return any one.)
  """
  all_kmers = [''.join(x) for x in itertools.product(constants.BASES, repeat=k)]
  min_d = float('inf')
  best_kmers = []
  for kmer in all_kmers:
    d = 0
    for text in texts:
      patterns = [text[i:i+k] for i in range(len(text)-k+1)]
      dist = min([hamming_distance(kmer,pattern) for pattern in patterns])
      d += dist
    if d < min_d:
      min_d = d
      best_kmers = [kmer]
    elif d == min_d:
      best_kmers.append(kmer)
  return best_kmers[0]

def profile_most_probable_kmer(text: str, profile_df: pd.DataFrame, k: int):
  """Profile-most Probable k-mer Problem: Find a Profile-most probable k-mer in a string.
    Input: A string text, an integer k, and a 4 × k dataframe profile_df.
    Output: A Profile-most probable k-mer in Text.
  """
  n = len(text)
  best_prob,best_kmer = 0, text[:k] #if all prob are 0 then any kmer is best
  for i in range(n-k+1):
    pattern = text[i:i+k]
    prob_list = [profile_df.loc[c,pi] for (pi,c) in enumerate(pattern)]
    prob = np.prod(prob_list)
    if prob > best_prob:
      best_prob,best_kmer = prob,pattern
  return best_kmer

def greedy_motif_search(texts: list[str],k: int,t: int) -> ndarray:
  """Greedy Motif Search
    Input: Integers k and t, followed by a space-separated collection of strings Dna.
    Output: A collection of strings BestMotifs resulting from applying GreedyMotifSearch(Dna, k, t). If at any step you find more than one Profile-most probable k-mer in a given string, use the one occurring first.
  """

  def score(motifs):
    matrix = np.zeros((len(constants.BASES), k), dtype=int)
    for kmer in motifs:
      for j in range(k):
        i = constants.BASES.index(kmer[j])
        matrix[i,j] += 1
    
    total = 0
    for j in range(k):
      m = 0
      for i in range(len(constants.BASES)):
        if m < matrix[i,j]:
          m = matrix[i,j]
      total += (len(constants.BASES)-m)
    return total

  n = len(texts[0])
  best_motifs = np.array([seq[:k] for seq in texts])
  for motif in [texts[0][i:i+k] for i in range(n-k+1)]:
    motifs = np.array([motif])
    for j in range(1,t):
      profile = profile_motif_matrix(np.array([list(row) for row in motifs])) 
      motifs = np.append(motifs, profile_most_probable_kmer(texts[j], profile, k))
    if score(motifs) < score(best_motifs):
      best_motifs = motifs
  return best_motifs

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

def test_motif_enumerate():
  assert(
    sorted(motif_enumerate_bruteforce(['ATTTGGC','TGCCTTA','CGGTATC', 'GAAAATT'],k=3,d=1)) ==
    ['ATA','ATT','GTT','TTT']
  )

def test_median_string():
  soln = median_string(['AAATTGACGCAT','GACGACCACGTT','CGTCAGCGCCTG','GCTGAGCACCGG','AGTTCGGGACAG'], k=3)
  assert(soln == 'ACG' or soln=='GAC')

  soln = median_string(['ACGT','ACGT','ACGT'], k=3)
  assert(soln == 'ACG' or soln=='CGT')

  soln = median_string(['ATA','ACA','AGA','AAT','AAC'], k=3)
  assert(soln == 'AAA')

  soln = median_string(['AAG','AAT'], k=3)
  assert (soln == 'AAG' or soln == 'AAT')

  soln = median_string(['ATTTGGC','TGCCTTA','CGGTATC', 'GAAAATT'], k=3)
  assert soln in ['ATA','ATT','GTT','TTT']

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

def test_greedy_motif_search():
  print()
  input = (['GGCGTTCAGGCA','AAGAATCAGTCA','CAAGGAGTTCGC','CACGTCAATCAC','CAATAATATTCG'],3,5)
  soln = greedy_motif_search(*input)
  print(soln)
  assert np.array_equal(soln, np.array(['CAG','CAG','CAA','CAA','CAA']))

if __name__ == '__main__':
  pytest.main(["-s", __file__]) #-s to not suppress prints
  print("all tests passed!")