#'education is something you don't want to finish'
# crushlabs@protonmail.com 
# feedback is appreciated

import pandas as pd # standard pandas import
import plotly # we will use this as our plotting library
import plotly.graph_objects as go # we will use this for plots in webbrowser
from plotly.subplots import make_subplots # this will allow for multiple plots
import world_bank_data as wb # for python3, open terminal -> pip3 install world_bank_data --upgrade

# pd.set_option('display.max_colwidth', -1) # set this if you want to print entire column value, i.e. to read a description

countries = wb.get_countries() # get countries
# print(countries) # uncomment if you want to check the values
indicators = wb.get_indicators() # get indicators
# print(indicators) # uncomment if you want to check the values
topics = wb.get_topics().reset_index() # get topics
# print(topics) # uncomment if you want to check the values

topicSearch1 = 'Climate' # enter a keyword or keywords to search topics i.e. current search is for -> Climate; capital 'C'
topicSearch2 = 'Environment' # enter a keyword or keywords to search topics
filteredTopics1 = topics[topics['value'].str.contains(topicSearch1, na=False)] # filtering topics by your search
filteredTopics2 = topics[topics['value'].str.contains(topicSearch2, na=False)] # filtering topics by your search
filteredTopics1 # check if something is returned
filteredTopics2 # check if something is returned
filteredTopicsId1 = filteredTopics1['id'].iloc[0] # get the topic ID, which you will input into indicator search
filteredTopicsId2 = filteredTopics2['id'].iloc[0] # get the topic ID, which you will input into indicator search
print(f'This value serves as input to indicator search:', filteredTopicsId1) # run this to see topic ID
print(f'This value serves as input to indicator search:', filteredTopicsId2) # run this to see topic ID

#sources = wb.get_sources().reset_index()
# print(sources) # uncomment if you want to check the values
#sourceSearch1 = 'Environment'
#sourceSearch2 = 'Education Statistics'
#filteredSources1 = sources[sources['name'].str.contains(sourceSearch1, na=False)]
#filteredSources2 = sources[sources['name'].str.contains(sourceSearch2, na=False)]
#filteredSources1 # check if something is returned
#filteredSources2 # check if something is returned
#filteredSourcesId1 = filteredSources1['id'].iloc[0] # get the source ID, which you will input into indicator search
#filteredSourcesId2 = filteredSources2['id'].iloc[0] # get the source ID, which you will input into indicator search
#print(f'This value serves as input to indicator search:', filteredSourcesId1) # run this to see topic ID
#print(f'This value serves as input to indicator search:', filteredSourcesId2) # run this to see topic ID

getIndicators1 = wb.get_indicators(topic = filteredTopicsId1) # plugging topicID and sourceID here
getIndicators1 # see what is returned
getIndicators1.name.unique()
strSearch1 = 'CO2 emissions' # let's search for CO2 emissions -> input your own value of interest
strSearch2 = 'Population growth' # let's search for Population growth -> input your own value of interest
strSearch3 = 'Renewable energy consumption' # let's search for Renewable energy
strSearch4 = 'Foreign direct investment' # let's search for Foreign direct investment

CO2_emissions = getIndicators1[getIndicators1['name'].str.contains(strSearch1, na=False)].reset_index() # locate the indicators with CO2
Population_growth = getIndicators1[getIndicators1['name'].str.contains(strSearch2, na=False)].reset_index() # locate the indicators with Population growth
Renewable_energy = getIndicators1[getIndicators1['name'].str.contains(strSearch3, na=False)].reset_index() # locate the indicators with Renewable energy
Foreign_Investment = getIndicators1[getIndicators1['name'].str.contains(strSearch4, na=False)].reset_index() # locate the indicators with Foreign Investment
CO2Id = str(CO2_emissions['id'].iloc[6]) # extract the id as string to input into series object
popGrowthId = str(Population_growth['id'].iloc[0]) # extract the id as string to input into series object
renewEnergyId = str(Renewable_energy['id'].iloc[0]) # extract the id as string to input into series object
foreignInvestId = str(Foreign_Investment['id'].iloc[0]) # extract the id as string to input into series object

print(f'The following value is inputed to series:', CO2Id) # run this to see input to series
print(f'The following value is inputed to series:', popGrowthId) # run this to see input to series
print(f'The following value is inputed to series:', renewEnergyId) # run this to see input to series
print(f'The following value is inputed to series:', foreignInvestId) # run this to see input to series

series1 = pd.DataFrame(wb.get_series(CO2Id)).reset_index() # get the data for searched indicator by country and year
series2 = pd.DataFrame(wb.get_series(popGrowthId)).reset_index() # get the data for searched indicator by country and year
series3 = pd.DataFrame(wb.get_series(renewEnergyId)).reset_index() # get the data for searched indicator by country and year
series4 = pd.DataFrame(wb.get_series(foreignInvestId)).reset_index() # get the data for searched indicator by country and year
countryList1 = ['Denmark', 'Sweden', 'Norway'] # define the number of countries and which you'd like to explore
countryList2 = ['Denmark',' Sweden', 'Norway'] # define the number of countries and which you'd like to explore
countryList3 = ['Denmark', 'Sweden', 'Norway'] # define the number of countries and which you'd like to explore
countryList4 = ['Denmark', 'Sweden', 'Norway'] # define the number of countries and which you'd like to explore

