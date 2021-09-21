# import dash
# import dash_core_components as dcc
# # import dash_html_components as html
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import calendar
import pandas as pd
from app import app
import pathlib

path = pathlib.Path(__file__).parent
datapath = path.joinpath('../datasets').resolve()

df_1 = pd.read_excel(datapath.joinpath('Dataframe1.xlsx'))
df_3 = pd.read_excel(datapath.joinpath('Dataframe3.xlsx'))
df_10 = pd.read_excel(datapath.joinpath('Dataframe_avgaeps.xlsx'))

#Dataframe..
# from sqldataframes import df_1
# from sqldataframes import df_3
# from sqldataframes import df_10

fig5 = px.line(df_10,x = 'Year_Number', y = 'Avg_Amount', height=250, width= 1250, title='Avarage Monthly Transaction Amount (year wise)').update_layout(margin=dict(t=0, r=0, l=0, b=0))
fig5.update_layout(yaxis = dict(showgrid = False),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',)
fig5.update_layout(xaxis = dict(showgrid = False), font = dict(family = 'calibri', size = 14), title = {'y' : 0.9, 'x' : 0.5, 'xanchor':'center','yanchor':'bottom'})
fig5.update_xaxes(type = 'category')

b = int((df_10[['Avg_Amount']][df_10.Year_Number == 2020]).get('Avg_Amount'))
c = int((df_10[['Avg_Amount']][df_10.Year_Number == 2021]).get('Avg_Amount'))

if b > c :
    fig5.update_traces(line={'color': 'red'})
else:
    fig5.update_traces(line={'color': 'green'})



def card(x,a):
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
    ], color='success', style={'height': '11rem'})
    return crd

layout = html.Div([

    dbc.Row([
             dbc.Col(dbc.Card(dcc.Graph(id='daily_avg', figure=fig5)), width=12)]),

    dbc.Row([
            dbc.Col(card('Txn Amount','ae_am'), width=3),dbc.Col(card('Profit Amount','ae_pm'), width=3),dbc.Col(card('Total Transactions','ae_txn'), width=3),dbc.Col(card('Avg. Amount','ae_avg'), width=3)
        ], justify='center', no_gutters=True),

    dbc.Row([
        dbc.Col(dbc.Card([
            html.H6(id='a_header_year',
                    style={'text-align': 'center', 'font-family': 'Times New Roman, Times, serif',
                           'font-weight': 'bold',
                           'color': 'black', 'margin-left': '20rem'})

        ], color='secondary', style={'height': '77%'}), width=10), dbc.Col(dbc.Card([
            dcc.Dropdown(id='yr1', options=[{'label': '2020', 'value': 2020},
                                            {'label': '2021', 'value': 2021}], value=2021)
        ], color='secondary'), width=2)
    ], no_gutters=True),

    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id='mnth_grph', figure={},style={'height': '50vh'}), width=12)
        ])
    ]),
    html.Div([
        dbc.Row([
            dbc.Col(card('Transaction_Amount','a_am'), width=3),dbc.Col(card('Profit_Amount','a_pm'), width=3),dbc.Col(card('Total_Txns','a_txn'), width=3),dbc.Col(card('Avg_Amount','a_avg'), width=3)
        ], justify='center', no_gutters=True)
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H6(id='a_header_month',
                    style={'text-align': 'center', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                           'color': 'black', 'margin-left': '20rem'})

        ], color='secondary', style={'height': '77%'}), width=10), dbc.Col(dbc.Card([
            dcc.Dropdown(id='mnth', options=[{'label': 'Jan', 'value': 1}, {'label': 'Feb', 'value': 2},
                                             {'label': 'Mar', 'value': 3},
                                             {'label': 'Apr', 'value': 4}, {'label': 'May', 'value': 5},
                                             {'label': 'Jun', 'value': 6}, {'label': 'Jul', 'value': 7},
                                             {'label': 'Aug', 'value': 8}, {'label': 'Sep', 'value': 9},
                                             {'label': 'Oct', 'value': 10}, {'label': 'Nov', 'value': 11},
                                             {'label': 'Dec', 'value': 12}], value=1)
        ], color='secondary'), width=2)
    ], no_gutters=True),
    dbc.Row([
        dbc.Col(dcc.Graph(id = 'a_fig', figure={}),width=8), dbc.Col(dcc.Graph(id = 'a_fig1', figure={}), width=4)
    ], no_gutters=True)

])


