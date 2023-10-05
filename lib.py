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
def find_clumps(text, k, L, t):
  n = len(text)
  clump_kmers = set()
  for i in range(n-L+1):
    window = text[i:i+L]
    kmers = freq_map_kmers(window, k)
    kmers_above_t = [k for (k,v) in kmers.items() if v >= t]
    clump_kmers.update(kmers_above_t)
  return sorted(list(clump_kmers))

## FILE IO
def write_temp(text):
  out = open('output.txt','w')
  out.write(text)
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

def print_sep():
  print(c("RED","-"*100))