seriesDf1 = series1[series1['Country'].isin(countryList1)] # filter the dataframe for wanted countries
seriesDf2 = series2[series2['Country'].isin(countryList2)] # filter the dataframe for wanted countries
seriesDf3 = series3[series3['Country'].isin(countryList3)] # filter the dataframe for wanted countries
seriesDf4 = series4[series4['Country'].isin(countryList4)] # filter the dataframe for wanted countries

seriesDf1 = seriesDf1[seriesDf1['Year']>='1990-01-01']
seriesDf2 = seriesDf2[seriesDf2['Year']>='1990-01-01']
seriesDf3 = seriesDf3[seriesDf3['Year']>='1990-01-01']
seriesDf4 = seriesDf4[seriesDf4['Year']>='1990-01-01']

seriesDf1.head(3) # inspect the data head
seriesDf1.tail(3) # inspect the data tail
seriesDf2.head(3) # inspect the data head
seriesDf2.tail(3) # inspect the data tail
seriesDf3.head(3) # inspect the data head
seriesDf3.tail(3) # inspect the data tail
seriesDf4.head(3) # inspect the data head
seriesDf4.tail(3) # inspect the data tail


title1 = seriesDf1['Series'].iloc[0]
title2 = seriesDf2['Series'].iloc[0]
title3 = seriesDf3['Series'].iloc[0]
title4 = seriesDf4['Series'].iloc[0]

DK = seriesDf1[seriesDf1['Country']=='Denmark']
SE = seriesDf1[seriesDf1['Country']=='Sweden']
NO = seriesDf1[seriesDf1['Country']=='Norway']

DK1 = seriesDf2[seriesDf2['Country']=='Denmark']
SE1 = seriesDf2[seriesDf2['Country']=='Sweden']
NO1 = seriesDf2[seriesDf2['Country']=='Norway']

DK2 = seriesDf3[seriesDf3['Country']=='Denmark']
SE2 = seriesDf3[seriesDf3['Country']=='Sweden']
NO2 = seriesDf3[seriesDf3['Country']=='Norway']

DK3 = seriesDf4[seriesDf4['Country']=='Denmark']
SE3 = seriesDf4[seriesDf4['Country']=='Sweden']
NO3 = seriesDf4[seriesDf4['Country']=='Norway']

fig = make_subplots(rows=2, cols=2, subplot_titles=(title1, title2, title3, title4))
fig.append_trace(go.Scatter(x=DK['Year'],y=DK['EN.ATM.CO2E.PC'], name = 'Denmark', marker = dict(color='LightSkyBlue'), legendgroup='group'), row=1, col=1)
fig.append_trace(go.Scatter(x=SE['Year'],y=SE['EN.ATM.CO2E.PC'], name = 'Sweden', marker = dict(color='MediumPurple'), legendgroup='group'), row=1, col=1)
fig.append_trace(go.Scatter(x=NO['Year'],y=NO['EN.ATM.CO2E.PC'], name = 'Norway', marker = dict(color='Green'), legendgroup='group'), row=1, col=1)

fig.append_trace(go.Bar(x=DK1['Year'],y=DK1['SP.POP.GROW'], name = 'Denmark', marker = dict(color='LightSkyBlue'), legendgroup='group2'), row=1, col=2)
fig.append_trace(go.Bar(x=SE1['Year'],y=SE1['SP.POP.GROW'], name = 'Sweden', marker = dict(color='MediumPurple'), legendgroup='group2'), row=1, col=2)
fig.append_trace(go.Bar(x=NO1['Year'],y=NO1['SP.POP.GROW'], name = 'Norway', marker = dict(color='Green'), legendgroup='group2'), row=1, col=2)

fig.append_trace(go.Scatter(x=DK2['Year'],y=DK2['EG.FEC.RNEW.ZS'], name = 'Denmark', marker = dict(color='LightSkyBlue'), showlegend = False), row=2, col=1)
fig.append_trace(go.Scatter(x=SE2['Year'],y=SE2['EG.FEC.RNEW.ZS'], name = 'Sweden', marker = dict(color='MediumPurple'), showlegend = False), row=2, col=1)
fig.append_trace(go.Scatter(x=NO2['Year'],y=NO2['EG.FEC.RNEW.ZS'], name = 'Norway', marker = dict(color='Green'), showlegend = False), row=2, col=1)

fig.append_trace(go.Bar(x=DK3['Year'],y=DK3['BX.KLT.DINV.WD.GD.ZS'], name = 'Denmark', marker = dict(color='LightSkyBlue'),showlegend = False), row=2, col=2)
fig.append_trace(go.Bar(x=SE3['Year'],y=SE3['BX.KLT.DINV.WD.GD.ZS'], name = 'Sweden', marker = dict(color='MediumPurple'), showlegend = False), row=2, col=2)
fig.append_trace(go.Bar(x=NO3['Year'],y=NO3['BX.KLT.DINV.WD.GD.ZS'], name = 'Norway', marker = dict(color='Green'), showlegend = False), row=2, col=2)

fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title = 'Denmark, Sweden, Norway', showlegend=True, title_x=0.5)
fig.write_html('worldbank.html', auto_open=True)