@app.callback(
    [
     Output(component_id='a_header_year', component_property='children'),Output(component_id='ae_am', component_property='children'),Output(component_id='ae_pm', component_property='children'),
     Output(component_id='ae_txn', component_property='children'),Output(component_id='ae_avg', component_property='children'),Output(component_id='mnth_grph', component_property='figure'),
     Output(component_id='a_fig', component_property='figure'),Output(component_id='a_header_month', component_property='children'),Output(component_id='a_fig1', component_property='figure'),
     Output(component_id='a_am', component_property='children'),Output(component_id='a_pm', component_property='children'),Output(component_id='a_txn', component_property='children'),
     Output(component_id='a_avg', component_property='children'),
    Input(component_id='mnth', component_property='value'),Input(component_id='yr1', component_property='value')]
)
def updated(mnth,yr):
    df1 = df_1.copy()
    df3 = df_3.copy()

    a_header_year = (f'FY : {yr}')
    ae_am = round((df1[['Txn_Amount']][df1.Type == 'Aeps'][df1.Year_Number == yr]).sum()).get('Txn_Amount')
    ae_pm = round((df1[['Profit_Amount']][df1.Type == 'Aeps'][df1.Year_Number == yr]).sum()).get('Profit_Amount')
    ae_txn = ((df1[['Total_Txns']][df1.Type == 'Aeps'][df1.Year_Number == yr]).sum()).get('Total_Txns')
    ae_avg = round(ae_am / ae_txn)

    ae_am1 = (df1[['Txn_Amount']][df1.Type == 'Aeps'][df1.Year_Number == yr]).get('Txn_Amount')
    mnthn = (df1[['Month_Number']][df1.Type == 'Aeps'][df1.Year_Number == yr]).get('Month_Number')

    fig2 = px.bar(x=mnthn, y=ae_am1, text=ae_am1, orientation='v', hover_data=[ae_am1],
                 template='plotly_dark', labels={''})
    fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig2.update_xaxes(title_text='Month Number', color='black', showgrid=False)
    fig2.update_yaxes(title_text='Amount', color='black', showgrid=False)
    fig2.update_traces(texttemplate='%{text:.4s}')


    df = (df3[df3.Month_Number == mnth][df3.Year_Number == yr][df3.Type == 'Aeps'])
    fig = px.bar(df, x = 'Day_Number', y = 'Txn_Amount', text='Txn_Amount', color='Month_Number')
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(title_text='Day Number', color='black', showgrid=False)
    fig.update_yaxes(title_text='Amount', color='black', showgrid=False)
    x = calendar.month_name[mnth]
    y = (f'{x} {yr}')

    df0 = (df3[df3['Type'] == 'Aeps'])
    df1 = df0.groupby(['Year_Number', 'Month_Number'], as_index=False)[['Txn_Amount', 'Profit_Amount', 'Total_Txns']].sum()
    z = (df1[df1.Month_Number == mnth])
    m_am = round((df1[['Txn_Amount']][df1.Month_Number == mnth][df1.Year_Number == yr]).get('Txn_Amount'))
    p_am = round((df1[['Profit_Amount']][df1.Month_Number == mnth][df1.Year_Number == yr]).get('Profit_Amount'))
    m_txn = (df1[['Total_Txns']][df1.Month_Number == mnth][df1.Year_Number == yr]).get('Total_Txns')
    m_avg = round(m_am /m_txn)

    fig1 = px.bar(z, x = 'Year_Number', y= 'Txn_Amount', barmode='group', text='Txn_Amount', color_continuous_scale=px.colors.cyclical.Phase, title=f'Yearly Comparision {x}')
    fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig1.update_xaxes(title_text='Year Number', color='black', showgrid=False, type = 'category')
    fig1.update_yaxes(title_text='Amount', color='black', showgrid=False)


    return a_header_year,ae_am,ae_pm,ae_txn,ae_avg,fig2,  fig, y, fig1,m_am, p_am,m_txn, m_avg








