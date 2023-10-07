import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def get_counts_ecoli(nucleotide):
  if nucleotide not in ['A', 'T', 'G', 'C']:
      raise ValueError(f"Invalid nucleotide {nucleotide}")
  
  NUM_FRAGMENTS = 46
  ecoli = open('inputs/E_coli_genome.txt').read().strip()
  npecoli = np.array(list(ecoli))

  fragments = np.array_split(npecoli,NUM_FRAGMENTS)
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

  fragments, c_counts = get_counts_ecoli(nucleotide)
  npccount = np.roll(c_counts,-16) #,axis=0)

  pct_counts = [count/len(fragments[0]) * 100 for count in npccount]
  pct_counts_shifted = [pct - shift_base for pct in pct_counts]
  num_fragments = len(c_counts)

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
      width=850,
      height=495
  )

  # MUST USE <img .. /> instead of <img..></img>
  # MUST USE ../static/.. for static paths
  descr = f"""## These are the percentage of {nucleotide}'s in each fragment. 
There are {num_fragments} fragments, of size {len(fragments[-1])}-{len(fragments[0])} each.
    """
  
  img = ""
  if nucleotide == 'C':
    img = """This graph should roughly match up with the below graph from [here](https://cogniterra.org/lesson/30277/step/1?unit=22352) <br/>
    <img src='../static/ecoli_cytosine_frequency.png' width='750' height='495' />"""
  elif nucleotide == 'G':
    img = """This graph should roughly match up with the below graph from [here](https://cogniterra.org/lesson/30277/step/1?unit=22352) <br/>
    <img src='../static/ecoli_guanine_frequency.png' width='750' height='495' />"""
  
  descr += img

  return (fig, descr)

def graph_test():
  pass