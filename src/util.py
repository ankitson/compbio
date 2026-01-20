import logging
import os
import sqlite3
import json

from typing import Dict, Iterator, Iterable

import constants

## DATABASE
def init_db():
  conn = sqlite3.connect('strings.db')
  conn.execute('''CREATE TABLE IF NOT EXISTS strings
               (id TEXT PRIMARY KEY,
               content TEXT NOT NULL)''')
  conn.commit()

def write_to_db(id: str, content):
  conn = sqlite3.connect('strings.db')
  conn.execute(f"INSERT OR REPLACE INTO strings (id, content) VALUES ('{id}', '{json.dumps({ 'id': id, 'content': content } )}')")
  conn.commit()

def read_from_db(id: str):
  conn = sqlite3.connect('strings.db')
  cursor = conn.execute(f"SELECT content FROM strings WHERE id = '{id}'")
  json_str = cursor.fetchone()[0]
  obj = json.loads(json_str)
  return obj['content']

## PARSING
def parse_graph(text: str):
  nodes = {}
  for line in text.splitlines():
    fro, tos = line.split(": ")
    fro = int(fro)
    tos = [int(to) for to in tos.split(" ")]
    nodes[fro] = tos
    for to in tos:
      if not to in nodes:
        nodes[to] = []
  return nodes

def parse_list(text:str, mapper=lambda x: x):
  l = text.strip().split(' ')
  return list(map(mapper, text.strip().split(' ')))

## OUTPUT
def format_iter(l: Iterator) -> str:
  return ' '.join([str(x) for x in l])

def format_dict(d: dict) -> str:
  lines = []
  for (k,v) in d.items():
    kstr = str(k)
    if hasattr(k, '__iter__') and not isinstance(k, str):
      kstr = format_iter(k)
    vstr = str(v)
    if hasattr(v, '__iter__') and not isinstance(v, str): 
      vstr = format_iter(v)
    line = f"{kstr}: {vstr}"
    lines.append(line)
  return '\n'.join(lines)

def dotviz_graph(graph: Dict):
  dotviz = "digraph {\n"
  for node, edges in graph.items():
    for edge in edges:
      dotviz += f"  {node} -> {edge};\n"
  dotviz += "}"
  return dotviz

## FILE IO
def write_temp(inp: Iterator) -> None:
  write_iter(inp, constants.TEMP_PATH)
  
def write_iter(inp: Iterator, outpath) -> None:
  out = open(outpath,'w')
  if type(inp) == dict:
    text = format_dict(inp)
  elif hasattr(inp, '__iter__') and not isinstance(inp, str):
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
  return text

def print_sep(text:str|None=None) -> None:
  SEP_LEN = 100
  lines = text.splitlines()
  if text:
    line1 = lines[0].strip()
    num_char = len(line1)
    num_spc = SEP_LEN - num_char
    print(c("RED","-"*(num_spc//2)) + c("BLUE",line1) + c("RED","-"*(num_spc//2)))
    for line in lines[1:]:
      print(c("BLUE", line))
  else:
    print(c("RED","-"*100))

def print_iter(l: Iterator) -> None:
  print(format_iter(l))
    
def print_highlight(str: str, highlight: Iterable, color="BOLD"):
  for h in highlight:
    str = str.replace(h, c(color, h))
  print(str)

def print_highlight_motifs(motifs: Iterable, highlights: Iterable, color="BOLD"):
  for (motif,highlight) in zip(motifs,highlights):
    motif = motif.replace(highlight, c(color, highlight))
    print(motif)

## COGNITERRA TEST UTILS 

def parse_atom(atom):
  if atom[0].isdigit():
    p = 0
    try:
      p = int(atom)
    except ValueError:
      p = float(atom)
    return p
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

def trunc(s):
  s = str(s)
  if len(s) > 100:
    return s[0:98] + ".."
  return s
  
def run_test(input_path, function_to_test, inp_transform=lambda t: t, out_transform=lambda t: t, exp_out_transform=lambda t: t):
  """Given the path to a folder containing the input and output files, and a function to test, 
  runs the function on each input file and compares the result to the corresponding output file."""
  input_folder = os.path.join(input_path, 'inputs')
  output_folder = os.path.join(input_path, 'outputs')
      
  input_files = sorted([f for f in os.listdir(input_folder) if f.startswith('input_') and f.endswith('.txt')])

  # logging.info(f"{function_to_test.__name__} on ({trunc(input)})")
  for input_file in input_files:
    with open(os.path.join(input_folder, input_file), 'r') as infile:
      input_data = infile.read()
      input = parse_input(input_data)
      transform = inp_transform(input)
      logging.debug(f"{function_to_test.__name__}: input = {trunc(transform)}")
      
      # logging.debug("Calling function with ")
      result = out_transform(function_to_test(*transform))
      logging.debug(f"{function_to_test.__name__}: result = {trunc(result)}")

      # Construct corresponding output file name
      output_file = input_file.replace('input_', 'output_')
      with open(os.path.join(output_folder, output_file), 'r') as outfile:
        expected_output = outfile.read()

      # unwrap
      parsed_output = parse_input(expected_output)
      parsed_output = exp_out_transform(parsed_output)
      while hasattr(result, '__iter__') and not isinstance(result, str) and len(result) == 1:
        result = result[0]
      while hasattr(parsed_output, '__iter__') and not isinstance(parsed_output, str) and len(parsed_output) == 1:
        parsed_output = parsed_output[0]

      # sort
      if hasattr(parsed_output, '__iter__') and not isinstance(parsed_output, str):
        parsed_output = sorted(parsed_output)
      if hasattr(result, '__iter__') and not isinstance(result, str):
        result = sorted(result)

      logging.debug(f"{function_to_test.__name__}: expect = {trunc(parsed_output)}")
      logging.debug(f"{function_to_test.__name__}: cleaned result = {trunc(result)}")

      if result != parsed_output:
        logging.info(f"{function_to_test.__name__}: ({trunc(input)}) expect {trunc(parsed_output)} but got {trunc(result)}")
      assert result == parsed_output, f"Mismatch in file {input_file}\nExpected {parsed_output}\nbut got {result}\non input {input}"
      
  print(f"{function_to_test.__name__}: all tests passed!")
    