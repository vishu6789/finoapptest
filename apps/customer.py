# import dash
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import calendar
from app import app
from datetime import datetime
import pandas as pd
import pathlib

path = pathlib.Path(__file__).parent
datapath = path.joinpath('../datasets').resolve()

df_4 = pd.read_excel(datapath.joinpath('Dataframe_benestatuscount.xlsx'))
df_5 = pd.read_excel(datapath.joinpath('Dataframe_accountnumbercount.xlsx'))
df_6 = pd.read_excel(datapath.joinpath('Dataframe_newcustomer.xlsx'))
df_7 = pd.read_excel(datapath.joinpath('Dataframe_newcustomeravg.xlsx'))

#Dataframe..
# from sqldataframes import df_4
# from sqldataframes import df_5
# from sqldataframes import df_6
# from sqldataframes import df_7


x = df_4.values
ab = (df_4.values)
y = (df_5[['Account_Numbers']].get('Account_Numbers').iloc[-1])

fig1 = px.line(df_7, x = 'Year_Number', y = 'Avarage_Customers')
fig1.update_traces(mode = 'lines+markers+text')
fig1.update_yaxes(showgrid = False)
fig1.update_xaxes(showgrid = False, type = 'category')
fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})

def card0(x,a):
    crd = dbc.Card([
        dbc.Row([
            dbc.Col(html.P(x, style={'text-align': 'center', 'color': 'white',
                                                        'font-family': 'Times New Roman, Times, serif',
                                                        'font-weight': 'bold', 'margin-top': '0rem'}))
        ]), dbc.Row([
            dbc.Col(html.H3(id=a, style={'text-align': 'center', 'color': 'white',
                                           'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                           'margin-top': '0rem'}))
        ])
    ], color='dark', style={'height': '11rem'})
    return crd

def card(a,b,c):
    card = dbc.Card([
        dbc.Row([
            dbc.Col(html.P(a, style={'text-align':'center','font-family': 'Times New Roman, Times, serif', 'font-weight':'bold','color':'black'})),
        ]),
        dbc.Row([
            dbc.Col(html.H5(b, style={'text-align':'center','font-family': 'Times New Roman, Times, serif', 'font-weight':'bold','color':'black'}))
        ])
    ],color=c, style={'height': '9rem'})
    return card


curr_year = datetime.now().year
prv_year = datetime.now().year - 1

avg_curr = (df_7[['Avarage_Customers']][df_7.Year_Number == curr_year])
avg_prv = (df_7[['Avarage_Customers']][df_7.Year_Number == prv_year])
lis = []

for i in avg_curr['Avarage_Customers']:
    lis.append(i)
for i in avg_prv['Avarage_Customers']:
    lis.append(i)

if lis[0] >lis[1]:
    fig1.update_traces(line = {'color':'green'})
elif lis[0] < lis[1]:
    fig1.update_traces(line={'color': 'red'})
fig5 = go.Figure(go.Indicator(
        mode='delta',
        value=lis[0],
        delta={'reference': lis[1], 'relative': True, 'valueformat': '.2%'}
    ))
fig5.update_traces(delta_font={'size': 20})
fig5.update_layout(height=60, width=100)





layout = html.Div([
    dbc.Row([
dbc.Col(dbc.Card(html.P(f'Total Customers : {y}', style={'text-align':'center','font-family': 'Times New Roman, Times, serif', 'font-weight':'bold','color':'white','margin-left':'2rem'}), color='dark', style={'height': '100%'}), width=12)
    ])

    ,dbc.Row([
        dbc.Col(card('Active', x[0][3], 'success'), width=3), dbc.Col(card('In-Active', x[2][3], 'warning'), width=3),
        dbc.Col(card('Partially-Closed', x[3][3], 'info'), width=3), dbc.Col(card('Closed', x[1][3], 'danger'), width=3)
    ], justify='center', no_gutters=True),
    dbc.Row([
        dbc.Col(dbc.Card(html.P(id='year', style={'text-align':'center','color':'white','font-family': 'Times New Roman, Times, serif',
                                                  'font-weight': 'bold', 'margin-top': '0.5rem', 'margin-left':'22rem'}), color='dark'), width=10),
        dbc.Col(dbc.Card(dcc.Dropdown(id = 'cs_yr', options=[{'label':'2021', 'value':2021},{'label':'2020', 'value':2020}
                                                             ,{'label':'2019', 'value':2019},{'label':'2018', 'value':2018}], value=2021
        ), color='dark'), width=2)
    ], no_gutters=True),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='a_1', figure={}, style={'margin-left':'25rem'})), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id='a_2', figure=fig5, style={'margin-left':'25rem'})), width=6)
    ], no_gutters=True),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id = 'count', figure={})), width=6), dbc.Col(dbc.Card(dcc.Graph(id = 'count1', figure=fig1)), width=6)
    ], no_gutters=True),
    # dbc.Row([
    #     dbc.Col(dcc.Graph(id= 'a', figure=fig9), width = 12)
    # ])

])

@app.callback([
    Output(component_id='year', component_property='children'),
    Output(component_id='a_1', component_property='figure'),
    Output(component_id='count', component_property='figure'),
    Input(component_id='cs_yr', component_property='value')
])
def fxn(value):
    df6 = df_6.copy()
    df = (df6[df6.Year_Number == value])
    df = df.sort_values('Month_Number')
    year = (df[['Year_Number']].drop_duplicates()).get('Year_Number')
    fig = px.line(df, x = 'Month_Number', y = 'New_Customers')
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(title_text='Month Number', color='black', showgrid=False)
    fig.update_yaxes(title_text='New Customers', color='black', showgrid=False)

    a = (df6[['New_Customers', 'Month_Number']][df6.Year_Number == value])
    max_mnth_count = (a[['New_Customers']][a.Month_Number == max(a.Month_Number)])
    avg_count = (df_7[['Avarage_Customers']][df_7.Year_Number == value])

    l = []
    for i in max_mnth_count['New_Customers']:
        l.append(i)
    for i in avg_count['Avarage_Customers']:
        l.append(i)
    if l[0] >l[1]:
        fig.update_traces(line = {'color':'green'})
    elif l[0] < l[1]:
        fig.update_traces(line={'color': 'red'})

    fig4 = go.Figure(go.Indicator(
        mode='delta',
        value=l[0],
        delta={'reference': l[1], 'relative': True, 'valueformat': '.2%'}
    ))
    fig4.update_traces(delta_font={'size': 20})
    fig4.update_layout(height=60, width=100)

    return year, fig4, fig











