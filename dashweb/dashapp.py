from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

import constants

from week2_plots import \
  graph_counts_pct, \
  graph_counts_pct_shifted, \
  graph_counts_raw, \
  graph_diff_counts_pct, \
  graph_skew_diagram
import pt2_week1
import constants

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
  figure_select = [plot.value for plot in constants.ENABLED_PLOTS]
  return \
   dbc.Container([
      dbc.Row(html.H1(children='Bioinformatics I', style={'textAlign':'center'}),),
      dbc.Row([
        dbc.Col(dcc.Dropdown(options=figure_select, value=figure_select[3], id='dropdown-selection')),
        dbc.Col(dbc.Stack([
          dcc.RadioItems(options=["A","T","C","G"], value="G", id="baseradio1",  inline=True),
          dcc.RadioItems(options=["A","T","C","G"], value="C", id="baseradio2",  inline=True)
        ]), width=2),
        dbc.Col(dcc.Dropdown(options=constants.DATASET_KEYS, value=constants.DATASET_KEYS[0], id="genomeselect"))
      ]),
      dbc.Row([
        dbc.Col([
          dcc.Markdown("## Plot", style={'textAlign':'center'}), 
          dcc.Graph(figure={}, id='graph-content', className='border-top border-start border-end border-primary')
        ],width=6),
        dbc.Col([
          dcc.Markdown("## Description", style={'textAlign':'center'}), 
          dcc.Markdown(
            id='graph-description', style={'textAlign':'center'}, 
            className='border-top border-secondary', dangerously_allow_html=True)
        ], width=6),
      ], className='g-0')
    ], fluid=True)

def init_callbacks(dash_app):
  @dash_app.callback(
    Output('graph-content', 'figure'),
    Output('graph-description', 'children'),
    Output('baseradio1', 'style'),
    Output('baseradio2', 'style'),
    Output("genomeselect", 'style'),
    Input('dropdown-selection', 'value'),
    Input("baseradio1", 'value'),
    Input("baseradio2", 'value'),
    Input("genomeselect", 'value')
  )
  def update_graph(value, nvalue, nvalue2, genome_dataset):
    STYLE_HIDDEN = { 'display' : 'none' } 
    STYLE_SHOW = { 'display' : 'block' }

    base_select_style = STYLE_SHOW
    base_select2_style = STYLE_HIDDEN
    genome_select_style = STYLE_HIDDEN

    if value == constants.Plots.COUNTS_RAW.value:
      (fig,descr) = graph_counts_raw(nucleotide=nvalue)
    elif value == constants.Plots.COUNTS_PCT.value:
      (fig,descr) = graph_counts_pct(nucleotide=nvalue)
    elif value == constants.Plots.COUNTS_PCT_BASE.value:
      (fig,descr) = graph_counts_pct_shifted(nucleotide=nvalue)
    elif value == constants.Plots.COUNTS_PCT_DIFF.value:
      (fig,descr) = graph_diff_counts_pct(nvalue, nvalue2)
      base_select2_style = STYLE_SHOW
    elif value == constants.Plots.SKEW.value:
      (fig, descr) = graph_skew_diagram(genome_dataset)
      genome_select_style = STYLE_SHOW
      base_select_style = STYLE_HIDDEN
    elif value == constants.Plots.NETWORK.value:
      print("Network graph")
      input = ("AAGATTCTCTAAGA", 4)
      output = pt2_week1.de_bruijn_graph_from_string(*input)
      fig = pt2_week1.de_bruijn_graph_vis(output)
      #fig = pt2_week1.sample_network_graph()
      descr = "xx"
    else:
      (fig,descr) = (px.bar(x=[1,2,3],y=[1,2,3]), """This is an example <br/>""" )
    
    fig.update_layout(height=559, margin=dict(l=0,t=40,r=0,b=0))
    return (fig, descr, base_select_style, base_select2_style, genome_select_style)