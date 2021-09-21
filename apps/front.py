# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_extensions as de
import dash
import plotly.express as px
import plotly.graph_objects as go
import calendar
import plotly.io as pio
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from app import app
from app import server
from apps import Moneytransfer, aeps, Railway
import pathlib
import pandas as pd

path = pathlib.Path(__file__).parent
datapath = path.joinpath('../datasets').resolve()


df_1 = pd.read_excel(datapath.joinpath('Dataframe1.xlsx'))


#Dataframe..
# from sqldataframes import df_1


# ob2 = pd.read_sql_query('select * from vw_yearlydata1', conn).reset_index()
# df2 = pd.DataFrame(ob2)
#
# ob3 = pd.read_sql_query('select * from vw_dailydata',conn).reset_index()
# df3 = pd.DataFrame(ob3)
#
# ob4 = pd.read_sql_query('select * from vw_BeneStatuscoun',conn).reset_index()
# df4 = pd.DataFrame(ob4)
#
# ob5 = pd.read_sql_query('select * from Accountnumber_count',conn).reset_index()
# df5 = pd.DataFrame(ob5)


options = dict(loop=True, autoplay=True)
train = 'https://assets9.lottiefiles.com/packages/lf20_NzgvNs.json'
dmt = 'https://assets7.lottiefiles.com/packages/lf20_k8tUSG.json'
aeps = 'https://assets4.lottiefiles.com/datafiles/D2dX6GVqV6yrIAT/data.json'


dmt_obj = (df_1[df_1['Type']=='Dmt'])
df_dmt = dmt_obj.groupby(['Year_Number'], as_index=False)[['Txn_Amount','Profit_Amount','Total_Txns']].sum()

aep_obj = (df_1[df_1['Type']=='Aeps'])
df_aep = aep_obj.groupby(['Year_Number'], as_index=False)[['Txn_Amount','Profit_Amount','Total_Txns']].sum()

rail_obj = (df_1[df_1['Type']=='Rail'])
df_rail = rail_obj.groupby(['Year_Number'], as_index=False)[['Txn_Amount','Profit_Amount','Total_Txns']].sum()


fig = px.bar(df_dmt,x='Year_Number',y='Txn_Amount', title='Yearly Report', text='Txn_Amount')
fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig.update_xaxes(title_text='Year Number', color='black', showgrid=False)
fig.update_yaxes(title_text='Amount', color='black', showgrid=False)
fig.update_traces(texttemplate='%{text:.2s}',textposition = 'outside')


fig1 = px.bar(df_aep,x='Year_Number',y='Txn_Amount', text='Txn_Amount')
fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig1.update_xaxes(title_text='Year Number', color='black', showgrid=False, type = 'category')
fig1.update_yaxes(title_text='Amount', color='black', showgrid=False)
fig1.update_traces(texttemplate='%{text:.3s}',textposition = 'outside')


fig2 = px.bar(df_rail,x='Year_Number',y='Total_Txns', text='Total_Txns')
fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
fig2.update_xaxes(title_text='Year Number', color='black', showgrid=False)
fig2.update_yaxes(title_text='PNR', color='black', showgrid=False)
fig2.update_traces(textposition = 'outside')


card0 = dbc.Card([
    dbc.CardBody([
        html.Div(de.Lottie(options = options,width='50%',height='10%',url = dmt))
    ], style={'height':'25rem'})
])

c1 = dbc.Card([
    dbc.Row([
        dbc.Col(html.H6('Total Turnover', style={'text-align': 'center', 'color': 'white',
                                                        'font-family': 'Times New Roman, Times, serif',
                                                        'font-weight': 'bold', 'margin-top': '0rem'}))
    ]),
    dbc.Row([
        dbc.Col(html.P('Rs. 106151898', style={'text-align': 'center', 'color': 'white',
                                                        'font-family': 'Times New Roman, Times, serif',
                                                        'font-weight': 'bold', 'margin-top': '0rem'}))
    ]),    dbc.Row([
        dbc.Col(html.H6('Total Transactions', style={'text-align': 'center', 'color': 'white',
                                                        'font-family': 'Times New Roman, Times, serif',
                                                        'font-weight': 'bold', 'margin-top': '0rem'}))
    ]),
    dbc.Row([
        dbc.Col(html.P('', style={'text-align': 'center', 'color': 'white',
                                                        'font-family': 'Times New Roman, Times, serif',
                                                        'font-weight': 'bold', 'margin-top': '0rem'}))
    ])
], color='primary')


layout = html.Div([
    dcc.Interval(id = 'intrvl', disabled=False, interval= 1 *3000, n_intervals=0, max_intervals=-1),

    dbc.Row([
        dbc.Col(card0, width=12)
    ], justify='center')

    ,dbc.Row([
        dbc.Col(dbc.Card(html.P('Money Transfer', style={'text-align':'center','color':'white','font-family': 'Times New Roman, Times, serif', 'font-weight':'bold','margin-top':'0rem','margin-bottom':'0rem'}),color='dark'), width=4),
        dbc.Col(dbc.Card(html.P('Withdrawal', style={'text-align':'center','color':'white','font-family': 'Times New Roman, Times, serif', 'font-weight':'bold','margin-top':'0rem','margin-bottom':'0rem'}),color='dark'), width=4),
        dbc.Col(dbc.Card(html.P('Railway', style={'text-align':'center','color':'white','font-family': 'Times New Roman, Times, serif', 'font-weight':'bold','margin-top':'0rem','margin-bottom':'0rem'}),color='dark'), width=4)
    ], no_gutters=True)

    ,dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id = 'dmt', figure=fig), color='secondary'), width=4),dbc.Col(dbc.Card(dcc.Graph(id = 'apes', figure=fig1), color='secondary'), width=4),dbc.Col(dbc.Card(dcc.Graph(id = 'rail', figure=fig2), color='secondary'), width=4)
    ], no_gutters=True),

    dbc.Row([
        dbc.Col(dcc.Dropdown(id='yr_chsn', options=[{'label':'2018', 'value':2018},{'label':'2019', 'value':2019}
                                                    ,{'label':'2020', 'value':2020},{'label':'2021', 'value':2021}], value=2021))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id = 'a', figure={},style={'height':''}), width=12)
    ])
], style={'background':'mintcream'})

@app.callback(
    Output(component_id='a', component_property='figure'),
    [Input(component_id='yr_chsn', component_property='value'), Input('intrvl','n_intervals')]
)
def grph(yr,intrvls):
    if intrvls == 0:
        raise PreventUpdate
    else:
        df = df_1.copy()
        df = (df[df.Type == 'Rail'][df.Year_Number == yr])
        df1 = df.groupby(['Month_Number'], as_index=False)[
            ['Txn_Amount', 'Profit_Amount', 'Total_Txns']].sum()

        fig3 = px.line(df1, x='Month_Number', y='Total_Txns', text='Total_Txns')
        fig3.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                            'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        fig3.update_xaxes(title_text='Month Number', color='black', showgrid=False)
        fig3.update_yaxes(title_text='PNR', color='black', showgrid=False)
        fig3.update_traces(textposition="bottom right")
        # fig3.update_traces(fill ='tozeroy',line={'color':'red'} )

        return fig3




