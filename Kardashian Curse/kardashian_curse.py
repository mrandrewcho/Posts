#%%
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from datetime import datetime
from scipy import stats

#Kendall Jenner, Blake Griffin; August 2017 - February 2018; 
#Tristan Thompson, Khloe Kardashian; July 2016 - February 19, 2019
#Ben Simmons, Kendall Jenner; June 12, 2018 - May 22, 2019
#Lamar Odom, Khloe Kardashian; August 2009 - December 13, 2013
#Kris Humphries, Kim Kardashian; November 2010 - November 2011
#Game Score, PER

#%%
#functions

#function to pull individual seasons for player
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
player_keys = ['griffbl01', 'thomptr01', 'simmobe01', 'odomla01', 'humphkr01']

#pull headers
url = 'https://www.basketball-reference.com/players/g/griffbl01/gamelog/2017'
#HTML from given URL
html = urlopen(url)
soup = BeautifulSoup(html)
#extract text into list
headers = [th.getText() for th in soup.findAll('thead')[0].findAll('tr')[0].findAll('th')]
headers = headers[1:]

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
#Blake Griffin Graph
trace1 = go.Scatter(
    x = bg_stats_weekly.index,
    y = bg_stats_weekly['rolling_GmSc'],
    name='Blake Griffin',
    line= {
        "color": "rgb(245, 16, 0)",
        "width": 2
    },
)

