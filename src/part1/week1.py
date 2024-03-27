import pytest
from lib import *
from util import *
import logging
import constants
  
import zipfile
import os

def parse_input(text):
  lines = [l for l in text.splitlines() if len(l) > 0]
  parsed = []
  for line in lines:
    if line[0].isdigit() or line[0] == ' ':
      nums = [int(x) for x in line.split()]
      if len(nums) == 1:
        parsed.append(nums[0])
      else:
        parsed.append(nums)
    elif line[0].isalpha():
      parsed.append(line)
    else:
      raise Exception("unnown")
  return parsed

def run_test(input_path, function_to_test, inp_transform=lambda t: t):
  input_folder = os.path.join(input_path, 'inputs')
  output_folder = os.path.join(input_path, 'outputs')
      
  input_files = [f for f in os.listdir(input_folder) if f.startswith('input_') and f.endswith('.txt')]
      
  for input_file in input_files:
    with open(os.path.join(input_folder, input_file), 'r') as infile:
      input_data = infile.read()  # Assuming the function takes the entire file content as input
      parsed = parse_input(input_data)
      transform = inp_transform(parsed)
      # Run the function and get the output
      logging.debug(f"Parsed input = {transform}")
      result = function_to_test(*transform)

      # TODO: The expected output can be unsorted, so compares fail
      # So write a real parser and unparser pair to go from python <-> cogniterra format
      # and compare outputs semantically

      # Construct corresponding output file name
      output_file = input_file.replace('input_', 'output_')
      with open(os.path.join(output_folder, output_file), 'r') as outfile:
        expected_output = outfile.read()

      parsed_output = parse_input(expected_output)
      if hasattr(result, '__iter__') and not isinstance(parsed_output, str):
        parsed_output = sorted(parsed_output)
      
      print(f"PO = {parsed_output}")
      if hasattr(result, '__iter__') and not isinstance(result, str):
        result = sorted(result)
      print(f"RES = {result}")
      
      assert result == parsed_output 


      
      formatted_result = str(result)
      if type(result) == dict:
        raise Exception("dict output not supported yet")
      elif hasattr(result, '__iter__') and not isinstance(result, str):
        formatted_result = format_iter(sorted(result))
      
      #TODO 
      # Check if the function's output matches the expected output
        assert formatted_result == expected_output, f"Mismatch in file {input_file}\nExpected {expected_output}\nbut got {formatted_result}\non input {parsed}"    
  print(f"{function_to_test.__name__}: all tests passed!")
    
