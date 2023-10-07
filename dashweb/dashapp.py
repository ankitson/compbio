#from flask import Flask, render_template
from dash import Dash, html, dcc, callback, Output, Input
from week2_plots import graph_counts_pct, graph_counts_pct_shifted, graph_counts_raw, graph_test
import plotly.express as px

def init_dash(server):
  dash_app = Dash(
    server=server,
    routes_pathname_prefix='/dash/',
    #external_stylesheets=[],
  )

  figure_select = ["Example", "Counts (Raw)", "Counts (Pct)", "Counts (Pct Base)", "Test"]
  dash_app.layout= html.Div([
    html.H1(children='Bioinformatics I', style={'textAlign':'center'}),
    dcc.Dropdown(figure_select, figure_select[3], id='dropdown-selection'),
    dcc.Dropdown(["A","T","C","G"], "C", id="nucleotide-selection"),
    dcc.Graph(figure={}, id='graph-content'),
    dcc.Markdown(id='graph-description', style={'align':'center'}, dangerously_allow_html=True),
  ])

  init_callbacks(dash_app)

  return dash_app.server

def init_callbacks(dash_app):
  @dash_app.callback(
    Output('graph-content', 'figure'),
    Output('graph-description', 'children'),
    Input('dropdown-selection', 'value'),
    Input("nucleotide-selection", 'value')
  )
  def update_graph(value, nvalue):
    if value == 'Counts (Raw)':
      return graph_counts_raw(nucleotide=nvalue)
    elif value == 'Counts (Pct)':
      return graph_counts_pct(nucleotide=nvalue)
    elif value == "Counts (Pct Base)":
      return graph_counts_pct_shifted(nucleotide=nvalue)
    elif value == "Test":
      return graph_test()
    else:
      return px.bar(x=[1,2,3],y=[1,2,3]), f"# This is an example" # @app.route('/')
