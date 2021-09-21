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
from datetime import datetime
import pathlib

path = pathlib.Path(__file__).parent
datapath = path.joinpath('../datasets').resolve()

df_1 = pd.read_excel(datapath.joinpath('Dataframe1.xlsx'))
df_3 = pd.read_excel(datapath.joinpath('Dataframe3.xlsx'))
df_qtr = pd.read_excel(datapath.joinpath('Dataframe_qtr.xlsx'))
df_9 = pd.read_excel(datapath.joinpath('Dataframe_avgamount.xlsx'))
df_9 = df_9.sort_values('Year_Number')


#dataframe..
# from sqldataframes import df_1
# from sqldataframes import df_3
# from sqldataframes import df_qtr
# from sqldataframes import df_9


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
        # ]), dbc.Row([
        #     dbc.Col(dcc.Graph(id =b, figure=fig4, style={'margin-left':'10rem'}))
        ])

    ], color='success', style={'height': '12rem'})
    return crd

def indicator(value, compare):

    fig9 = go.Figure(go.Indicator(
            mode='delta',
            value=value,
            delta={'reference': compare, 'relative': True, 'valueformat': '.2%'},
        # delta={'reference': 500, 'relative': True, 'valueformat': '.2%','increasing': {'color':'green'}, 'decreasing' : {'color':'brown'}}
    ))
    fig9.update_traces(delta_font={'size': 15})
    fig9.update_layout(height=20, width=100)
    fig9.update_layout(paper_bgcolor='rgb(0,0,0,0)', plot_bgcolor= 'rgb(0,0,0,0)')
    return fig9

def card1(x,a,m,n,b,c):
    crd = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.Card(html.P(x, style={'text-align': 'center', 'color': 'white',
                                                        'font-family': 'Times New Roman, Times, serif',
                                                        'font-weight': 'bold', 'margin-top': '0rem'}), color='primary',style={'height': '2.5rem'}))
        ])
        ,dbc.Row([
            dbc.Col(html.H3(id=a, style={'text-align': 'center', 'color': 'black',
                                           'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                           'margin-top': '0rem'}))
        ]),
        dbc.Row([
            dbc.Col(html.P(id= m, style={'text-align': 'center', 'color': 'black',
                                             'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold','margin-left': '0rem'}))
            , dbc.Col(dcc.Graph(id = b, figure = {}))
        ]),
        dbc.Row([
            dbc.Col(html.P(id = n, style={'text-align': 'center', 'color': 'black',
                                             'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                             'margin-left': '0rem'}))
            , dbc.Col(dcc.Graph(id= c, figure={}))
        ])

    ], color='secondary', style={'height': '14rem'})
    return crd

fig5 = px.line(df_9,x = 'Year_Number', y = 'Avg_Amount', height=250, title='Monthly Transaction').update_layout(margin=dict(t=0, r=0, l=0, b=0))
fig5.update_layout(yaxis = dict(showgrid = False),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',)
fig5.update_layout(xaxis = dict(showgrid = False))
fig5.update_xaxes(type = 'category')

a = int((df_9[['Avg_Amount']][df_9.Year_Number == 2019]).get('Avg_Amount'))
b = int((df_9[['Avg_Amount']][df_9.Year_Number == 2020]).get('Avg_Amount'))
c = int((df_9[['Avg_Amount']][df_9.Year_Number == 2021]).get('Avg_Amount'))

if c < b or c < a :
    fig5.update_traces(line={'color': 'red'})
else:
    fig5.update_traces(line={'color': 'green'})

layout_qtr = html.Div([
    dbc.Row([
        #
        # dbc.Col(dbc.Card(html.P(id='qtr_hdr', children=[], style={'text-align': 'center', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
        #                    'color': 'black'})), width=10),
        dbc.Col(dbc.Card(dcc.Dropdown(id = 'dw_yr', options=[{'label':'2021', 'value':2021},
                                                             {'label':'2020', 'value':2020},
                                                             {'label':'2019', 'value':2019},
                                                              {'label':'2018', 'value':2018}], value= 2021, multi=False)), width = 6),
        dbc.Col(dbc.Card(dcc.Dropdown(id='dw_qtr', options=[{'label': 'Qtr 1', 'value': 1},
                                                           {'label': 'Qtr 2', 'value': 2},
                                                           {'label': 'Qtr 3', 'value': 3},
                                                           {'label': 'Qtr 4', 'value': 4}], value=1, multi=False)),   width=6)
    ], no_gutters=True
    ),

    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id = 'qtr_am', figure = {})), width = 6), dbc.Col(dbc.Card(dcc.Graph(id = 'qtr_txn', figure={})), width = 6)
    ], no_gutters=True)
])

