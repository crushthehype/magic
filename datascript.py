### if you're not excited - get excited ###

### education is something you can't finish ###

# This is a naive script
# Please give feedback to me -> crushlabs@protonmail.com
# This script:
    # pulls trade data from www.bitmex.com
    # pulls data from www.blockchain.com 
    # merges pulled data on daily timestamp to dataframe

# Have fun, be fun
# ridethehype

import requests
import pandas as pd 
import numpy as np 
import datetime
from bitmex import bitmex

transactions = requests.get('https://api.blockchain.info/charts/n-transactions?timespan=all&format=json&sampled=false') # confirmed transactions per day
transactions.status_code # if 200 - success, else - fail
tx = transactions.json() # to json
tx_values = tx['values'] # get only values
type(tx_values) # confirm type
df = pd.DataFrame(tx_values) # to dataframe
df['x'] = pd.to_datetime(df['x'], unit = 's') # to datetime
df.columns = ['timestamp', 'transactions'] # name columns as you wish
df = df[df['timestamp']>='2015-09-30'] # filter your data
df.set_index('timestamp', inplace = True) # set your indexes
df.info() # know your data
df.head(3) # verify what you see
df.tail(3) # keep verifying what you see

txCostUSD = requests.get('https://api.blockchain.info/charts/cost-per-transaction?timespan=all&format=json&sampled=false') # transaction cost USD
txCostUSD.status_code # if 200 - success, else - fail
costUSD = txCostUSD.json() # to json
cost_values = costUSD['values'] # get only values
type(cost_values) # confirm type
df4 = pd.DataFrame(cost_values) # to dataframe
df4['x'] = pd.to_datetime(df4['x'], unit = 's') # to datetime
df4.columns = ['timestamp', 'txCostUSD'] # name columns as you wish
df4 = df4[df4['timestamp']>='2015-09-30'] # filter your data
df4.set_index('timestamp', inplace = True) # set your indexes
df4.info() # know your data
df4.head(3) # verify what you see
df4.tail(3) # keep verifying what you see

uniqueAdresses = requests.get('https://api.blockchain.info/charts/n-unique-addresses?timespan=all&format=json&sampled=false') # transaction cost USD
uniqueAdresses.status_code # if 200 - success, else - fail
uniques = uniqueAdresses.json() # to json
nUniques_values = uniques['values'] # get only values
type(nUniques_values) # confirm type
df5 = pd.DataFrame(nUniques_values) # to dataframe
df5['x'] = pd.to_datetime(df5['x'], unit = 's') # to datetime
df5.columns = ['timestamp', 'uniqueAddresses'] # name columns as you wish
df5 = df5[df5['timestamp']>='2015-09-30'] # filter your data
df5.set_index('timestamp', inplace = True) # set your indexes
df.info() # know your data
df5.head(3) # verify what you see
df5.tail(3) # keep verifying what you see

estTxVolUSD = requests.get('https://api.blockchain.info/charts/estimated-transaction-volume-usd?timespan=all&format=json&sampled=false') # est tx volume USD
estTxVolUSD.status_code # if 200 - success, else - fail
txVolUSD = estTxVolUSD.json() # to json
txVolUSD_values = txVolUSD['values'] # get only values
type(txVolUSD_values) # confirm type
df6 = pd.DataFrame(txVolUSD_values) # to dataframe
df6['x'] = pd.to_datetime(df6['x'], unit = 's') # to datetime
df6.columns = ['timestamp', 'txVolUSD'] # name columns as you wish
df6 = df6[df6['timestamp']>='2015-09-30'] # filter your data
df6.set_index('timestamp', inplace = True) # set your indexes
df6.info() # know your data
df6.head(3) # verify what you see
df6.tail(3) # keep verifying what you see

t = datetime.datetime.strptime("2015-10-1T00:00:00+0100", "%Y-%m-%dT%H:%M:%S%z") # set start time for 1st 1k values
t1 = datetime.datetime.strptime("2018-06-27T00:00:00+0100", "%Y-%m-%dT%H:%M:%S%z") # set start time for 2nd 1k values
client = bitmex(test=False) # connect to client
r = client.Trade.Trade_getBucketed(symbol = 'XBTUSD', binSize='1d', startTime = t, count=1000).result() # get data 1st 1k values
r1 = client.Trade.Trade_getBucketed(symbol = 'XBTUSD', binSize='1d', startTime = t1, count=1000).result() # get data 2nd 1k values

df1 = pd.DataFrame(list(r[0])) # to dataframe 
df1.timestamp = df1.timestamp + pd.DateOffset(days=-1) # THIS IS IMPORTANT # confirm OHCL with tradinview or any other broker you use
df1.head(3) # verify what you see
df1.tail(3) # keep verifying what you see

df2 = pd.DataFrame(list(r1[0]))  # to dataframe 
df2.timestamp = df2.timestamp + pd.DateOffset(days=-1) # THIS IS IMPORTANT # confirm OHCL with tradinview or any other broker you use
df2.head(3) # verify what you see
df2.tail(3) # keep verifying what you see

df1['timestamp'] = df1['timestamp'].dt.strftime('%Y-%m-%d') # convert to datetime
df2['timestamp'] = df2['timestamp'].dt.strftime('%Y-%m-%d') # convert to datetime

df3 = df1.append(df2) # append dataframes from BitMEX
df3.set_index('timestamp', inplace = True) # set your indexes
df3 = df3[['open', 'high', 'low', 'close', 'trades', 'volume', 'vwap']] # selct values you want to your dataframe

df3.head(3) # verify what you see
df3.tail(3) # keep fucking verifying what you see

df3.index = pd.to_datetime(df3.index) # index to datetime 

merged = df3.merge(df, on = 'timestamp') # merge 
merge_1 = merged.merge(df4, on = 'timestamp') # keep merging 
merge_2 = merge_1.merge(df5, on = 'timestamp') # keep merging 
merge_3 = merge_2.merge(df6, on = 'timestamp') # keep merging

data = merge_3 # change the name

data.head(3) # verify what you see
data.tail(3) # keep verifying what you see
data.info() # know your data

# end