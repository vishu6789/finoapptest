# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from app import server
from apps import Moneytransfer
from apps import aeps
from apps import Railway
from apps import  front
from apps import customer


app.layout = html.Div([
    dcc.Location(id = 'url', refresh= False),
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Link('Fino Dashboard', href='/', style={'color':'white', 'font-size':'20px','margin-top':'0.4rem','font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}), color='primary', style={'height': '100%'}), width=4),
        # ,dbc.Col(dbc.Card(color='primary', style={'height': '100%'}), width=4)
        dbc.Col(dbc.Card(html.H6(id = 'header', style={'text-align':'center','color':'white','font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}), color='primary', style={'height':'4rem'}), width= 4)

        ,dbc.Col(dbc.Card(dcc.Link('Dmt', href='/dmt', style={'color':'white', 'margin-top':'1.3rem','font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}),
        color='primary', style={'text-align':'center','height': '100%'}), width = 1)
        ,dbc.Col(dbc.Card(dcc.Link('Aeps', href='/aeps', style={'color':'white', 'margin-top':'1.3rem','font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}),
        color='primary', style={'text-align':'center','height': '100%'}), width = 1)
        ,dbc.Col(dbc.Card(dcc.Link('Railway', href='/railway', style={'color':'white', 'margin-top':'1.3rem','font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}),
        color='primary', style={'text-align':'center','height': '100%'}), width = 1)
        ,dbc.Col(dbc.Card(dcc.Link('Customer', href='/customer', style={'color':'white', 'margin-top':'1.3rem','font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}),
        color='primary', style={'text-align':'center','height': '100%'}), width = 1)
        ], no_gutters=True),
    html.Div(id = 'page-content', children=[])

],style={'background':'white'})


@app.callback([
    Output('page-content','children'),Output(component_id='header', component_property='children'),
    Input('url', 'pathname')
])
def displaypage(pathname):

    if pathname == '/':
        h = 'Welcome to the Portal'
        return front.layout , h

    elif pathname == '/dmt':
        h = 'Money Transfer'
        return Moneytransfer.layout, h

    elif pathname == '/dmt/year':
        h = 'Money Transfer'
        return Moneytransfer.layout_year,h

    elif pathname == '/dmt/anlys':
        h = 'Money Transfer Analysis'
        return Moneytransfer.layout_analysis,h

    elif pathname == '/aeps':
        h = 'Cash Withdrawal'
        return aeps.layout, h

    elif pathname == '/railway':
        h = "Railway's Portal"
        return Railway.layout, h

    elif pathname == '/customer':
        h = 'Customer Portal'
        return customer.layout, h

    elif pathname == '/dmt/qtr':
        h = 'Money Transfer'
        return Moneytransfer.layout_qtr, h

if __name__ == '__main__':
    app.run_server(debug= True,host = 'localhost')