layout_year = html.Div([

    dbc.Row([dbc.Col(card('Txn Amount','y_am'),width=3),dbc.Col(card('Profit Amount','y_pm'), width=3)
            ,dbc.Col(card('Total Transactions','y_txn'), width=3),dbc.Col(card('Avg. Amount','y_avg'), width=3)
            ], justify='center', no_gutters=True),
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H6(id='m_header_year',style={'text-align': 'center', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                           'color': 'black', 'margin-left': '2rem'})], color='secondary', style={'height': '77%'}), width=10),
        dbc.Col(dbc.Card([
            dcc.Dropdown(id='yr', options=[{'label': '2021', 'value': 2021}, {'label': '2020', 'value': 2020},
                                           {'label': '2019', 'value': 2019},
                                           {'label': '2018', 'value': 2018}], value=2021
                         )
                        ], color='secondary'), width=2)
            ], no_gutters=True),
    dbc.Row([dbc.Col(dcc.Graph(id='mnth_grph1', figure={},style={'height': '50vh'}), width=12)]),
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H6('Monthly Comparision',
                    style={'text-align': 'center', 'font-family': 'Times New Roman, Times, serif',
                           'font-weight': 'bold',
                           'color': 'black'})], color='secondary', style={'height': '77%'}), width=12)]),

    dbc.Row([
        dbc.Col(dbc.Card([
            dcc.Dropdown(id='yr2', options=[{'label': '2019', 'value': 2019},
                                            {'label': '2020', 'value': 2020},
                                            {'label': '2021', 'value': 2021}], value=[datetime.now().year], multi=True
                         )
        ], color='secondary'), width=4),
        dbc.Col(dbc.Card([dcc.Dropdown(id='mnth1', options=[{'label': 'Jan', 'value': 1}, {'label': 'Feb', 'value': 2},
                                                            {'label': 'Mar', 'value': 3},
                                                            {'label': 'Apr', 'value': 4}, {'label': 'May', 'value': 5},
                                                            {'label': 'Jun', 'value': 6}, {'label': 'Jul', 'value': 7},
                                                            {'label': 'Aug', 'value': 8}, {'label': 'Sep', 'value': 9},
                                                            {'label': 'Oct', 'value': 10},
                                                            {'label': 'Nov', 'value': 11},
                                                            {'label': 'Dec', 'value': 12}], value=[datetime.now().month], multi=True)],
                         color='secondary'), width=8)], no_gutters=True),

    dbc.Row([
        dbc.Col()
    ])

    ,dbc.Row([
        dbc.Col(dcc.Graph(id='m_fig3', figure={}), width=12)
    ], no_gutters=True, justify='center')

    ])

layout_analysis = html.Div([

])

