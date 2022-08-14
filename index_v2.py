from datetime import datetime
from distutils.log import debug
from pydoc import classname
from tkinter.tix import InputOnly
from tkinter.ttk import Style
from turtle import width
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
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
                        html.H4("Ticker and Time Range selection")
                    ], className="card-title"),
                    
                    html.Div([
                        dcc.Dropdown(
                        id='ticker-dropdown-option',
                        value="2330TW",
                        options=[{'label':t, 'value':t}
                        for t in list(map(lambda x :re.sub('.csv','',x), next(walk("./data"), (None, None, []))[2] ))]
                    )

                    ], className="dropdown", style={"width": "25%"})



                ], className="card-body")

            ], className="card border-primary mb-3 text-xl-center")

        ]),
    ]),

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
                    

                ], className="card-body")

            ], className="card border-primary mb-3"),          

        ]),

        dbc.Col([

            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Minks Distance : ")
                    ], className="card-title"),
                    

                ], className="card-body")

            ], className="card border-primary mb-3"),
        ]),

        dbc.Col([
            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Dtnamic Time Wraping : ")
                    ], className="card-title"),
                    

                ], className="card-body")

            ], className="card border-primary mb-3"),




        ]),

        dbc.Col([
            html.Div([
                
                html.Div([

                    html.Div([
                        html.H4("Shape-Based Similarity : ")
                    ], className="card-title"),
                    
                    

                ], className="card-body")

            ], className="card border-primary mb-3"),  
        ])

    ]),

    dbc.Row([

    ])
])

# @app.callback(
#     Output('test', 'figure'),
#     [Input('ticker-dropdown-option', 'value'),
#     Input('date-picker-range-baseline', 'start_date'),
#     Input('date-picker-range-baseline', 'end_date')])

# def update_graph_shaped(Ticker, start_date, end_date):
    
#     # read data
#     df = pd.read_csv(r"./data/{}.csv".format(Ticker))

#     # transform date to index
#     s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

#     # search and return res
#     search_res = return_res.get_sim_res(df, s, e, 'mink_d') # a:b
    

#     # get res start and end
#     s_res, e_res = res_process.range_2_num(search_res)

#     return(
#         plotly_plot.plot(df, s = s_res, e= e_res)
#     )

if __name__ == '__main__':
    app.run_server(debug=True)