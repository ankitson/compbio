import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import constants
from lib import gc_skew_iter

def get_counts_ecoli(nucleotide):
  if nucleotide not in ['A', 'T', 'G', 'C']:
      raise ValueError(f"Invalid nucleotide {nucleotide}")
  
  NUM_FRAGMENTS = 46
  with open(constants.DATASETS['e_coli']) as f: ecoli = f.read().strip()

  npecoli = np.array(list(ecoli))

  fragments = np.array_split(npecoli,NUM_FRAGMENTS)
  fragments_untyp = np.array(fragments, dtype=object)
  fragments = np.roll(fragments_untyp, -16, axis=0)
  counts = [np.count_nonzero(fragment == nucleotide) for fragment in fragments]
  return fragments, counts

#Graph methods should return a tuple of a figure, and a markdown description of the graph
def graph_counts_raw(nucleotide):
  fragments, counts = get_counts_ecoli(nucleotide)
  num_fragments = len(counts)
  fig = px.bar(x=list(range(num_fragments)), y=counts)
  descr = f"""
    ## These are the raw counts of the number of {nucleotide}'s in each fragment. 
    There are {num_fragments} fragments, of size {len(fragments[-1])}-{len(fragments[0])} each"""
  return (fig,descr)

def graph_counts_pct(nucleotide):
  fragments, counts = get_counts_ecoli(nucleotide)
  pct_counts = [count/len(fragments[0]) * 100 for count in counts]
  num_fragments = len(counts)
  fig = px.bar(x=list(range(num_fragments)), y=pct_counts)
  fig.update_layout(yaxis_range=[20, 30], barmode='relative', bargap=0.1, bargroupgap=0.1)
  
  descr = f"""
    ## These are the percentage of {nucleotide}'s in each fragment. 
    There are {num_fragments} fragments, of size {len(fragments[-1])}-{len(fragments[0])} each"""
  return (fig,descr)

#This is called a bidirectional bar chart
def graph_counts_pct_shifted(nucleotide, shift_base=25):
  fragments, counts = get_counts_ecoli(nucleotide)

  pct_counts = [count/len(fragments[0]) * 100 for count in counts]
  pct_counts_shifted = [pct - shift_base for pct in pct_counts]
  num_fragments = len(counts)

  fig = go.Figure()

  fig.add_trace(go.Bar(
    base=shift_base,
    y=pct_counts_shifted,
    x=list(range(num_fragments)),
    orientation='v',
  ))

  fig.update_layout(
      barmode='relative',
      title=f'Variation in frequency of {nucleotide} with position along genome (E. coli)',
      yaxis=dict(title=f'Frequency of {nucleotide} (%)', range=(shift_base-5,shift_base+5)),
      xaxis=dict(title='Chunk', tickvals=np.linspace(1,num_fragments,10)),
  )

  # MUST USE <img .. /> instead of <img..></img>
  # MUST USE ../static/.. for static paths
  descr = f"""These are the percentage of {nucleotide}'s in each fragment. 
There are {num_fragments} fragments, of size {len(fragments[-1])}-{len(fragments[0])} each.
    """
  
  img = ""
  if nucleotide == 'C':
    img = """This graph should roughly match up with the below graph from [here](https://cogniterra.org/lesson/30277/step/1?unit=22352) <br/>
    <img src='../static/ecoli_cytosine_frequency.png' width='750' height='495'/>"""
  elif nucleotide == 'G':
    img = """This graph should roughly match up with the below graph from [here](https://cogniterra.org/lesson/30277/step/1?unit=22352) <br/>
    <img src='../static/ecoli_guanine_frequency.png' width='750' height='495'/>"""
  descr += img

  return (fig, descr)

def graph_diff_counts_pct(b1,b2):
  fragments1, counts1 = get_counts_ecoli(b1)
  fragments2, counts2 = get_counts_ecoli(b2)

  pct_counts1 = [count/len(fragments1[0]) * 100 for count in counts1]
  pct_counts2 = [count/len(fragments2[0]) * 100 for count in counts2]
  pct_diff = [pct_counts1[i] - pct_counts2[i] for i in range(len(counts1))]
  num_fragments = len(counts1)

  fig = go.Figure()

  fig.add_trace(go.Bar(
    y=pct_diff,
    x=list(range(num_fragments)),
    orientation='v',
  ))

  fig.update_layout(
      barmode='relative',
      yaxis=dict(title=f'% frequency of {b1} - % frequency of {b2}', range=(-5,5)),
      xaxis=dict(title='Chunk', tickvals=np.linspace(1,num_fragments,10)),
  )


  # MUST USE <img .. /> instead of <img..></img>
  # MUST USE ../static/.. for static paths
  descr = f"""This is the difference between the % of {b1} and the % of {b2} in each fragment.
  There are {num_fragments} fragments, of size {len(fragments1[-1])}-{len(fragments1[0])} each.
  """
  
  img = ""
  if b1 == 'G' and b2 == 'C':
    img = """This graph should roughly match up with the below graph from [here](https://cogniterra.org/lesson/30277/step/3?unit=22352) <br/>
    <img src='../static/ecoli_frequency_difference.png' width='750' height='495'/>"""
  descr += img

  return (fig, descr)

def graph_skew_diagram(genome_dataset, sample_freq=100):
  skewg = gc_skew_iter(constants.dataset(genome_dataset))
  # Dont plot every point, sample uniformly
  skew_pts = []
  for i, val in enumerate(skewg):
    if i%sample_freq == 0:
      skew_pts.append(val)

  fig = go.Figure()
  fig.add_trace(go.Scatter(
    x=sample_freq * np.arange(0, len(skew_pts)),
    y=skew_pts,
    mode='lines',
    name='Skew',
    line=dict(color='blue')
  ))
  fig.update_layout(
    title=f'Skew Diagram for {genome_dataset}',
    xaxis=dict(title='Position'),
    yaxis=dict(title='Skew'),
  )
  descr = """This is the skew diagram, showing the cumulative `(# of G's - # of C's)` along the positions of the genome.
  Since the difference is negative on the reverse half-strand and positive on the forward half-strand, the **minimum** corresponds to the position of *Ori* and the **maximum** corresponds to the position of *Ter*
  """
  return (fig, descr)