layout = html.Div([
    dbc.Row([
        dbc.Col(dbc.Card(dbc.Nav([dbc.NavLink('Quarter ', href='/dmt/qtr', style={'text-align': 'center','font-family': 'Times New Roman, Times, serif',
                            'font-weight': 'bold','color': 'white','margin-left': '15rem'})],style={'text-align': 'center'}), color='primary', style={'height':'3rem'}), width=4),
        dbc.Col(dbc.Card(dbc.Nav([dbc.NavLink('Year Section ', href='/dmt/year', style={'text-align': 'center','font-family': 'Times New Roman, Times, serif',
                            'font-weight': 'bold','color': 'white','margin-left': '15rem'})]), color= 'primary', style={'height':'3rem'}),width=4),
        dbc.Col(dbc.Card(dbc.Nav([dbc.NavLink('Analysis ', href='/dmt/anlys', style={'text-align': 'center','font-family': 'Times New Roman, Times, serif',
                            'font-weight': 'bold','color': 'white','margin-left': '15rem'})],style={'text-align': 'center'}), color= 'primary', style={'height':'3rem'}), width=4),
            ], no_gutters=True)
    # html.Div(dbc.Card(html.P('Monthly Txn Per Month', style={'text-align': 'center', 'color': 'white','font-family': 'Times New Roman, Times, serif','font-weight': 'bold', 'margin-bottom': '0rem'}),
    #                   color = 'primary' ))
    ,dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id='mnth_pnr', figure=fig5)), width=12)
    ]),
    # html.Br(),

    dbc.Row([
            dbc.Col(card1('Transaction_Amount','m_am','yta1','yta2','c_ta19','c_ta20'), width=3),dbc.Col(card1('Profit_Amount','m_pm','ypa1','ypa2','c_pa19','c_pa20'), width=3)
            ,dbc.Col(card1('Total_Txns','m_txn','ytt1','ytt2', 'c_tt19','c_tt20'), width=3),dbc.Col(card1('Avg_Amount','m_avg','yaa1','yaa2','c_aa19','c_aa20'), width=3)
        ], justify='center', no_gutters=True),
    dbc.Row([
        dbc.Col(dbc.Card([
            html.H6(id='m_header_month',
                    style={'text-align': 'left', 'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                           'color': 'white','margin-left':'2rem'})

        ], color='primary', style={'height': '3.8rem'}), width=10),
        dbc.Col(dbc.Card([dcc.Dropdown(id='yr', options=[{'label': '2018', 'value': 2018}, {'label': '2019', 'value': 2019},
                                                           {'label': '2020', 'value': 2020},{'label': '2021', 'value': 2021}], value=2021)], color='secondary'), width=1),
        dbc.Col(dbc.Card([dcc.Dropdown(id='mnth', options=[{'label': 'Jan', 'value': 1}, {'label': 'Feb', 'value': 2},
                                             {'label': 'Mar', 'value': 3},
                                             {'label': 'Apr', 'value': 4}, {'label': 'May', 'value': 5},
                                             {'label': 'Jun', 'value': 6}, {'label': 'Jul', 'value': 7},
                                             {'label': 'Aug', 'value': 8}, {'label': 'Sep', 'value': 9},
                                             {'label': 'Oct', 'value': 10}, {'label': 'Nov', 'value': 11},
                                             {'label': 'Dec', 'value': 12}], value=datetime.now().month)], color='secondary'), width=1)], no_gutters=True),
    dbc.Row([
        dbc.Col(dcc.Graph(id = 'm_fig', figure={}),width=8), dbc.Col(dcc.Graph(id = 'm_fig1', figure={}), width=4)
    ], no_gutters=True)
])




@app.callback([
     Output(component_id='yta1', component_property='children'),Output(component_id='yta2', component_property='children'),
     Output(component_id='c_ta19', component_property='figure'),Output(component_id='c_ta20', component_property='figure'),
     Output(component_id='ypa1', component_property='children'),Output(component_id='ypa2', component_property='children'),
     Output(component_id='c_pa19', component_property='figure'),Output(component_id='c_pa20', component_property='figure'),
     Output(component_id='ytt1', component_property='children'),Output(component_id='ytt2', component_property='children'),
     Output(component_id='c_tt19', component_property='figure'),Output(component_id='c_tt20', component_property='figure'),

     Output(component_id='yaa1', component_property='children'),Output(component_id='yaa2', component_property='children'),
     Output(component_id='c_aa19', component_property='figure'),Output(component_id='c_aa20', component_property='figure'),

     Output(component_id='m_fig', component_property='figure'),Output(component_id='m_header_month', component_property='children'),Output(component_id='m_fig1', component_property='figure'),
     Output(component_id='m_am', component_property='children'),Output(component_id='m_pm', component_property='children'),Output(component_id='m_txn', component_property='children'),
     Output(component_id='m_avg', component_property='children'),
    Input(component_id='mnth', component_property='value'),Input(component_id='yr', component_property='value')])