layout = go.Layout(
    font= {
      "size": 12,
      "color": "#444",
      "family": "Muli, sans-serif"
    },
    title="<b>Blake Griffin</b><br>Mean Game Scores (Rolling 2 Week)", 
    xaxis={'title':'Date'}, 
    yaxis={'title':'Mean Game Score'},
    shapes=[
        # Kendall
        {
            'type': 'line',
            'x0': datetime.strptime('2017-08-01', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2017-08-02', '%Y-%m-%d'),
            'y1': 30,
            'line': {
                'color': 'rgb(123, 123, 245)',
                'width': 2,
                'dash': 'dot'
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
                'color': 'rgb(123, 123, 245)',
                'width': 2,
                'dash': 'dot'
            },
            'layer': 'below'
        }
    ],
    annotations=[
        dict(
            x=datetime.strptime('2017-11-01', '%Y-%m-%d'),
            y=31,
            xref='x',
            yref='y',
            text='Kendall Jenner',
            showarrow=False,
            arrowhead=7,
            ax=0,
            ay=-40,
            font= {
                "size": 14,
                "color": 'rgb(123, 123, 245)',
            },
        )
    ],
    autosize=False,
    height=575,
    bargap=0.2,
    boxgap=0.3,
    margin=go.layout.Margin(
        l=80,
        r=80,
        b=80,
        t=100,
        pad=0,
        autoexpand=True
    ),
    bargroupgap= 0,
    boxgroupgap= 0.3,
    hidesources= True,
    plot_bgcolor= "rgb(240, 240, 240)",
    paper_bgcolor= "rgb(240, 240, 240)"
)
fig = go.Figure(data=[trace1], layout=layout)
iplot(fig, filename='time-series-simple')

#%%
#mean game score during dating and outside of dating
bg_stats_no_curse = bg_stats[(bg_stats.index > '2018-02-01') | (bg_stats.index < '2017-08-01')]
bg_stats_curse = bg_stats[(bg_stats.index >= '2017-08-01') & (bg_stats.index <= '2018-02-01')]
print('No Curse', bg_stats_no_curse.describe())
print('Curse', bg_stats_curse.describe())

#%%
#t-test
bg_stats_no_curse_no_null = bg_stats_no_curse[bg_stats_no_curse.GmSc.notnull()]
bg_stats_curse_no_null = bg_stats_curse[bg_stats_curse.GmSc.notnull()]
stats.ttest_ind(bg_stats_no_curse_no_null.GmSc, bg_stats_curse_no_null.GmSc)

#%%
#Tristan Thompson Graph
trace1 = go.Scatter(
    x = tt_stats_weekly.index,
    y = tt_stats_weekly['rolling_GmSc'],
    name='Tristan Thompson',
    line= {
        "color": "rgb(245, 16, 0)",
        "width": 2
    },
)

layout = go.Layout(
    font= {
      "size": 12,
      "color": "#444",
      "family": "Muli, sans-serif"
    },
    title="<b>Tristan Thompson</b><br>Mean Game Scores (Rolling 2 Week)", 
    xaxis={'title':'Date'}, 
    yaxis={'title':'Mean Game Score'},
    shapes=[
        # Khloe
        {
            'type': 'line',
            'x0': datetime.strptime('2016-07-01', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2016-07-02', '%Y-%m-%d'),
            'y1': 20,
            'line': {
                'color': 'rgb(100, 220, 220)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        },
        {
            'type': 'line',
            'x0': datetime.strptime('2019-02-19', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2019-02-20', '%Y-%m-%d'),
            'y1': 20,
            'line': {
                'color': 'rgb(100, 220, 220)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        }
    ],
    annotations=[
        dict(
            x=datetime.strptime('2017-11-01', '%Y-%m-%d'),
            y=21,
            xref='x',
            yref='y',
            text='Khloe Kardashian',
            showarrow=False,
            arrowhead=7,
            ax=0,
            ay=-40,
            font= {
                "size": 14,
                "color": 'rgb(100, 220, 220)',
            },
        )
    ],
    autosize=False,
    height=575,
    bargap=0.2,
    boxgap=0.3,
    margin=go.layout.Margin(
        l=80,
        r=80,
        b=80,
        t=100,
        pad=0,
        autoexpand=True
    ),
    bargroupgap= 0,
    boxgroupgap= 0.3,
    hidesources= True,
    plot_bgcolor= "rgb(240, 240, 240)",
    paper_bgcolor= "rgb(240, 240, 240)"
)
fig = go.Figure(data=[trace1], layout=layout)
iplot(fig, filename='time-series-simple')

#%%
#mean game score during dating and outside of dating
tt_stats_no_curse = tt_stats[(tt_stats.index > '2019-02-19') | (tt_stats.index < '2016-07-01')]
tt_stats_curse = tt_stats[(tt_stats.index >= '2017-07-01') & (tt_stats.index <= '2019-02-19')]
print('No Curse', tt_stats_no_curse.describe())
print('Curse', tt_stats_curse.describe())

#%%
#t-test
tt_stats_no_curse_no_null = tt_stats_no_curse[tt_stats_no_curse.GmSc.notnull()]
tt_stats_curse_no_null = tt_stats_curse[tt_stats_curse.GmSc.notnull()]
stats.ttest_ind(tt_stats_no_curse_no_null.GmSc, tt_stats_curse_no_null.GmSc)

#%%
#Ben Simmons Graph
trace1 = go.Scatter(
    x = bs_stats_weekly.index,
    y = bs_stats_weekly['rolling_GmSc'],
    name='Ben Simmons',
    line= {
        "color": "rgb(245, 16, 0)",
        "width": 2
    },
)

layout = go.Layout(
    font= {
      "size": 12,
      "color": "#444",
      "family": "Muli, sans-serif"
    },
    title="<b>Ben Simmons</b><br>Mean Game Scores (Rolling 2 Week)", 
    xaxis={'title':'Date'}, 
    yaxis={'title':'Mean Game Score'},
    shapes=[
        # Kendall
        {
            'type': 'line',
            'x0': datetime.strptime('2018-06-12', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2018-06-13', '%Y-%m-%d'),
            'y1': 20,
            'line': {
                'color': 'rgb(123, 123, 245)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        },
        {
            'type': 'line',
            'x0': datetime.strptime('2019-05-22', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2019-05-23', '%Y-%m-%d'),
            'y1': 20,
            'line': {
                'color': 'rgb(123, 123, 245)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        }
    ],
    annotations=[
        dict(
            x=datetime.strptime('2018-12-01', '%Y-%m-%d'),
            y=22,
            xref='x',
            yref='y',
            text='Kendall Jenner',
            showarrow=False,
            arrowhead=7,
            ax=0,
            ay=-40,
            font= {
                "size": 14,
                "color": 'rgb(123, 123, 245)',
            },
        )
    ],
    autosize=False,
    height=575,
    bargap=0.2,
    boxgap=0.3,
    margin=go.layout.Margin(
        l=80,
        r=80,
        b=80,
        t=100,
        pad=0,
        autoexpand=True
    ),
    bargroupgap= 0,
    boxgroupgap= 0.3,
    hidesources= True,
    plot_bgcolor= "rgb(240, 240, 240)",
    paper_bgcolor= "rgb(240, 240, 240)"
)
fig = go.Figure(data=[trace1], layout=layout)
iplot(fig, filename='time-series-simple')

#%%
#mean game score during dating and outside of dating
bs_stats_no_curse = bs_stats[(bs_stats.index > '2019-05-22') | (bs_stats.index < '2018-06-12')]
bs_stats_curse = bs_stats[(bs_stats.index >= '2018-06-12') & (bs_stats.index <= '2019-05-22')]
print('No Curse', bs_stats_no_curse.describe())
print('Curse', bs_stats_curse.describe())

#%%
#t-test
bs_stats_no_curse_no_null = bs_stats_no_curse[bs_stats_no_curse.GmSc.notnull()]
bs_stats_curse_no_null = bs_stats_curse[bs_stats_curse.GmSc.notnull()]
stats.ttest_ind(bs_stats_no_curse_no_null.GmSc, bs_stats_curse_no_null.GmSc)

#%%
#Lamar Odom Graph
trace1 = go.Scatter(
    x = lo_stats_weekly.index,
    y = lo_stats_weekly['rolling_GmSc'],
    name='Lamar Odom',
    line= {
        "color": "rgb(245, 16, 0)",
        "width": 2
    },
)

layout = go.Layout(
    font= {
      "size": 12,
      "color": "#444",
      "family": "Muli, sans-serif"
    },
    title="<b>Lamar Odom</b><br>Mean Game Scores (Rolling 2 Week)", 
    xaxis={'title':'Date'}, 
    yaxis={'title':'Mean Game Score'},
    shapes=[
        # Khloe
        {
            'type': 'line',
            'x0': datetime.strptime('2009-08-01', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2009-08-02', '%Y-%m-%d'),
            'y1': 20,
            'line': {
                'color': 'rgb(100, 220, 220)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        },
        {
            'type': 'line',
            'x0': datetime.strptime('2013-12-13', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2013-12-14', '%Y-%m-%d'),
            'y1': 20,
            'line': {
                'color': 'rgb(100, 220, 220)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        }
    ],
    annotations=[
        dict(
            x=datetime.strptime('2011-11-01', '%Y-%m-%d'),
            y=21,
            xref='x',
            yref='y',
            text='Khloe Kardashian',
            showarrow=False,
            arrowhead=7,
            ax=0,
            ay=-40,
            font= {
                "size": 14,
                "color": 'rgb(100, 220, 220)',
            },
        )
    ],
    autosize=False,
    height=575,
    bargap=0.2,
    boxgap=0.3,
    margin=go.layout.Margin(
        l=80,
        r=80,
        b=80,
        t=100,
        pad=0,
        autoexpand=True
    ),
    bargroupgap= 0,
    boxgroupgap= 0.3,
    hidesources= True,
    plot_bgcolor= "rgb(240, 240, 240)",
    paper_bgcolor= "rgb(240, 240, 240)"
)
fig = go.Figure(data=[trace1], layout=layout)
iplot(fig, filename='time-series-simple')

#%%
#mean game score during dating and outside of dating
lo_stats_no_curse = lo_stats[(lo_stats.index > '2013-12-13') | (lo_stats.index < '2009-08-01')]
lo_stats_curse = lo_stats[(lo_stats.index >= '2009-08-01') & (lo_stats.index <= '2013-12-13')]
print('No Curse', lo_stats_no_curse.describe())
print('Curse', lo_stats_curse.describe())

#%%
#t-test
lo_stats_no_curse_no_null = lo_stats_no_curse[lo_stats_no_curse.GmSc.notnull()]
lo_stats_curse_no_null = lo_stats_curse[lo_stats_curse.GmSc.notnull()]
stats.ttest_ind(lo_stats_no_curse_no_null.GmSc, lo_stats_curse_no_null.GmSc)


#%%
#Kris Humphries; November 2010 - November 2011
#Kris Humphries Graph
trace1 = go.Scatter(
    x = kh_stats_weekly.index,
    y = kh_stats_weekly['rolling_GmSc'],
    name='Kris Humphries',
    line= {
        "color": "rgb(245, 16, 0)",
        "width": 2
    },
)

layout = go.Layout(
    font= {
      "size": 12,
      "color": "#444",
      "family": "Muli, sans-serif"
    },
    title="<b>Kris Humphries</b><br>Mean Game Scores (Rolling 2 Week)", 
    xaxis={'title':'Date'}, 
    yaxis={'title':'Mean Game Score'},
    shapes=[
        # Kim
        {
            'type': 'line',
            'x0': datetime.strptime('2010-11-01', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2010-11-02', '%Y-%m-%d'),
            'y1': 16,
            'line': {
                'color': 'rgb(255, 148, 220)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        },
        {
            'type': 'line',
            'x0': datetime.strptime('2011-11-01', '%Y-%m-%d'),
            'y0': 0,
            'x1': datetime.strptime('2011-11-02', '%Y-%m-%d'),
            'y1': 16,
            'line': {
                'color': 'rgb(255, 148, 220)',
                'width': 3,
                'dash': 'dot'
            },
            'layer': 'below'
        }
    ],
    annotations=[
        dict(
            x=datetime.strptime('2011-05-01', '%Y-%m-%d'),
            y=17,
            xref='x',
            yref='y',
            text='Kim Kardashian',
            showarrow=False,
            arrowhead=7,
            ax=0,
            ay=-40,
            font= {
                "size": 14,
                "color": 'rgb(255, 148, 220)',
            },
        )
    ],
    autosize=False,
    height=575,
    bargap=0.2,
    boxgap=0.3,
    margin=go.layout.Margin(
        l=80,
        r=80,
        b=80,
        t=100,
        pad=0,
        autoexpand=True
    ),
    bargroupgap= 0,
    boxgroupgap= 0.3,
    hidesources= True,
    plot_bgcolor= "rgb(240, 240, 240)",
    paper_bgcolor= "rgb(240, 240, 240)"
)
fig = go.Figure(data=[trace1], layout=layout)
iplot(fig, filename='time-series-simple')

#%%
#mean game score during dating and outside of dating
kh_stats_no_curse = kh_stats[(kh_stats.index > '2011-11-01') | (kh_stats.index < '2010-11-01')]
kh_stats_curse = kh_stats[(kh_stats.index >= '2010-11-01') & (kh_stats.index <= '2011-11-01')]
print('No Curse', kh_stats_no_curse.describe())
print('Curse', kh_stats_curse.describe())

#%%
#t-test
kh_stats_no_curse_no_null = kh_stats_no_curse[kh_stats_no_curse.GmSc.notnull()]
kh_stats_curse_no_null = kh_stats_curse[kh_stats_curse.GmSc.notnull()]
stats.ttest_ind(kh_stats_no_curse_no_null.GmSc, kh_stats_curse_no_null.GmSc)

#%%


#%%
