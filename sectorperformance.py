### 'education is something you don't want to finish'
# crushlabs@protonmail.com
# feedback appreciated
# exploring AlphaVantage sector performance

# perform usual imports
import pandas as pd 
import numpy as np 
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.sectorperformance import SectorPerformances
apikey = '' # input your alpha vantage api key

sp = SectorPerformances(key = apikey) # get sector performance
data = sp.get_sector() # this is a tuple
l = list(data) # let's convert it to list
df = pd.DataFrame.from_dict(l[0]).reset_index() # now convert it to DF
dfTr = df.transpose().reset_index() # transpose for our use case

dfTr.columns = dfTr.iloc[0] # update column values
dfTr = dfTr.iloc[1:] # drop unnecessary row
dfTr.head(3) # inspect data
dfTr.tail(3) # keep inspecting

ytd = dfTr[dfTr['index']=='Rank F: Year-to-Date (YTD) Performance'] # year to date performance of sectors
ytd = ytd.drop('Real Estate', axis = 1) # Real estate in 5 year period has a NaN value - let's remove the sector for coherence

monthly = dfTr[dfTr['index']=='Rank D: 1 Month Performance'] # monthly sector performance
monthly = monthly.drop('Real Estate', axis = 1) # no Real estate

yearly = dfTr[dfTr['index']=='Rank G: 1 Year Performance'] # yearly sector performance 
yearly = yearly.drop('Real Estate', axis = 1) # no Real estate

yearfive = dfTr[dfTr['index']=='Rank I: 5 Year Performance'] # five year sector performance
yearfive = yearfive.drop('Real Estate', axis = 1) # no real estate

title1 = str(monthly['index'].iloc[0]).replace('Rank D:', '') # get titles for plots
title2 = str(ytd['index'].iloc[0]).replace('Rank F:', '') # get titles for plots
title3 = str(yearly['index'].iloc[0]).replace('Rank G:', '') # get titles for plots
title4 = str(yearfive['index'].iloc[0]).replace('Rank I:', '') # get titles for plots

# this sets bar colors to red if values are negative
def SetColor(b):
    if(b==0):
        return 'rgb(51, 51, 77)'
    elif(b<0):
        return "red"
    elif(b>0):
        return 'rgb(51, 51, 77)'



fig = make_subplots(rows=2, cols=2, subplot_titles = (title1, title2, title3, title4)) # make subplots

# you can remove this step, it's for subplot title annotations, setting font size to 12
for i in fig['layout']['annotations']:
    i['font'] = dict(size=12,color='rgb(51, 51, 77)')

# usuall ploty stuff bellow
fig.append_trace(go.Bar(x=monthly.columns[1:],y=monthly.iloc[0][1:], marker = dict(color=list(map(SetColor,monthly.iloc[0][1:])))), row=1, col=1)
fig.append_trace(go.Bar(x=ytd.columns[1:],y=ytd.iloc[0][1:], marker = dict(color=list(map(SetColor,ytd.iloc[0][1:])))), row=1, col=2)
fig.append_trace(go.Bar(x=yearly.columns[1:],y=yearly.iloc[0][1:], marker = dict(color=list(map(SetColor,yearly.iloc[0][1:])))), row=2, col=1)
fig.append_trace(go.Bar(x=yearfive.columns[1:],y=yearfive.iloc[0][1:], marker = dict(color=list(map(SetColor,yearfive.iloc[0][1:])))), row=2, col=2)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    title = 'Sector Performance %',
                    title_x = 0.5,
                    showlegend = False,
                    font=dict(color='rgb(51, 51, 77)'))                
fig.write_html('SectorPerformances.html', auto_open=True)

# end