def updated(mnth,yr):
    df = df_1.copy()
    df3 = df_3.copy()
    # ob1 = pd.read_sql_query('select * from vw_yearlydata_new', conn).reset_index()
    # df = pd.DataFrame(ob1)
    yx1 = ''
    yx2 = ''
    if yr == 2021:
        yx1 = 2019
        yx2 = 2020
    if yr == 2020:
        yx1 = 2019
        yx2 = 2021
    if yr == 2019:
        yx1 = 2020
        yx2 = 2021

    tx_21 = int((df[['Txn_Amount']][df.Month_Number == mnth][df.Year_Number == 2021][df.Type == 'Dmt']).get('Txn_Amount'))
    tx_19 = int((df[['Txn_Amount']][df.Month_Number == mnth][df.Year_Number == 2019][df.Type == 'Dmt']).get('Txn_Amount'))
    tx_20 = int((df[['Txn_Amount']][df.Month_Number == mnth][df.Year_Number == 2020][df.Type == 'Dmt']).get('Txn_Amount'))
    if yr == 2021:
        j = indicator(tx_21,tx_19)
        n = indicator(tx_21,tx_20)
    elif yr == 2020:
        j = indicator(tx_20,tx_19)
        n = indicator(tx_20,tx_21)
    elif yr == 2019:
        j = indicator(tx_19,tx_20)
        n = indicator(tx_19,tx_21)

    px_21 = int((df[['Profit_Amount']][df.Month_Number == mnth][df.Year_Number == 2021][df.Type == 'Dmt']).get('Profit_Amount'))
    px_19 = int((df[['Profit_Amount']][df.Month_Number == mnth][df.Year_Number == 2019][df.Type == 'Dmt']).get('Profit_Amount'))
    px_20 = int((df[['Profit_Amount']][df.Month_Number == mnth][df.Year_Number == 2020][df.Type == 'Dmt']).get('Profit_Amount'))
    if yr == 2021:
        x1 = indicator(px_21,px_19)
        x2 = indicator(px_21,px_20)
    elif yr == 2020:
        x1 = indicator(px_20,px_19)
        x2 = indicator(px_20,px_21)
    elif yr == 2019:
        x1 = indicator(px_19,px_20)
        x2 = indicator(px_19,px_21)

    ttx_21 = int((df[['Total_Txns']][df.Month_Number == mnth][df.Year_Number == 2021][df.Type == 'Dmt']).get('Total_Txns'))
    ttx_19 = int((df[['Total_Txns']][df.Month_Number == mnth][df.Year_Number == 2019][df.Type == 'Dmt']).get('Total_Txns'))
    ttx_20 = int((df[['Total_Txns']][df.Month_Number == mnth][df.Year_Number == 2020][df.Type == 'Dmt']).get('Total_Txns'))

    if yr == 2021:
        t1 = indicator(ttx_21,ttx_19)
        t2 = indicator(ttx_21,ttx_20)
    elif yr == 2020:
        t1 = indicator(ttx_20,ttx_19)
        t2 = indicator(ttx_20,ttx_21)
    elif yr == 2019:
        t1 = indicator(ttx_19,ttx_20)
        t2 = indicator(ttx_19,ttx_21)

    ax_21 = int((df[['Total_Txns']][df.Month_Number == mnth][df.Year_Number == 2021][df.Type == 'Dmt']).get('Total_Txns'))
    ax_19 = int((df[['Total_Txns']][df.Month_Number == mnth][df.Year_Number == 2019][df.Type == 'Dmt']).get('Total_Txns'))
    ax_20 = int((df[['Total_Txns']][df.Month_Number == mnth][df.Year_Number == 2020][df.Type == 'Dmt']).get('Total_Txns'))

    if yr == 2021:
        a1 = indicator(ax_21,ax_19)
        a2 = indicator(ax_21,ax_20)
    elif yr == 2020:
        a1 = indicator(ax_20,ax_19)
        a2 = indicator(ax_20,ax_21)
    elif yr == 2019:
        a1 = indicator(ax_19,ax_20)
        a2 = indicator(ax_19,ax_21)


    df = (df3[df3.Month_Number == mnth][df3.Year_Number == yr][df3.Type == 'Dmt'])
    fig = px.bar(df, x = 'Day_Number', y = 'Txn_Amount', text='Txn_Amount', color='Month_Number')
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(title_text='Day Number', color='black', showgrid=False)
    fig.update_yaxes(title_text='Amount', color='black', showgrid=False)
    fig.update_traces(texttemplate='%{text:.2s}',textposition = 'outside', showlegend = False)
    x = calendar.month_name[mnth]
    y = (f'{x} {yr}')

    df0 = (df3[df3['Type'] == 'Dmt'])
    df1 = df0.groupby(['Year_Number', 'Month_Number'], as_index=False)[['Txn_Amount', 'Profit_Amount', 'Total_Txns']].sum()
    z = (df1[df1.Month_Number == mnth])
    m_am = round((df1[['Txn_Amount']][df1.Month_Number == mnth][df1.Year_Number == yr]).get('Txn_Amount'))
    p_am = round((df1[['Profit_Amount']][df1.Month_Number == mnth][df1.Year_Number == yr]).get('Profit_Amount'))
    m_txn = (df1[['Total_Txns']][df1.Month_Number == mnth][df1.Year_Number == yr]).get('Total_Txns')
    m_avg = round(m_am /m_txn)

    fig1 = px.bar(z, x = 'Year_Number', y= 'Txn_Amount', barmode='group', text='Txn_Amount', color_continuous_scale=px.colors.cyclical.Phase, title=f'Yearly Comparision {x}')
    fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)'
                      })
    fig1.update_xaxes(title_text='Year_Number', color='black', showgrid=False)
    fig1.update_yaxes(title_text='Amount', color='black', showgrid=False)
    fig1.update_traces(texttemplate='%{text:.3s}', textposition='outside')

    return yx1,yx2,j,n, yx1,yx2,x1,x2, yx1,yx2,t1,t2,yx1,yx2,a1,a2,fig, y, fig1,m_am, p_am,m_txn, m_avg


