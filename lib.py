def freq_map_kmers(text, k):
  n = len(text)
  freqs = {}
  for i in range(n-k+1):
    kmer = text[i:i+k]
    freqs[kmer] = freqs.get(kmer, 0) + 1
  return freqs

#1.2 - 12
#output all most frequent k-mers in text
def frequent_words(text, k):
  freq_map = freq_map_kmers(text, k)
  max_freq = max(freq_map.values())
  freq_words = []
  for (kmer,freq) in freq_map.items():
    if freq == max_freq:
      freq_words.append(kmer)
  return freq_words

def reverse(text):
  return text[::-1]

def complement(text):
  compls = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
  return text.translate(str.maketrans(compls))

def reverse_complement(text):
  return complement(reverse(text))

def pattern_match(text,pattern):
  starts = []
  for i in range(len(text) - len(pattern) + 1):
    if text[i:i+len(pattern)] == pattern:
      starts.append(i)
  return starts

#Clump Finding Problem: Find patterns forming clumps in a string.
#  Input: A string Genome, and integers k, L, and t.
#  Output: All distinct k-mers forming (L, t)-clumps in Genome.
# Optimized version using sliding windows
def find_clumps(text, k, L, t):
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

def minimum_skew(text):
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


def hamming_distance(s1, s2):
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

def pattern_match_approx(text,pattern,d):
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

def pattern_count_approx(text, pattern, d):
  n = len(text)
  k = len(pattern)
  count = 0
  for i in range(n-k+1):
    window = text[i:i+k]
    if hamming_distance(window, pattern) <= d:
      count += 1
  return count


def frequent_words_approx(text, k, d):
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
def neighbors_lt(pattern, d):
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

def frequent_words_with_mismatches(text, k, d):
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
  return max_freq_kmers

def frequent_words_with_mismatches_complements(text, k, d):
  """
  Frequent Words with Mismatches and Reverse Complements Problem: Find the most frequent k-mers (with mismatches and reverse complements) in a string.
    Input: A DNA string Text as well as integers k and d.
    Output: All k-mers Pattern maximizing the sum Countd(Text, Pattern)+ Countd(Text, Patternrc) over all possible k-mers.
  """
  freq_map = {}
  n = len(text)
  for i in range(n-k+1):
    pattern = text[i:i+k]
    nbrs = neighbors_lt(pattern, d)
    for nbr in nbrs:
      freq_map[nbr] = freq_map.get(nbr,0) + 1
      nbrc = reverse_complement(nbr)
      freq_map[nbrc] = freq_map.get(nbrc,0) + 1

  max_freq = max(freq_map.values())
  max_freq_kmers = [kmer for kmer in freq_map if freq_map[kmer] == max_freq]
  return max_freq_kmers

def skew(genome):
  """
  """
  skew_map = {'G': 1, 'C': -1, 'A': 0, 'T': 0} #contribution to skew of each base
  skews = []
  curr = 0
  for char in genome:
    curr += skew_map[char]
    skews.append(curr)
    yield curr

## FILE IO
def write_temp(inp):
  out = open('temp.txt','w')
  if hasattr(inp, '__iter__'):
    text = format_iter(inp)
  else:
    text = str(inp)
  out.write(text)
  print("written to file temp.txt")
  return out.close()

## CONSOLE IO
def c(color, text):
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

def print_sep(text=None):
  SEP_LEN = 100
  if text:
    num_char = len(text)
    num_spc = SEP_LEN - num_char
    print(c("RED","-"*(num_spc//2)) + c("BLUE",text) + c("RED","-"*(num_spc//2)))
  else:
    print(c("RED","-"*100))

def format_iter(l):
  return ' '.join([str(x) for x in l])

def print_iter(l):
  print(format_iter(l))
  