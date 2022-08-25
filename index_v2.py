from datetime import datetime
from distutils.log import debug
from pydoc import classname
from tkinter.tix import InputOnly
from tkinter.ttk import Style
from turtle import st, width
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
from utils.data_process import input_process, res_process
from utils.search import return_res
from utils.plot import plotly_plot
from datetime import date
from os import walk
import re


# https://hackerthemes.com/bootstrap-cheatsheet/ <- get boostrap here
app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.SOLAR],
                    meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
    )

app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(html.H1("Similarity Algorisom Dashboard"), 
        className='text-xl-center', width=100)
    ]),

    dbc.Row([
        dbc.Col([

            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Ticker and Time selection")
                    ], className="card-title"),
                    
                    html.Div([
                        dcc.Dropdown(
                        id='ticker-dropdown-option',
                        value="2330TW",
                        options=[{'label':t, 'value':t}
                        for t in list(map(lambda x :re.sub('.csv','',x), next(walk("./data"), (None, None, []))[2] ))],
                    )

                    ], className="dropdown", style={"width": "100%"}),#, style={"width": "20%"}

                    html.Br(),

                    html.Div([
                        dcc.DatePickerRange(
                            id='date-picker-range-baseline',        
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            start_date = date(2021, 1, 20),
                            end_date = date(2021, 2, 5)
                        )
                    ], className="dropdown", style={"width": "100%"}),
                    
                    html.Br(),

                    html.Button('Submit change', id='update-button')


                ], className="card-body")

            ], className="card border-primary mb-3 text-xl-center")

        ], width=2),    # xs = 30

        dbc.Col([
            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Search For Your Goal Interval")
                    ], className="card-title"),

                    html.Div([
                        dcc.Loading(children=[dcc.Graph(id="full-wav-plot")])
                    ])

                ], className="card-body")

            ], className="card border-primary mb-3 text-xl-center"),
        ])
    ], '''# width=6'''), # , width=6

    dbc.Row([

        dbc.Col([

            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Search Result From Different Algorisim")
                    ], className="card-title"),

                ], className="card-body")

            ], className="card border-primary mb-3 text-xl-center"),




        ]),

    ]),
    dbc.Row([

        dbc.Col([
            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Correlation Coefficient : ")
                    ], className="card-title"),
                    
                    html.Div([
                        dcc.Loading(children=[dcc.Graph(id="searh-result-corr")])
                    ])

                ], className="card-body")

            ], className="card border-primary mb-3"),          

        ]),

        dbc.Col([

            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Minks Distance : ")
                    ], className="card-title"),
                    
                    html.Div([
                       dcc.Loading(children=[dcc.Graph(id="searh-result-mink")])
                    ])

                ], className="card-body")

            ], className="card border-primary mb-3"),
        ]),

    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Dtnamic Time Wraping : ")
                    ], className="card-title"),
                    
                    html.Div([
                        dcc.Loading(children=[dcc.Graph(id="searh-result-dtw")])
                    ])

                ], className="card-body")

            ], className="card border-primary mb-3"),




        ]),

        dbc.Col([
            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Shape-Based Similarity : ")
                    ], className="card-title"),
                    
                    html.Div([
                        dcc.Loading(children=[dcc.Graph(id="searh-result-shape")])
                    ])

                ], className="card-body")

            ], className="card border-primary mb-3"),  
        ])
    ]),

    dbc.Row([
        dbc.Col([
            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Polynomial Similarity : ")
                    ], className="card-title"),
                    
                    html.Div([
                        dcc.Loading(children=[dcc.Graph(id="searh-result-poly")])
                    ])

                ], className="card-body")

            ], className="card border-primary mb-3"),  
        ]),


        dbc.Col([

            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Polynomial Similarity cos: ")
                    ], className="card-title"),
                    
                    html.Div([
                        dcc.Loading(children=[dcc.Graph(id="searh-result-polycos")])
                    ])

                ], className="card-body")

            ], className="card border-primary mb-3"), 
        ])
        ]),
       
    ])

@app.callback(
    Output('full-wav-plot', 'figure'),
    [Input('ticker-dropdown-option', 'value')])

def update_graph_full(Ticker):
    # read data
    # print(Ticker)
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    return (plotly_plot.plot_all(df))



@app.callback(
    Output('searh-result-corr', 'figure'),
    [Input('update-button', component_property='n_clicks'),
    State('ticker-dropdown-option', 'value'),
    State('date-picker-range-baseline', 'start_date'),
    State('date-picker-range-baseline', 'end_date')]
)

def update_graph_corr_res(n,Ticker, start_date, end_date, step=5):

    # read data
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'corr_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)

    return(
        plotly_plot.plot(df, s_res = s_res, e_res= e_res, step = step)
    )

@app.callback(
    Output('searh-result-mink', 'figure'),
    [Input('update-button', component_property='n_clicks'),
    State('ticker-dropdown-option', 'value'),
    State('date-picker-range-baseline', 'start_date'),
    State('date-picker-range-baseline', 'end_date')]
)

def update_graph_mink_res(n,Ticker, start_date, end_date, step=5):

    # read data
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'mink_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)

    return(
        plotly_plot.plot(df, s_res = s_res, e_res= e_res, step = step)
    )


@app.callback(
    Output('searh-result-dtw', 'figure'),
    [Input('update-button', component_property='n_clicks'),
    State('ticker-dropdown-option', 'value'),
    State('date-picker-range-baseline', 'start_date'),
    State('date-picker-range-baseline', 'end_date')]
)

def update_graph_shape_res(n,Ticker, start_date, end_date, step=5):

    # read data
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'dtw_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)

    return(
        plotly_plot.plot(df, s_res = s_res, e_res= e_res, step = step)
    )




@app.callback(
    Output('searh-result-shape', 'figure'),
    [Input('update-button', component_property='n_clicks'),
    State('ticker-dropdown-option', 'value'),
    State('date-picker-range-baseline', 'start_date'),
    State('date-picker-range-baseline', 'end_date')]
)

def update_graph_shape_res(n, Ticker, start_date, end_date, step=5):

    # read data
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'shape_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)
    print(s_res, e_res)
    return(
        plotly_plot.plot(df, s_res = s_res, e_res= e_res, step = step)
    )

@app.callback(
    Output('searh-result-poly', 'figure'),
    [Input('update-button', component_property='n_clicks'),
    State('ticker-dropdown-option', 'value'),
    State('date-picker-range-baseline', 'start_date'),
    State('date-picker-range-baseline', 'end_date')]
)

def update_graph_poly_res(n, Ticker, start_date, end_date, step=5):

    # read data
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'poly_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)
    print(s_res, e_res)
    return(
        plotly_plot.plot(df, s_res = s_res, e_res= e_res, step = step)
    )


@app.callback(
    Output('searh-result-polycos', 'figure'),
    [Input('update-button', component_property='n_clicks'),
    State('ticker-dropdown-option', 'value'),
    State('date-picker-range-baseline', 'start_date'),
    State('date-picker-range-baseline', 'end_date')]
)

def update_graph_poly_res(n, Ticker, start_date, end_date, step=5):

    # read data
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'polycos_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)
    print(s_res, e_res)
    return(
        plotly_plot.plot(df, s_res = s_res, e_res= e_res, step = step)
    )


if __name__ == '__main__':
    app.run_server(debug=True)