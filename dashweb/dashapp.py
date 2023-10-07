from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from week2_plots import graph_counts_pct, graph_counts_pct_shifted, graph_counts_raw, graph_test, graph_diff_counts_pct
import plotly.express as px

def init_dash(server):
  """Setup the dash app as child of main flask app"""
  dash_app = Dash(
    server=server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    #requests_pathname_prefix='/static/'    
  )
  dash_app.layout = build_layout()
  dash_app.title = "Bioinformatics Plots"
  init_callbacks(dash_app)

  return dash_app.server

def build_layout():
  #all available figures are here - not showing all.
  #figure_select = ["Example", "Counts (Raw)", "Counts (Pct)", "Counts (Pct Base)", "Diff Counts", "Test"]
  figure_select = ["Counts (Pct Base)", "Diff Counts", "Test"]
  return \
   dbc.Container([
      dbc.Row(html.H1(children='Bioinformatics I', style={'textAlign':'center'}),),
      dbc.Row([
        dbc.Col(dcc.Dropdown(options=figure_select, value=figure_select[1], id='dropdown-selection')),
        dbc.Col(dcc.RadioItems(options=["A","T","C","G"], value="C", id="nucleotide-selection",  inline=True)),
        dbc.Col(dcc.RadioItems(options=["A","T","C","G"], value="C", id="nucleotide-selection2",  inline=True)),
      ]),
      dbc.Row([
        dbc.Col([dcc.Markdown("## Plot", style={'textAlign':'center'}), dcc.Graph(figure={}, id='graph-content')],width=6),
        dbc.Col([dcc.Markdown("## Description", style={'textAlign':'center'}), dcc.Markdown(id='graph-description', style={'textAlign':'center'}, dangerously_allow_html=True)], width=6),
      ], className='g-0')
    ], fluid=True)

def init_callbacks(dash_app):
  @dash_app.callback(
    Output('graph-content', 'figure'),
    Output('graph-description', 'children'),
    Input('dropdown-selection', 'value'),
    Input("nucleotide-selection", 'value'),
    Input("nucleotide-selection2", 'value')
  )
  def update_graph(value, nvalue, nvalue2):
    if value == 'Counts (Raw)':
      (fig,descr) = graph_counts_raw(nucleotide=nvalue)
    elif value == 'Counts (Pct)':
      (fig,descr) = graph_counts_pct(nucleotide=nvalue)
    elif value == "Counts (Pct Base)":
      (fig,descr) = graph_counts_pct_shifted(nucleotide=nvalue)
    elif value == "Test":
      (fig,descr) = graph_test()
    elif value == "Diff Counts":
      (fig,descr) = graph_diff_counts_pct(nvalue, nvalue2)
    else:
      (fig,descr) = (px.bar(x=[1,2,3],y=[1,2,3]), """This is an example <br/>""" )
    
    fig.update_layout(height=559, margin=dict(l=0,r=0,b=0))
    return (fig, descr)