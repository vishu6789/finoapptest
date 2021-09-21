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
import pandas as pd
import pathlib


path = pathlib.Path(__file__).parent
datapath = path.joinpath('../datasets').resolve()

df_1 = pd.read_excel(datapath.joinpath('Dataframe1.xlsx'))
df_3 = pd.read_excel(datapath.joinpath('Dataframe3.xlsx'))
df_8 = pd.read_excel(datapath.joinpath('Dataframe_avgpnr.xlsx'))


#Dataframe
# from sqldataframes import df_1
# from sqldataframes import df_3
# from sqldataframes import df_8


def card(x,a):
    crd = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Card(html.P(x, style={'text-align': 'center', 'color': 'white',
                                                        'font-family': 'Times New Roman, Times, serif',
                                                        'font-weight': 'bold', 'margin-top': '0rem','margin-bottom': '0rem'}), color='primary'))
        ]), dbc.Row([
            dbc.Col(html.H3(id=a, style={'text-align': 'center', 'color': 'black',
                                           'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                           'margin-top': '0rem'}))
        ])
    ], color='secondary', style={'height': '11rem'})
    return crd

fig5 = px.line(df_8,x = 'Year_Number', y = 'Avg_Pnr', text = 'Avg_Pnr', width =1250 ,height=250, title='Average Monthly PNR (year wise)').update_layout(margin=dict(t=0, r=0, l=0, b=0))
fig5.update_layout(yaxis = dict(showgrid = False),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',)
fig5.update_layout(xaxis = dict(showgrid = False), font = dict(family = 'calibri', size = 14), title = {'y':0.9,'x':0.5,'xanchor':'center','yanchor':'bottom'})
fig5.update_traces(line={'color':'green'} )
fig5.update_xaxes(type = 'category')


layout = html.Div([
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id = 'mnth_pnr', figure=fig5)), width = 12)
    ])
    ,dbc.Row([
        dbc.Col(card('Txn Amount', 'ra_am'), width=3), dbc.Col(card('Profit Amount', 'ra_pm'), width=3),
        dbc.Col(card('Total Transactions', 'ra_txn'), width=3), dbc.Col(card('Monthly Avg. PNR', 'ra_avg'), width=3)
    ], justify='center', no_gutters=True),

    dbc.Row([
        # dbc.Col(dbc.Card([
        #     html.H6(id='r_header_year', style={'text-align': 'center', 'font-family': 'Times New Roman, Times, serif',
        #                                        'font-weight': 'bold', 'color': 'white', 'margin-left': '22rem'})
        #
        # ], color='primary', style={'height': '3.8rem'}), width=10),
    dbc.Col(dbc.Card([
            dcc.Dropdown(id='yr2', options=[{'label': '2018', 'value': 2018}, {'label': '2019', 'value': 2019},
                                            {'label': '2020', 'value': 2020},
                                            {'label': '2021', 'value': 2021}], value=2021)
        ], color='secondary'), width=12)
    ], no_gutters=True),

    html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id='r_mnth_grph', figure={},style={'height': '50vh'}), width=12)
        ])
    ]),
    html.Div([
        dbc.Row([
            dbc.Col(card('Transaction_Amount','r_am'), width=3),dbc.Col(card('Profit_Amount','r_pm'), width=3),dbc.Col(card('Total_PNR','r_txn'), width=3),dbc.Col(card('Avg_PNR per day','r_avg'), width=3)
        ], justify='center', no_gutters=True)
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H6(id='r_header_month',
                    style={'text-align': 'center', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                           'color': 'white', 'margin-left': '2rem'})

        ], color='primary', style={'height': '77%'}), width=10), dbc.Col(dbc.Card([
            dcc.Dropdown(id='mnth', options=[{'label': 'Januray', 'value': 1}, {'label': 'February', 'value': 2},
                                             {'label': 'March', 'value': 3},
                                             {'label': 'April', 'value': 4}, {'label': 'May', 'value': 5},
                                             {'label': 'June', 'value': 6}, {'label': 'July', 'value': 7},
                                             {'label': 'August', 'value': 8}, {'label': 'September', 'value': 9},
                                             {'label': 'October', 'value': 10}, {'label': 'November', 'value': 11},
                                             {'label': 'December', 'value': 12}], value=1)
        ], color='secondary'), width=2)
    ], no_gutters=True),
    dbc.Row([
        dbc.Col(dcc.Graph(id = 'r_fig', figure={}),width=8), dbc.Col(dcc.Graph(id = 'r_fig1', figure={}), width=4)
    ], no_gutters=True)

])


