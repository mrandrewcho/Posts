#%%
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from datetime import datetime

#Kendall Jenner, Blake Griffin; August 2017 - February 2018; 
#Tristan Thompson, Khloe Kardashian; July 2016 - February 19, 2019
#Ben Simmons, Kendall Jenner; June 12, 2018 - May 22, 2019
#Lamar Odom, Khloe Kardashian; August 2009 - December 13, 2013
#Kris Humphries; November 2010 - November 2011
#Game Score, PER


#%%
player_keys = ['griffbl01', 'thomptr01', 'simmobe01', 'odomla01', 'humphkr01']

#pull headers
url = 'https://www.basketball-reference.com/players/g/griffbl01/gamelog/2017'
#HTML from given URL
html = urlopen(url)
soup = BeautifulSoup(html)
#extract text into list
headers = [th.getText() for th in soup.findAll('thead')[0].findAll('tr')[0].findAll('th')]
headers = headers[1:]

#pull individual seasons for player
def pull_gamelogs(player_key):
    year = 1999 #first year of Lamar Odom's career (oldest player)
    complete_stats = pd.DataFrame()
    while (year <= 2019):
        #URL to scrape
        url = 'https://www.basketball-reference.com/players/g/{}/gamelog/{}'.format(player_key, year)
        try:
            #HTML from given URL
            html = urlopen(url)
            soup = BeautifulSoup(html)
            rows = soup.findAll('tbody')[0].findAll('tr')
            player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]
            stats = pd.DataFrame(player_stats, columns = headers)
            stats = stats[stats['G'].notnull()]
            stats = stats.reset_index(drop=True)
            complete_stats = complete_stats.append(stats)
        except:
            pass
        year+=1
    return complete_stats

#%%
bg_stats = pull_gamelogs(player_keys[0])
bg_stats['Player'] = 'Blake Griffin'
tt_stats = pull_gamelogs(player_keys[1])
tt_stats['Player'] = 'Tristan Thompson'
bs_stats = pull_gamelogs(player_keys[2])
bs_stats['Player'] = 'Ben Simmons'
lo_stats = pull_gamelogs(player_keys[3])
lo_stats['Player'] = 'Lamar Odom'
kh_stats = pull_gamelogs(player_keys[4])
kh_stats['Player'] = 'Kris Humphries'

#%%
bg_stats['Date'] = pd.to_datetime(bg_stats['Date'])
tt_stats['Date'] = pd.to_datetime(tt_stats['Date'])
bs_stats['Date'] = pd.to_datetime(bs_stats['Date'])
lo_stats['Date'] = pd.to_datetime(lo_stats['Date'])
kh_stats['Date'] = pd.to_datetime(kh_stats['Date'])

#%%
bg_stats.index = bg_stats['Date']
del bg_stats['Date']
tt_stats.index = tt_stats['Date']
del tt_stats['Date']
bs_stats.index = bs_stats['Date']
del bs_stats['Date']
lo_stats.index = lo_stats['Date']
del lo_stats['Date']
kh_stats.index = kh_stats['Date']
del kh_stats['Date']

#%%
bg_stats['GmSc'] = bg_stats['GmSc'].astype('float64')
tt_stats['GmSc'] = tt_stats['GmSc'].astype('float64')
bs_stats['GmSc'] = bs_stats['GmSc'].astype('float64')
lo_stats['GmSc'] = lo_stats['GmSc'].astype('float64')
kh_stats['GmSc'] = kh_stats['GmSc'].astype('float64')


#%%
bg_stats_weekly = bg_stats.resample('W').mean()
bg_stats_weekly['rolling_GmSc'] = bg_stats_weekly['GmSc'].rolling( window=2).mean()
tt_stats_weekly = tt_stats.resample('W').mean()
tt_stats_weekly['rolling_GmSc'] = tt_stats_weekly['GmSc'].rolling( window=2).mean()
bs_stats_weekly = bs_stats.resample('W').mean()
bs_stats_weekly['rolling_GmSc'] = bs_stats_weekly['GmSc'].rolling( window=2).mean()
lo_stats_weekly = lo_stats.resample('W').mean()
lo_stats_weekly['rolling_GmSc'] = lo_stats_weekly['GmSc'].rolling( window=2).mean()
kh_stats_weekly = kh_stats.resample('W').mean()
kh_stats_weekly['rolling_GmSc'] = kh_stats_weekly['GmSc'].rolling( window=2).mean()

#%%
trace1 = go.Scatter(
    x = bg_stats_weekly.index,
    y = bg_stats_weekly['rolling_GmSc'],
    name='Blake Griffin'
)

layout = go.Layout(
    title="Blake Griffin 2 Week Roling Game Scores", 
    xaxis={'title':'Date'}, 
    yaxis={'title':'Weekly Mean Game Score'},
    shapes=[
        # Kendall
        {
            'type': 'line',
            'x0': datetime.strptime('2017-08-01', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2017-08-02', '%Y-%m-%d'),
            'y1': 30,
            'line': {
                'color': 'red',
                'width': 3,
                'dash': 'dashdot'
            },
            'layer': 'below'
        },
        {
            'type': 'line',
            'x0': datetime.strptime('2018-02-01', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2018-02-02', '%Y-%m-%d'),
            'y1': 30,
            'line': {
                'color': 'red',
                'width': 3,
                'dash': 'dashdot'
            },
            'layer': 'below'
        }
    ],
    annotations=[
        dict(
            x=datetime.strptime('2017-11-01', '%Y-%m-%d'),
            y=32,
            xref='x',
            yref='y',
            text='Kendall Jenner',
            showarrow=False,
            arrowhead=7,
            ax=0,
            ay=-40
        )
    ],
    autosize=False,
    width=600,
    height=400,
    margin=go.layout.Margin(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    )
)
fig = go.Figure(data=[trace1], layout=layout)
iplot(fig, filename='time-series-simple')

#%%
