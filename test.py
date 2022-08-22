from re import template
import pandas as pd
from utils.algo.calculation import get_fbna
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import talib
import pandas as pd
import time
import threading

templates = ["solar"]
load_figure_template(templates)

df = pd.read_csv("./data/2317TW.csv")

fuck = []


def clear_timeli():
    while True:
        if len(fuck)>2:
            fuck = []



fig = go.FigureWidget(go.Figure())
fig.add_trace(go.Candlestick(x=df["Date"],
                            open=df['Open'],
                            high=df['High'],
                            low=df['Low'],
                            close=df['Close'],
                            name="Price", 
                            ))
fig.update_layout(
    yaxis = dict(
       autorange = True,
       fixedrange= False
   ), width=1000*0.7,height=700*0.8,template="solar"
)

scatter = fig.data[0]
def log_date(trace, points, selector):
    global fuck
    date = list(scatter.x)
    for i in points.point_inds:
        fuck.append(date[i])

scatter.on_click(log_date)
fig
t = threading.Thread(target = clear_timeli)
t.start()
print(fuck)