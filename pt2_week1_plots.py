import plotly.graph_objects as go
import networkx as nx

import pt2_week1

def de_bruijn_graph_to_nx_graph(graph: dict):
  nx_graph = nx.DiGraph()
  for prefix, suffixes in graph.items():
    for suffix in suffixes:
      nx_graph.add_edge(prefix, suffix)

  # Layout the graph using spring layout
  pos = nx.spring_layout(nx_graph)
  
  # Add the 'pos' values to the nodes
  for node, position in pos.items():
    print(f"node: {node}")
    nx_graph.nodes[node]['label'] = node.split(':')[0]
    nx_graph.nodes[node]['pos'] = position
  
  return nx_graph

def de_bruijn_graph_vis(graph: dict):
  dbgraph = de_bruijn_graph_to_nx_graph(graph)
  print(f"Original graph:\n{graph}\nDe bruinjn:{dbgraph}\n")
  edge_x = []
  edge_y = []
  return nx_graph_vis(dbgraph)

def nx_graph_vis(G: nx.Graph):
  edge_x = []
  edge_y = []
  for edge in G.edges():
      x0, y0 = G.nodes[edge[0]]['pos']
      x1, y1 = G.nodes[edge[1]]['pos']
      edge_x.append(x0)
      edge_x.append(x1)
      edge_x.append(None)
      edge_y.append(y0)
      edge_y.append(y1)
      edge_y.append(None)

  edge_trace = go.Scatter(
      x=edge_x, y=edge_y,
      line=dict(width=0.5, color='#888'),
      hoverinfo='none',
      mode='lines')

  node_x = []
  node_y = []
  node_labels = []
  for node in G.nodes():
      x, y = G.nodes[node]['pos']
      node_x.append(x)
      node_y.append(y)
      node_labels.append(G.nodes[node]['label'])

  node_trace = go.Scatter(
      x=node_x, y=node_y,
      mode='markers+text',
      hoverinfo='text',
      text=node_labels,
      marker=dict(
          showscale=True,
          # colorscale options
          #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
          #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
          #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
          colorscale='YlGnBu',
          reversescale=True,
          color=[],
          #size=10,
          colorbar=dict(
              thickness=15,
              title='Node Connections',
              xanchor='left',
              titleside='right'
          ),
          line_width=2))
  node_adjacencies = []
  node_text = []
  for node, adjacencies in enumerate(G.adjacency()):
      node_adjacencies.append(len(adjacencies[1]))
      node_text.append('# of connections: '+str(len(adjacencies[1])))

  node_trace.marker.color = node_adjacencies
  node_trace.text = node_labels
  fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
  return fig

def sample_network_graph():
  G = nx.random_geometric_graph(200, 0.125)
  return nx_graph_vis(G)

def sample_debruijn_graph():
  input = ("AAGATTCTCTAAGA", 4)
  output = pt2_week1.de_bruijn_graph_from_string(*input)
  fig = de_bruijn_graph_vis(output)
  return (fig, "De Bruijn graph of 4-mers of AAGATTCTCTAAGA")