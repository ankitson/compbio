import pytest
from lib import *
from util import *
import logging
import constants
import os

def parse_atom(atom):
  if atom[0].isdigit():
    return int(atom)
  elif atom[0].isalpha():
    return atom.strip()
  else:
    raise Exception("unknown atom")

def parse_line(line):
  atoms = [parse_atom(a) for a in line.split()]
  if len(atoms) == 1:
    return atoms[0]
  else:
    return atoms

def parse_input(text):
  lines = [l for l in text.splitlines() if len(l) > 0]
  parsed = []
  for line in lines:
    parsed.append(parse_line(line))
  # if len(parsed) == 1 and hasattr(parsed[0], '__iter__') and not isinstance(parsed[0], str):
  #   return parsed[0]
  return parsed

def run_test(input_path, function_to_test, inp_transform=lambda t: t):
  input_folder = os.path.join(input_path, 'inputs')
  output_folder = os.path.join(input_path, 'outputs')
      
  input_files = [f for f in os.listdir(input_folder) if f.startswith('input_') and f.endswith('.txt')]
      
  for input_file in input_files:
    with open(os.path.join(input_folder, input_file), 'r') as infile:
      input_data = infile.read()  # Assuming the function takes the entire file content as input
      input = parse_input(input_data)
      transform = inp_transform(input)
      logging.debug(f"Parsed input = {transform}")

      result = function_to_test(*transform)

      # Construct corresponding output file name
      output_file = input_file.replace('input_', 'output_')
      with open(os.path.join(output_folder, output_file), 'r') as outfile:
        expected_output = outfile.read()

      # unwrap
      parsed_output = parse_input(expected_output)
      if hasattr(result, '__iter__') and not isinstance(result, str) and len(result) == 1:
        result = result[0]
      if hasattr(parsed_output, '__iter__') and not isinstance(parsed_output, str) and len(parsed_output) == 1:
        parsed_output = parsed_output[0]

      # sort
      if hasattr(result, '__iter__') and not isinstance(parsed_output, str):
        parsed_output = sorted(parsed_output)
      if hasattr(result, '__iter__') and not isinstance(result, str):
        result = sorted(result)

      logging.debug(f"expected_output = {parsed_output}")
      logging.debug(f"output = {result}")
      
      assert result == parsed_output, f"Mismatch in file {input_file}\nExpected {parsed_output}\nbut got {result}\non input {input}"
  print(f"{function_to_test.__name__}: all tests passed!")
    
def test_week1():
  print_sep("""\nBioinformatics I: Week 1 - Where in the Genome Does Replication Begin?""")

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

if __name__ == '__main__':
  pytest.main(["-s", __file__ + "::test_week1", "--log-cli-level=INFO"],) #-s to not suppress prints