@app.callback([Output(component_id='m_header_year', component_property='children'),Output(component_id='y_am', component_property='children'),Output(component_id='y_pm', component_property='children'),
     Output(component_id='y_txn', component_property='children'),Output(component_id='y_avg', component_property='children'),Output(component_id='mnth_grph1', component_property='figure'),
     Output(component_id='m_fig3', component_property='figure'),
     Input(component_id='yr', component_property='value'),Input(component_id='mnth1', component_property='value'),Input(component_id='yr2', component_property='value')])
def updated1(yr, mnth1,yr2):
    df1 = df_1.copy()
    m_header = (f'Fy : {yr}')
    y_am = round((df1[['Txn_Amount']][df1.Type == 'Dmt'][df1.Year_Number == yr]).sum()).get('Txn_Amount')
    y_pm= round((df1[['Profit_Amount']][df1.Type == 'Dmt'][df1.Year_Number == yr]).sum()).get('Profit_Amount')
    y_txn = ((df1[['Total_Txns']][df1.Type == 'Dmt'][df1.Year_Number == yr]).sum()).get('Total_Txns')
    y_avg = round(y_am / y_txn)

    y_am1 = (df1[['Txn_Amount']][df1.Type == 'Dmt'][df1.Year_Number == yr]).get('Txn_Amount')
    mnthn = (df1[['Month_Number']][df1.Type == 'Dmt'][df1.Year_Number == yr]).get('Month_Number')

    fig2 = px.bar(x=mnthn, y=y_am1, text=y_am1, orientation='v', hover_data=[y_am1],
                 template='plotly_dark', labels={''},)
    fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig2.update_xaxes(title_text='Month Number', color='black', showgrid=False)
    fig2.update_yaxes(title_text='Amount', color='black', showgrid=False)
    fig2.update_traces(texttemplate='%{text:.4s}')

    z = df1[df1.Month_Number.isin(mnth1)][df1.Year_Number.isin(yr2)][df1.Type == 'Dmt']

    x = z.groupby(['Year_Number'], as_index=False)[['Txn_Amount']].sum()

    t2021 = (x[['Txn_Amount']][x.Year_Number == 2021])
    t2020 = (x[['Txn_Amount']][x.Year_Number == 2020])
    t2019 = (x[['Txn_Amount']][x.Year_Number == 2019])

    fig3 = px.line(x, x='Year_Number', y='Txn_Amount', text='Txn_Amount', width =1250 ,height=370)
    fig3.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig3.update_xaxes(title_text='Year Number', color='black', showgrid=False, type = 'category')
    fig3.update_yaxes(title_text='Amount', color='black', showgrid=False)
    fig3.update_traces(texttemplate='%{text:.4s}')
    t21 = []
    t20 = []
    t19 = []

    for i in t2021['Txn_Amount']:
        t21.append(i)
    for i in t2020['Txn_Amount']:
        t20.append(i)
    for i in t2019['Txn_Amount']:
        t19.append(i)

    if t21 < t20 :
        fig3.update_traces(fill ='tozeroy',line={'color': 'red'})
    elif t21 < t19:
        fig3.update_traces(fill ='tozeroy',line={'color': 'red'})
    elif t21 > t20 :
        fig3.update_traces(fill ='tozeroy',line={'color': 'green'})
    elif t21 > t19:
        fig3.update_traces(fill ='tozeroy',line={'color': 'green'})
    elif t20 < t19 :
        fig3.update_traces(fill ='tozeroy',line={'color': 'red'})
    elif t20 > t19:
        fig3.update_traces(fill ='tozeroy',line={'color': 'green'})


    return m_header, y_am, y_pm, y_txn, y_avg, fig2, fig3


