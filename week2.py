import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def get_C_counts_ecoli():
  NUM_FRAGMENTS = 46
  ecoli = open('inputs/E_coli_genome.txt').read().strip()
  npecoli = np.array(list(ecoli))

  fragments = np.array_split(npecoli,NUM_FRAGMENTS)
  c_counts = [np.count_nonzero(fragment == 'C') for fragment in fragments]
  return fragments, c_counts

#Graph methods should return a tuple of a figure, and a markdown description of the graph
def graph_C_counts_raw():
  fragments, c_counts = get_C_counts_ecoli()
  num_fragments = len(c_counts)
  fig = px.bar(x=list(range(num_fragments)), y=c_counts)
  descr = f"""
    ## These are the raw counts of the number of C's in each fragment. 
    There are {num_fragments} fragments, of size {len(fragments[-1])}-{len(fragments[0])} each"""
  return (fig,descr)

def graph_C_counts_pct():
  fragments, c_counts = get_C_counts_ecoli()
  pct_c_counts = [count/len(fragments[0]) * 100 for count in c_counts]
  num_fragments = len(c_counts)
  fig = px.bar(x=list(range(num_fragments)), y=pct_c_counts)
  fig.update_layout(yaxis_range=[20, 30], barmode='relative', bargap=0.1, bargroupgap=0.1)
  
  descr = f"""
    ## These are the percentage of C nucleotides in each fragment. 
    There are {num_fragments} fragments, of size {len(fragments[-1])}-{len(fragments[0])} each"""
  return (fig,descr)

def graph_C_counts_pct_shifted():
  base = 25

  fragments, c_counts = get_C_counts_ecoli()
  pct_c_counts = [count/len(fragments[0]) * 100 for count in c_counts]
  pct_c_counts_shifted = [pct - base for pct in pct_c_counts]
  num_fragments = len(c_counts)

  fig = go.Figure()

  fig.add_trace(go.Bar(
    base=base,
    y=pct_c_counts_shifted,
    x=list(range(num_fragments)),
    orientation='v',
  ))

  fig.update_layout(
      barmode='relative',
      title='Variation in frequency of C nucleotide with position along genome (E. coli)',
      yaxis=dict(title='Frequency of C (%)', range=(20,30)),
      xaxis=dict(title='Chunk', tickvals=np.linspace(1,num_fragments,10)),
      width=850,
      height=595
  )

  # NOTE: MUST USE <img .. /> instead of <img..></img>
  descr = f"""## These are the percentage of C nucleotides in each fragment. 
There are {num_fragments} fragments, of size {len(fragments[-1])}-{len(fragments[0])} each.
This graph should roughly match up with the below graph from [here](https://cogniterra.org/lesson/30277/step/1?unit=22352) <br/>
<img src='http://bioinformaticsalgorithms.com/images/Replication/ecoli_cytosine_frequency.png' width='750' />
    """
  
  return (fig, descr)

def graph_test():
  pass