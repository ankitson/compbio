from dash import Dash, html, dcc, callback, Output, Input
from week2 import graph_C_counts_pct, graph_C_counts_raw, graph_test, graph_C_counts_pct_shifted
import plotly.express as px

app = Dash(__name__)
server = app.server

figure_select = ["Example", "C Counts (Raw)", "C Counts (Pct)", "C Counts (Pct Base)", "Test"]

app.layout = html.Div([
  html.H1(children='Bioinformatics I', style={'textAlign':'center'}),
  dcc.Dropdown(figure_select, figure_select[3], id='dropdown-selection'),
  dcc.Graph(figure={}, id='graph-content'),
  dcc.Markdown(id='graph-description', style={'align':'center'}, dangerously_allow_html=True),
])

@callback(
  Output('graph-content', 'figure'),
  Output('graph-description', 'children'),
  Input('dropdown-selection', 'value')
)
def update_graph(value):
  if value == 'C Counts (Raw)':
    return graph_C_counts_raw()
  elif value == 'C Counts (Pct)':
    return graph_C_counts_pct()
  elif value == "C Counts (Pct Base)":
    a, b = graph_C_counts_pct_shifted()
    return (a,b) 
  elif value == "Test":
    return graph_test()
  else:
    return px.bar(x=[1,2,3],y=[1,2,3]), f"# This is an example"

if __name__ == '__main__':
  app.run(debug=True)