def test_week1():
  print_sep("""\nBioinformatics I: Week 1 - Where in the Genome Does Replication Begin?""")

  #1.2 - 5
  print_sep("""Implement pattern count
    Input: Strings Text and Pattern.
    Output: Count(Text, Pattern).""")
  assert(len(pattern_match("GCGCG", "GCG")) == 2)

  #1.2 - 12
  print_sep("""Frequent Words            
    Input: A string Text and an integer k.
    Output: All most frequent k-mers in Text.
  """)
  freq_words = frequent_words("ACGTTGCATGTCGCATGATGCATGAGAGCT",4)
  assert(sorted(freq_words) == ['CATG', 'GCAT'])
  run_test("../debug_datasets/FrequentWords", frequent_words)

  #1.3 - 2
  print_sep("""Reverse Complement            
    Input: A DNA string Pattern.
    Output: Patternrc , the reverse complement of Pattern.
  """)
  assert(reverse_complement('AAAACCCGGT') == 'ACCGGGTTTT')
  run_test("../debug_datasets/ReverseComplement", reverse_complement)

  #1.3 - 5
  print_sep("""Pattern Matching
    Input: Two strings, Pattern and Genome.
    Output: A collection of integers specifying all starting positions where Pattern appears as a substring of Genome.
  """)
  assert(pattern_match('GATATATGCATATACTT','ATAT') == [1,3,9])
  run_test("../debug_datasets/PatternMatching", pattern_match, inp_transform=lambda t: (t[1],t[0]))

  #1.3 - 6
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
  # text = 'GGGCGTGGAATAAATGATTGAGACTGTATGTCGCTAGGGGGGCCAAGTGAAGTACTACCGTAACATGAACGCCTGCTGTAGACGCTTGGGGAGTGTGTAAACTGATGCTTACTTAAGAACCGATCATTGCACTGGCGGTTCCACATGCTAGCTCCGCATAGACTCCTAGTTACATACCGCGTCTATCAAGTATATCAAGGTCTCCAGGTCCGGTCTGGTACAGTCACTACGGAGTTGGACGGGGACCTCCTGATGGCACCCGAGTTGATCGCAGACACGTCCTCGGACTCCCCACCACTAATCATACCCATCGTGAATCATTAGATGGGGGACGGTCAGGTCAGTGAAATGCGGATCCTTCCAAAATAGTGGAACAGTCCCTGAATGTTATCGGCCAGTAGTGACACCAGTTGTCCTTGTGGCGTGTTACATCTGGAATAATCTCCGTCTGACGTACGGCTCTTGACCCAGGACTTCCCCCCACAATCACGGAGATGAGTCCGCGACGCTTGATATGGTTGTTCCAGACCGCTGTTATCAGTGCTTGCATTTGCATAGGGCTTTGTATTCGTCAACATACTATCCATCCACATAAGTACTGGTACTGATTCAAGTTTGCATCCGAAGGGCGCGCATGAAAGGTAGCAGGCTTTGCTAGCTTGAAGCTAGCTTGAAGCTTGAGCGCACACATGCGGCATGCACGTGCTGTTCTCCTGTGGATGTCGGATTCGATAAGATCCTCGGAACGCATCTTTTTGTACGCCTCTTATTACCATAGACATGGACCTGGCATCCAGACGCAAACGAAGAGACGCAAACATGTGCCGCGATCGCCCGCTGTCGGGAGCGTTTCATAGGGATCAGTCCCAAAGATCTGCAGACAATCCGATCTTAATTTTAAGCACGTTGTGGTGGGCTGGAGGATGTATTCCCAGTGCTTCGGGCGGCGAAAAATCAATGCCGGTACAACCAATAAATAGAGCGAAACATCCGCGGCTGCGGCACACGTTAGCCTCGGCTAGGCGCCCGGGTACCGATGATTTTTTACACACACTTACACACACATGAGTGTGGTCGTGGTGTCCAACTCTGAGACCGGGTTATAGGGCCCCACCTGTCATTGTTACTTTCCGATTGTTCTGGACATGCGAGAACTTGTACGTCTCCGGGTCGGTACGATATGTGCCGGAGAAGAACGTCTCTCCTGCACCTTTAATGGTTACCCTGTTTTTTCCGAGACAATCTGAGGCGTGGGAGCGACCACCGTCCGCCCCCTGGGTTATATACGAGGGGTTAGGAAGCAGGAAGGGACGAGCCTACTGACCGCGAACGGCGGTCGCCTTTCCAGCATTGAAGGGATAGCGTTCGTCTTGCGTGACACTTAGCTCATTACCATATGGCGCTAGCGTGATCCGCAAGCCATCCCCGCTCATAGAGGACCGTCGAAAACCTCCCAATGAGACTCGAGGCCCTATCCCCAGCCGGGTAGTTCATCGCTTCAGCGATAGAGAAGTGATAGGCACAAACGACACATGAATCAGCTTTTAAAGCTAAGGTTTACTGTACTGTAAGACGTAGAACAAGTTATCCCTGTTTGTTGTCTTAACCCGCTATATGTTGTAGCTAAGTTCTGCCATACCACTTTGCCACGCTCTCATAGGAGCAAATCCAATCCGTCAATCCGTCGCCTCCGGTCCTTGAGTCTTGCTGCGCAGGAATCCGATATTGATTTGATTCTTGATTCAAAACTTCGGTAATTCTCATGGTTTGTACTCGGGGCGAGTGCAACACTAAGCTTTTAGAGTCGTTAGCAAATATGGTGATATTAAGGGACCCACGGGGGACGCATGGTCAGTCTCCTTGCGCCAGCAACTTGATCTTCCGGCGGACGGGCGGGAGCGGGTGCTAGTGTGTTCACATTTAACTTCCATCCAAAGAAGATCCTCCAAAGAAGTGTGAGCATACATAACCCCCCCCATTCCGGCCGCATTCCG'
  # ans = find_clumps(text, k=10, L=26, t=4)
  # print(ans)
  sys.exit(1)

  print_sep("Find how many 9-mers form (500,3) clumps in the E. Coli Genome (4.6ßMB!)")

  with open(constants.DATASETS['e_coli']) as f: ecoli_genome = f.read()
  ans = find_clumps(ecoli_genome, k=9, L=500, t=3)
  write_temp(' '.join(ans))
  print(len(ans))

  print_sep("Coursera Quiz 1")

  # Quiz 1
  s = 'TAAACGTGAGAGAAACGTGCTGATTACACTTGTTCGTGTGGTAT'
  print(frequent_words(s,3))

  s = 'AAACATAGGATCAAC'
  print(pattern_match(s,"AA"))


  print("all assertions passed!")

if __name__ == '__main__':
  pytest.main(["-s", __file__ + "::test_week1", "--log-cli-level=DEBUG"],) #-s to not suppress prints