@app.callback([
    Output(component_id='fig4', component_property='figure'),
   Input(component_id='mnth2', component_property='value'),Input(component_id='yr3', component_property='value')
])
def updated2(mnth2, yr3):
    df1 = df_1.copy()
    z = df1[df1.Month_Number.isin([mnth2])][df1.Year_Number.isin([yr3])][df1.Type == 'Dmt']
    x = z.groupby(['Year_Number'], as_index=False)[['Txn_Amount']].sum()
    print(x)
    fig4 = px.line(x, x='Year_Number', y='Txn_Amount', text='Txn_Amount')
    fig4.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                        'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig4.update_xaxes(title_text='Year Number', color='black', showgrid=False)
    fig4.update_yaxes(title_text='Amount', color='black', showgrid=False)
    fig4.update_traces(texttemplate='%{text:.4s}')

    return fig4


@app.callback([
    Output(component_id='qtr_am', component_property='figure'),Output(component_id='qtr_txn', component_property='figure'),
    Input(component_id='dw_yr', component_property='value'),Input(component_id='dw_qtr', component_property='value')
])
def updated4(yr,qtr):
    a = df_qtr
    a = a.sort_values('Quarter_No')
    a = a[a.Year_No == yr]

    fig_qtr_am = px.bar(a, x = 'Quarter_No', y = 'Txn_Amount', height=250).update_layout(margin=dict(t=0, r=0, l=0, b=0))
    fig_qtr_am.update_layout(yaxis = dict(showgrid = False),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',)
    fig_qtr_am.update_layout(xaxis = dict(showgrid = False))
    fig_qtr_am.update_xaxes(type='category')

    b = df_qtr
    b = b.sort_values('Year_No')
    b = b[b.Quarter_No == qtr]

    fig_qtr_txn = px.bar(b, x='Year_No', y='Txn_Amount', height=250).update_layout(margin=dict(t=0, r=0, l=0, b=0))
    fig_qtr_txn.update_layout(yaxis = dict(showgrid = False),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',)
    fig_qtr_txn.update_layout(xaxis = dict(showgrid = False))
    fig_qtr_txn.update_xaxes(type = 'category')
    fig_qtr_txn.update_yaxes(title_text='Txn_Amount', color='black', showgrid=False)
    # fig_qtr_txn.update_traces(texttemplate='%{text:.2s}', textposition='outside')


    return fig_qtr_am,fig_qtr_txn














