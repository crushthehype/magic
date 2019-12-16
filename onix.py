import bitmex
import pandas as pd 
import numpy as np 
import requests, json
import lxml
apiKey = ''
apiSecret = ''

# Connecting to client
client = bitmex.bitmex(test = False, api_key=apiKey, api_secret=apiSecret)
# fetching trade execution history
r = client.Execution.Execution_getTradeHistory().result()
d = pd.DataFrame(list(r[0]))
cols = list(d.columns.str.lower())


# get data from ONIXS for dictionary
df = pd.read_html('https://www.onixs.biz/fix-dictionary/5.0.SP2/msgType_8_8.html', skiprows=5)[0]
df.columns = df.iloc[0]
df = df.iloc[2:]
df.head()
df.tail()
# lowercase the values of field name to match Onixs dictionary
df['Field Name'] = df['Field Name'].str.lower()

# individual search - just type what you're looking for
x = 'timeinforce'
result = df.loc[df['Field Name'] == x]
result = list(result.values)
row = result[0][0]
tag = result[0][1]
required  = result[0][2]
desc = result[0][3]
print('Row: ' + row, 'Tag: ' + tag , 'Required: ' + required, 'Description: ' + desc, sep = '\n')

# match the execution history columns to Onixs dictionary
match = df[df['Field Name'].isin(cols)]
match = match.dropna()
pd.set_option('display.max_colwidth', -1)
print(match[['Field Name', 'Comments']], flush=True)