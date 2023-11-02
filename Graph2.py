import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


tesla = yf.Ticker('TSLA')

tesla_data = tesla.history(period = 'max')


url = ' https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
data  = requests.get(url).text

beautiful_soup = BeautifulSoup(data, 'html5lib')

read_html_pandas_data = pd.read_html(str(beautiful_soup))    
tesla_revenue = read_html_pandas_data[1]
tesla_revenue["Date"] = tesla_revenue[['Tesla Quarterly Revenue(Millions of US $)']]
tesla_revenue["Revenue"] = tesla_revenue[['Tesla Quarterly Revenue(Millions of US $).1']]
tesla_revenue
new_tesla_revenue = tesla_revenue[["Date", "Revenue"]]
new_tesla_revenue

new_tesla_revenue["Revenue"] = new_tesla_revenue['Revenue'].str.replace(',|\$',"")

new_tesla_revenue.dropna(inplace=True)

new_tesla_revenue = new_tesla_revenue[new_tesla_revenue['Revenue'] != ""]

new_tesla_revenue.tail()


gamestock = yf.Ticker("GME")

gme_data = gamestock.history(period="max")

gme_data.reset_index(inplace=True)
gme_data.head()


url = ' https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue.'
data  = requests.get(url).text

beautiful_soup = BeautifulSoup(data, 'html5lib')

read_html_pandas_data = pd.read_html(str(beautiful_soup))    
gme_revenue = read_html_pandas_data[1]
gme_revenue["Date"] = gme_revenue["GameStop Quarterly Revenue(Millions of US $)"]
gme_revenue["Revenue"] = gme_revenue["GameStop Quarterly Revenue(Millions of US $).1"]
gme_revenue
new_gme_revenue = gme_revenue[["Date", "Revenue"]]
new_gme_revenue

new_gme_revenue["Revenue"] = new_gme_revenue['Revenue'].str.replace(',|\$',"")
new_gme_revenue.dropna(inplace=True)
new_gme_revenue = new_gme_revenue[new_gme_revenue['Revenue'] != ""]
new_gme_revenue.tail()


make_graph(tesla_data, new_tesla_revenue, 'Tesla')


make_graph(gme_data, new_gme_revenue, 'GameStop')
