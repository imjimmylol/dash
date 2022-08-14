from datetime import datetime
from distutils.log import debug
from tkinter.tix import InputOnly
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

# data = pd.read_csv(r"./data/2330TW.csv")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")

app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.SOLAR],
                    meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
    )

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range-baseline',        
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                start_date = date(2021, 1, 20),
                end_date = date(2021, 2, 5)
            ),
            dcc.Dropdown(
                id='ticker-dropdown-option',
                value="2330TW",
                options=[{'label':t, 'value':t}
                for t in list(map(lambda x :re.sub('.csv','',x), next(walk("./data"), (None, None, []))[2] ))]
            )
        ]),

    html.Div([

        dcc.Graph(id="test")


    ])


    ])

])


@app.callback(
    Output('test', 'figure'),
    [Input('ticker-dropdown-option', 'value'),
    Input('date-picker-range-baseline', 'start_date'),
    Input('date-picker-range-baseline', 'end_date')])

def update_graph_shaped(Ticker, start_date, end_date):
    
    # read data
    df = pd.read_csv(r"./data/{}.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, start_date), input_process.DateIndexMap(df, end_date)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'shape_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)

    return(
        plotly_plot.plot(df, s = s_res, e= e_res)
    )

if __name__ == '__main__':
    app.run_server(debug=True)