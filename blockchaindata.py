### 'education is something you don't want't to finish' ###
# crushlabs@protonmail.com
# learn, analyse, give feedback

import requests
import pandas as pd 
import numpy as np 
import datetime
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots


hashRate = requests.get('https://api.blockchain.info/charts/hash-rate?timespan=all&format=json&sampled=false') # confirmed transactions per day
hashRate.status_code # if 200 - success, else - fail
hr = hashRate.json() # to json
hr_values = hr['values'] # get only values
type(hr_values)
df = pd.DataFrame(hr_values)
df['x'] = pd.to_datetime(df['x'], unit = 's')
df.columns = ['timestamp', 'hashrate']
df = df[df['timestamp']>='2019-01-01']
df.set_index('timestamp', inplace = True)
df['hashrate'] = df['hashrate']/1000000
df['std'] = df['hashrate'].rolling(7).std()
df.head(3)
df.tail(3)


txCostUSD = requests.get('https://api.blockchain.info/charts/cost-per-transaction?timespan=all&format=json&sampled=false') # transaction cost USD
txCostUSD.status_code # if 200 - success, else - fail
costUSD = txCostUSD.json() # to json
cost_values = costUSD['values'] # get only values
type(cost_values)
df4 = pd.DataFrame(cost_values)
df4['x'] = pd.to_datetime(df4['x'], unit = 's')
df4.columns = ['timestamp', 'txCostUSD']
df4['median'] = df4['txCostUSD'].rolling(7).median()
df4 = df4[df4['timestamp']>='2019-01-01']
df4.set_index('timestamp', inplace = True)
df4.head(3)
df4.tail(3)

avgtperblock = requests.get('https://api.blockchain.info/charts/n-transactions-per-block?timespan=all&format=json&sampled=false') # average transactions per block
avgtperblock.status_code # if 200 - success, else - fail
txperblock = avgtperblock.json() # to json
tx_values = txperblock['values'] # get only values
type(tx_values)
df2 = pd.DataFrame(tx_values)
df2['x'] = pd.to_datetime(df2['x'], unit = 's')
df2.columns = ['timestamp', 'avgtxperblock']
df2 = df2[df2['timestamp']>='2019-01-01']
df2.set_index('timestamp', inplace = True)
df2.head(3)
df2.tail(3)

tradevolusd = requests.get('https://api.blockchain.info/charts/trade-volume?timespan=all&format=json&sampled=false') # trade-volume
tradevolusd.status_code # if 200 - success, else - fail
volusd = tradevolusd.json() # to json
volusd_values = volusd['values'] # get only values
type(volusd_values)
df3 = pd.DataFrame(volusd_values)
df3['x'] = pd.to_datetime(df3['x'], unit = 's')
df3.columns = ['timestamp', 'tradevolusd']
df3 = df3[df3['timestamp']>='2019-01-01']
df3.set_index('timestamp', inplace = True)
df3['tradevolusd'] = df3['tradevolusd']/1000000
df3['median'] = df3['tradevolusd'].rolling(7).median()
df3.head(3)
df3.tail(3)

title1 = 'The estimated number of tera hashes per second the Bitcoin network is performing'
title2 = 'A chart showing miners revenue divided by the number of transactions (USD)'
title3 = 'The average number of transactions per block'
title4 = 'The total USD value of trading volume on major bitcoin exchanges (Mln)'



fig = make_subplots(rows=2, cols=2, subplot_titles=(title1, title2, title3, title4))

for i in fig['layout']['annotations']:
    i['font'] = dict(size=12,color='rgb(51, 51, 77)')

fig.append_trace(go.Scatter(x=df.index,y=df.hashrate, name = 'Hashrate', marker = dict(color='rgb(71, 71, 107)'), showlegend=False), row=1, col=1)
fig.append_trace(go.Scatter(x=df.index,y=df['std'], name = '7d stdev', marker = dict(color='rgb(102, 140, 255)')), row=1, col=1)
fig.append_trace(go.Bar(x=df4.index,y=df4.txCostUSD, name = 'txCostUSD', marker = dict(color='rgb(71, 71, 107)'), showlegend=False), row=1, col=2)
fig.append_trace(go.Scatter(x=df4.index,y=df4['median'], name = '7d roll median', marker = dict(color='rgb(0, 45, 179)')), row=1, col=2)
fig.append_trace(go.Scatter(x=df2.index,y=df2['avgtxperblock'], name = 'avg tx per block', marker = dict(color='rgb(71, 71, 107)'), showlegend=False), row=2, col=1)
fig.append_trace(go.Bar(x=df3.index,y=df3['tradevolusd'], name = 'trade volume usd', marker = dict(color='rgb(71, 71, 107)'), showlegend=False), row=2, col=2)
fig.append_trace(go.Scatter(x=df3.index,y=df3['median'], name = '7d roll median', marker = dict(color='rgb(0, 45, 179)'), showlegend = False), row=2, col=2)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title = 'Blockchain data', title_x = 0.5)
fig.write_html('crypto.html', auto_open=True)

# end