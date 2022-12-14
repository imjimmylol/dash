from re import template
import pandas as pd
from utils.algo.calculation import get_fbna
from dash_bootstrap_templates import load_figure_template
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import talib

templates = ["solar"]
load_figure_template(templates)

def plot(df, s, e, step):
    df = pd.DataFrame(df)
    df['k'], df['d'] = talib.STOCH(df['High'], df['Low'], df['Close'])
    df['k'].fillna(value=0, inplace=True)
    df['d'].fillna(value=0, inplace=True)

    df['diff'] =df['Close'] - df['Open']
    df.loc[df['diff']>=0, 'color'] = 'green'
    df.loc[df['diff']<0, 'color'] = 'red'
    l1,l2,l3,l4,l5 = get_fbna(min(df['Low'][s:e]),max(df['High'][s:e]))


    fig = make_subplots(

    rows = 8, cols = 1,

    specs = [[{"rowspan": 4, "secondary_y": True}],
            [None],
            [None],
            [None],
            [{"rowspan":2}],
            [None],
            [{"rowspan":2}],
            [None]],

    print_grid=False, shared_xaxes=True, vertical_spacing=0.05
)
##########################################################

    # condle
    fig.add_trace(go.Candlestick(x=df['Date'][s-step:e+step],
                                open=df['Open'][s-step:e+step],
                                high=df['High'][s-step:e+step],
                                low=df['Low'][s-step:e+step],
                                close=df['Close'][s-step:e+step],
                                name="Price", 
                                ), secondary_y=False, row = 1, col = 1)
    # candle partition
    fig.update_yaxes(range=[min(df['Low'][s-step:e+step])*0.975, max(df["High"][s-step:e+step]*1.025)], row=1, col=1, title_text = "Candle")
    fig.add_hline(y = l1,line_dash="dot",row = 1, col=1, line_color = '#ff7f0e')
    fig.add_hline(y = l2,line_dash="dot",row = 1, col=1, line_color = '#8c564b')
    fig.add_hline(y = l3, line_dash="dot",row = 1, col=1, line_color ='#9467bd')
    fig.add_hline(y = l4, line_dash="dot", row = 1, col=1, line_color = '#bcbd22')
    fig.add_hline(y = l5, line_dash="dot", row = 1, col=1, line_color = '#1f77b4')
    
    fig.add_vrect(x0=df['Date'][s], x1=df['Date'][e], annotation_text="search result", row = 1, col=1)

    # volume subplot
    fig.add_trace(go.Bar(x=df['Date'][s-step:e+step], y=df['Volume'][s-step:e+step], name='Volume', marker={'color':df['color']}),  row = 5, col = 1)
    fig.update_yaxes(title_text = "Vloume", row=5, col=1)

    # KD subplot
    fig.add_trace(go.Scatter(x=df['Date'][s-step:e+step], y = df["k"][s-step:e+step], name = "k", mode='lines'), row=7, col=1)
    fig.add_trace(go.Scatter(x=df['Date'][s-step:e+step], y = df["d"][s-step:e+step], name = "d", mode='lines'), row=7, col=1)
    fig.update_yaxes(title_text = "KD", row=7, col=1)


    fig.update_layout(autosize=False,
        width=1000*0.5,
        height=700*0.7,title_font_size = 1,xaxis_rangeslider_visible=False, xaxis2_rangeslider_visible=False,
        xaxis3_rangeslider_visible=False, template='solar') 

    return fig



def plot_all(df):
    fig = go.Figure()
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
    ),template="solar"
    )

    return fig