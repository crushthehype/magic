### 'education is something you don't want to finish' ###
# crushlabs@protonmail.com
# learn, have fun, give feedback
# it was challenging to plot circle size by nKilled and color by AttackType with go.Figure properties
# data is filtered from 1997 onwards
# na's filled with 0 for representation of total number attacks

import kaggle # pip3 install kaggle
import pandas as pd 
import numpy as np 
import plotly.graph_objects as go

mapboxtoken ='' # you will need your MapBox token here

kaggle.api.authenticate()
datasets = kaggle.api.datasets_list()
kaggle.api.dataset_download_files('START-UMD/gtd', path='/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages', unzip=True) # change location of your downloaded file

res = pd.read_csv('globalterrorismdb_0718dist.csv', encoding='ISO-8859-1') # read csv with encoding 
res.head()
res.tail()
list(res.columns)
data = res

data.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed','nwound':'Wounded','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True) # rename columns of interest
data=data[['Year','Country','Region','city','latitude','longitude','AttackType','Killed','Wounded','Target','Group','Target_type','Weapon_type','Motive',]] # get data in the frame

data.head(3)
data.tail(3)

data1997 = data[data['Year']>=1997] # filter for > 1997 or selected year
data1997.isnull().sum() # check for null's
data1997.info()
data1997.head(3)
data1997.tail(3)
data1997 = data1997.fillna(0) # fill na's for representativeness, otherwise you'll end-up removing big subsets of data


fig= go.Figure(go.Scattermapbox(lat= data1997['latitude'],
    lon=data1997['longitude'],
    mode='markers', 
    marker = go.scattermapbox.Marker(size=data1997['Killed']*0.1,color=data1997['Killed'], colorscale='deep', opacity=0.7), # wanted to color by size and color as attacktype, but was lazy to encode data into categories
    text = data1997[['Killed', 'AttackType', 'city', 'Year']],
    hoverinfo='text'))

fig.update_layout(hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapboxtoken,
        bearing=0,
        center=go.layout.mapbox.Center(lat=0,lon=0),
        pitch=0,
        zoom=1.5),
        showlegend = False,
        mapbox_style='dark',
        title = 'Terrorist attacks 1997-2017;number of people killed, attack type, year',
        font=dict(color='rgb(255,255,255)'),
        width = 1500,
        height = 850,
        title_x = 0.5,
        paper_bgcolor='rgb(25,26,26)')
fig.write_html('terrorism.html', auto_open=True)

# end