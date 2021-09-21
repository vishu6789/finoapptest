import dash
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.YETI])
server = app.server
