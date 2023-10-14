from typing import Iterator, Iterable

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

def print_highlight(str: str, highlight: Iterable, color="BOLD"):
  for h in highlight:
    str = str.replace(h, c("BOLD", h))
  print(str)

def print_highlight_motifs(motifs: Iterable, highlights: Iterable, color="BOLD"):
  for (motif,highlight) in zip(motifs,highlights):
    motif = motif.replace(highlight, c(color, highlight))
    print(motif)
  