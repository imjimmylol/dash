from tkinter.tix import InputOnly
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from utils.data_process import input_process, res_process
from utils.search import return_res


# data = pd.read_csv(r"./data/2330TW.csv")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")

app = dash.Dash(__name__, 
    external_stylesheets=[dbc.themes.SOLAR]
    )

app.layout = html.Div(
    html.Div([

        html.Div([
            dcc.DatePickerRange(
                id=''        
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                alendar_orientation='vertical',
            )

        ])


    ])

)


@app.callback(
    Output('test', 'figure'),
    Input('Ticker', 'value'),
    Input('StartDate', 'value'),
    Input('EndDate', 'value')
    )

def update_graph_shaped(Ticker, StartDate, EndDate):
    
    # read data
    df = pd.read_csv(r"./data/{}TW.csv".format(Ticker))

    # transform date to index
    s, e = input_process.DateIndexMap(df, StartDate), input_process.DateIndexMap(df, EndDate)

    # search and return res
    search_res = return_res.get_sim_res(df, s, e, 'shape_d') # a:b
    

    # get res start and end
    s_res, e_res = res_process.range_2_num(search_res)

    return{
        plotly_plot.plot(df, s = s_res, e= e_res)
    }
