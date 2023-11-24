import os

from typing import Dict, Iterator, Iterable

import constants

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
  if hasattr(inp, '__iter__') and not isinstance(inp, str):
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
    
def print_highlight(str: str, highlight: Iterable, color="BOLD"):
  for h in highlight:
    str = str.replace(h, c("BOLD", h))
  print(str)

def print_highlight_motifs(motifs: Iterable, highlights: Iterable, color="BOLD"):
  for (motif,highlight) in zip(motifs,highlights):
    motif = motif.replace(highlight, c(color, highlight))
    print(motif)
  