@app.callback(
    [Output(component_id='ra_am', component_property='children'),Output(component_id='ra_pm', component_property='children'),
     Output(component_id='ra_txn', component_property='children'),Output(component_id='ra_avg', component_property='children'),Output(component_id='r_mnth_grph', component_property='figure'),
     Output(component_id='r_fig', component_property='figure'),Output(component_id='r_header_month', component_property='children'),Output(component_id='r_fig1', component_property='figure'),
     Output(component_id='r_am', component_property='children'),Output(component_id='r_pm', component_property='children'),Output(component_id='r_txn', component_property='children'),
     Output(component_id='r_avg', component_property='children'),
     Input(component_id='mnth', component_property='value'),Input(component_id='yr2', component_property='value')]

)
def updated(mnth, yr2):
    df1 = df_1.copy()
    df3 = df_3.copy()

    r_header_year = yr2
    ra_am = round((df1[['Txn_Amount']][df1.Type == 'Rail'][df1.Year_Number == yr2]).sum()).get('Txn_Amount')
    ra_pm = round((df1[['Profit_Amount']][df1.Type == 'Rail'][df1.Year_Number == yr2]).sum()).get('Profit_Amount')
    ra_txn = ((df1[['Total_Txns']][df1.Type == 'Rail'][df1.Year_Number == yr2]).sum()).get('Total_Txns')
    max_mnth = ((df1[['Month_Number']][df1.Type == 'Rail'][df1.Year_Number == yr2])).get('Month_Number')
    m_max = max(max_mnth)
    ra_avg = round(ra_txn / m_max)

    r_am1 = (df1[['Total_Txns']][df1.Type == 'Rail'][df1.Year_Number == yr2]).get('Total_Txns')
    mnthn = (df1[['Month_Number']][df1.Type == 'Rail'][df1.Year_Number == yr2]).get('Month_Number')

    fig2 = px.bar(x=mnthn, y=r_am1, text=r_am1, orientation='v', hover_data=[r_am1],
                  template='plotly_dark', labels={''})
    fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig2.update_xaxes(title_text='Month Number', color='black', showgrid=False)
    fig2.update_yaxes(title_text="PNR's", color='black', showgrid=False)



    df = (df3[df3.Month_Number == mnth][df3.Year_Number == yr2][df3.Type == 'Rail'])
    fig = px.bar(df, x = 'Day_Number', y = 'Total_Txns', text='Total_Txns', color='Month_Number')
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(title_text='Day Number', color='black', showgrid=False)
    fig.update_yaxes(title_text='Amount', color='black', showgrid=False)
    x = calendar.month_name[mnth]
    y = (f'{x} {yr2}')

    df0 = (df3[df3['Type'] == 'Rail'])
    df1 = df0.groupby(['Year_Number', 'Month_Number'], as_index=False)[['Txn_Amount', 'Profit_Amount', 'Total_Txns']].sum()
    z = (df1[df1.Month_Number == mnth])
    m_am = round((df1[['Txn_Amount']][df1.Month_Number == mnth][df1.Year_Number == yr2]).get('Txn_Amount'))
    p_am = round((df1[['Profit_Amount']][df1.Month_Number == mnth][df1.Year_Number == yr2]).get('Profit_Amount'))
    m_txn = (df1[['Total_Txns']][df1.Month_Number == mnth][df1.Year_Number == yr2]).get('Total_Txns')
    m_avg = ''
    if mnth == 1:
        m_avg = round(m_txn/31)
    elif mnth == 2:
        m_avg = round(m_txn/28)
    elif mnth == 3:
        m_avg = round(m_txn/31)
    elif mnth == 4:
        m_avg = round(m_txn/30)
    elif mnth == 5:
        m_avg = round(m_txn/31)
    elif mnth == 6:
        m_avg = round(m_txn/30)
    elif mnth == 7:
        m_avg = round(m_txn/31)
    elif mnth == 8:
        m_avg = round(m_txn/31)
    elif mnth == 9:
        m_avg = round(m_txn/30)
    elif mnth == 10:
        m_avg = round(m_txn/31)
    elif mnth == 11:
        m_avg = round(m_txn/30)
    else:
        m_avg = round(m_txn /31)


    fig1 = px.bar(z, x = 'Year_Number', y= 'Total_Txns', barmode='group', text='Total_Txns', color_continuous_scale=px.colors.cyclical.Phase, title=f'Yearly Comparision {x}')
    fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig1.update_xaxes(title_text='Year Number', color='black', showgrid=False)
    fig1.update_yaxes(title_text="PNR's", color='black', showgrid=False)


    return  ra_am, ra_pm, ra_txn, ra_avg, fig2,fig, y, fig1,m_am, p_am,m_txn, m_avg







