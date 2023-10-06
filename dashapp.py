from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

NUM_FRAGMENTS = 46


ecoli = open('inputs/E_coli_genome.txt').read().strip()
npecoli = np.array(list(ecoli))

fragments = np.array_split(npecoli,NUM_FRAGMENTS)
c_counts = [np.count_nonzero(fragment == 'C') for fragment in fragments]

#fragment_size = len(ecoli) // NUM_FRAGMENTS
#ecoli_fragments = [ecoli[i:i+fragment_size] for i in range(0, len(ecoli), fragment_size)]
#c_counts = [fragment.count('C') for fragment in ecoli_fragments]
#print(c_counts)


fig = px.bar(x=list(range(NUM_FRAGMENTS)), y=c_counts)


#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
app = Dash(__name__)
server = app.server

app.layout = html.Div([
  html.H1(children='Bioinformatics I', style={'textAlign':'center'}),
  #dcc.Dropdown(df.country.unique(), 'ss', id='dropdown-selection'),
  #dcc.Graph(id='graph-content'),
  dcc.Graph(figure=fig, id='c-counts')
])

#@callback(
#  Output('graph-content', 'figure'),
#  Input('dropdown-selection', 'value')
#)
#def update_graph(value):
  #dff = df[df.country==value]
  #return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
  app.run(debug=True)