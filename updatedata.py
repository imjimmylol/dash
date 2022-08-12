from ast import arg
from turtle import st
from unicodedata import name
import yfinance as yf
import argparse
import re

# input params
parser = argparse.ArgumentParser()
parser.add_argument('-s' , '--start',
    default='2008-01-01',
    help='start date',
    type=str
)
parser.add_argument('-t', '--ticker',
    default='2330.TW',
    help='stock ticker e.g 2330.TW',
    type=str
)

args = parser.parse_args()

def update_csv(start_date , stock_no):
    
    # get data
    stock = yf.Ticker(stock_no)
    stock_data = stock.history(start=start_date)

    # output csv
    tick = args.ticker.replace(".", "")
    stock_data.to_csv('./data/{}.csv'.format(tick))
    return print('done')

if __name__=="__main__":
    update_csv(start_date = args.start, stock_no=args.ticker)