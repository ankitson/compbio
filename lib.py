import itertools
from typing import Iterable, Iterator, Tuple
import pytest

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
  compls = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
  return text.translate(str.maketrans(compls))

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

## FILE IO
def write_temp(inp: Iterator) -> None:
  out = open('temp.txt','w')
  if hasattr(inp, '__iter__'):
    text = format_iter(inp)
  else:
    text = str(inp)
  out.write(text)
  print("written to file temp.txt")
  return out.close()

## CONSOLE IO
def c(color: str, text: str) -> str:
  color_dict = {
    "PURPLE": "\033[95m",
    "CYAN": "\033[96m",
    "DARKCYAN": "\033[36m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m"
  }
  
  for k, v in color_dict.items():
    shortk = k.lower()[0:1]
    if shortk == color or k == color:
      return v + text + color_dict["END"]

def print_sep(text:str=None) -> None:
  SEP_LEN = 100
  if text:
    num_char = len(text)
    num_spc = SEP_LEN - num_char
    print(c("RED","-"*(num_spc//2)) + c("BLUE",text) + c("RED","-"*(num_spc//2)))
  else:
    print(c("RED","-"*100))

def format_iter(l: Iterator) -> str:
  return ' '.join([str(x) for x in l])

def print_iter(l: Iterator) -> None:
  print(format_iter(l))

def print_highlight(str: str, highlight: Iterable):
  for h in highlight:
    str = str.replace(h, c("BOLD", h))
  print(str)


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

  assert(
    sorted(motif_enumerate_bruteforce(['ATTTGGC','TGCCTTA','CGGTATC', 'GAAAATT'],k=3,d=1)) ==
    ['ATA','ATT','GTT','TTT']
  )
  
  print("all assertions passed!")

if __name__ == '__main__':
  pytest.main(["-s", __file__]) #-s to not suppress prints