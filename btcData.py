import pandas as pd 
import numpy as np 
from bitmex import bitmex
import plotly.graph_objects as go 
import dash 
import dash_core_components as dcc 
import dash_html_components as html
import matplotlib.pyplot as plt
import datetime
from plotly.subplots import make_subplots

t = datetime.datetime.strptime("2017-09-30T00:00:00+0100", "%Y-%m-%dT%H:%M:%S%z")
client = bitmex(test=False)
r = client.Trade.Trade_getBucketed(symbol = 'XBTUSD', binSize='1d', startTime = t, count=1000).result()

df = pd.DataFrame(list(r[0])).reset_index()
df.timestamp = df.timestamp + pd.DateOffset(days=-1)
df.head()
df.tail()

df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')

df['return'] = np.log(df['close']/df['close'].shift(1))
df = df[df['timestamp']>='2017-10-01']


def SetColor(b):
    if(b==0):
        return "blue"
    elif(b<0):
        return "red"
    elif(b>0):
        return "green"


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dcc.Graph(
        id='close price',
        figure={
            'data': [
                {'x': df.timestamp, 
                'y': df.close, 
                'type': 'scatter', 
                'name': 'XBTUSD close price'}],
                'layout': {'title': 'XBTUSD close price', 'height': '800'}}),
    dcc.Graph(
        id='returns',
        figure={
            'data': [
                {'x': df.timestamp, 
                'y': df['return'], 
                'type': 'bar', 
                'name': 'XBTUSD returns', 
                'marker': dict(color=list(map(SetColor,df['return'])))}],
                'layout': {'title': 'XBTUSD returns', 'height': '600'}})])            

if __name__ == '__main__':
    app.run_server(debug=True)
