#%%
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import plotly.graph_objs as go
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#%%
#####
#functions
#####

#visualize all the dataframe columns as line plots
def plotly_df(df, title=''):
    common_kw = dict(x=df.index, mode='lines')
    data = [go.Scatter(y=df['y'], name=title, **common_kw, line= {"color": "rgb(245, 16, 0)", "width": 2})]
    layout = go.Layout(
        font= {
            'size': 12,
            'color': '#444',
            'family': 'Muli, sans-serif'
        },
        title='<b>%s</b><br>Wikipedia Page Views' % title, 
        xaxis={'title':'Date'}, 
        yaxis={'title':'Daily Page Views'},
        autosize=False,
        height=500,
        margin=go.layout.Margin(
            l=80,
            r=80,
            b=80,
            t=100,
            pad=0,
            autoexpand=True
        ),
        plot_bgcolor= "rgb(240, 240, 240)",
        paper_bgcolor= "rgb(240, 240, 240)"
    )
    fig = dict(data=data, layout=layout)
    iplot(fig, show_link=False)

#join historical df to forecast df
def make_comparison_dataframe(historical, forecast):
    return forecast.set_index('ds')[['yhat', 'yhat_lower', 'yhat_upper']].join(historical.set_index('ds'))

#calculate MAPES & MAES
def calculate_forecast_errors(df, prediction_size):  
    '''  
       Args:
           df: joined dataset with 'y' and 'yhat' columns.
           prediction_size: number of days at the end to predict.
    '''
    # Make a copy
    df = df.copy()
    
    # Calculate the values of e_i and p_i, with unlogged values
    df['e'] = np.exp(df['y']) - np.exp(df['yhat'])
    df['p'] = 100 * df['e'] / np.exp(df['y'])
    
    # Recall that we held out the values of the last `prediction_size` days
    # in order to predict them and measure the quality of the model. 
    
    # Now cut out the part of the data which we made our prediction for.
    predicted_part = df[-prediction_size:]
    
    # Define the function that averages absolute error values over the predicted part.
    error_mean = lambda error_name: np.mean(np.abs(predicted_part[error_name]))
    
    # Now we can calculate MAPE and MAE and return the resulting dictionary of errors.
    return {'MAPE': error_mean('p'), 'MAE': error_mean('e')}

#visualize forecast
def show_forecast(cmp_df, num_predictions, num_values, title):    
    def create_go(name, column, num, **kwargs):
        points = cmp_df.tail(num)
        args = dict(name=name, x=points.index, y=points[column], mode='lines')
        args.update(kwargs)
        return go.Scatter(**args)
    
    lower_bound = create_go('Lower Bound', 'yhat_lower', num_predictions,
                            line=dict(width=0),
                            marker=dict(color="#444"))
    upper_bound = create_go('Upper Bound', 'yhat_upper', num_predictions,
                            line=dict(width=0),
                            marker=dict(color="#444"),
                            fillcolor='rgba(68, 68, 68, 0.3)', 
                            fill='tonexty')
    forecast = create_go('Forecast', 'yhat', num_predictions,
                         line=dict(color='rgb(31, 119, 180)'))
    actual = create_go('Actual', 'y', num_values,
                       marker=dict(color="red"))
    
    # In this case the order of the series is important because of the filling
    data = [lower_bound, upper_bound, forecast, actual]

    layout = go.Layout(yaxis=dict(title='Posts'), title=title, showlegend = False, autosize=False)
    fig = go.Figure(data=data, layout=layout)
    iplot(fig, show_link=False)

#stabilize variance
def inverse_boxcox(y, lambda_):
    return np.exp(y) if lambda_ == 0 else np.exp(np.log(lambda_ * y + 1) / lambda_)

#%%
#wikipedia daily page views data for Roger Federer, Rafael Nadal, Novak Djokovic, Andy Murray
#https://tools.wmflabs.org/pageviews/?project=en.wikipedia.org&platform=all-access&agent=user&range=all-time&pages=Roger_Federer|Rafael_Nadal|Novak_Djokovic|Andy_Murray
df = pd.read_csv('Posts/Roger Federer/data.csv')
df.head()

#%%
df_roger = df[df.columns[:2]] #isolate df to roger federer
df_roger['Date'] = pd.to_datetime(df_roger['Date']) #convert to datetime object
df_roger.columns = ['ds', 'y'] #rename columns

#change to time series index
df_roger.index = df_roger['ds']
del df_roger['ds']

#%%
#chart daily page views
plotly_df(df_roger, title='Roger Federer')
#data is highly volatile with order-of-magnitude differences b/w a typical day and a high traffic day

#%%
#apply log transform to make data easier to model
#logging converts multiplicative relationships to additive relationships, and by the same token it converts exponential (compound growth) trends to linear trends. By taking logarithms of variables which are multiplicatively related and/or growing exponentially over time, we can often explain their behavior with linear models.
df_roger['y'] = np.log(df_roger['y'])  
#chart
plotly_df(df_roger, title='Roger Federer')

#%%
#reindex and make 'ds' a column again
df_roger = df_roger.reset_index()

#split into test, and train data
prediction_size = 365
train_df_roger = df_roger[:-prediction_size]
train_df_roger.tail()

#%%
#instantiate Prophet model and fit to data
m = Prophet()
m.fit(train_df_roger)

#%%
#create dataframe with full period dates
future = m.make_future_dataframe(periods=prediction_size)
future.tail()

#%%
#make forecast predictions
forecast = m.predict(future)
np.exp(forecast[['yhat', 'yhat_lower', 'yhat_upper']]) #unlog

#%%
#plot forecasted predictions
fig = m.plot(forecast)

#%%
#plot components
fig2 = m.plot_components(forecast)
#trend: goes up in 2017, and is slowly tailing off since then
#weekly: highest sunday and monday
#yearly: highest in January, July, September

#%%
cmp_df = make_comparison_dataframe(df_roger, forecast)
cmp_df.tail()

#%%
#calculate MAPE & MAE
for err_name, err_value in calculate_forecast_errors(cmp_df, prediction_size).items():
    print(err_name, err_value)

#%%
#visualize forecast
show_forecast(cmp_df, prediction_size, 730, 'Roger Federer Page Views')

#%%
#visualize unlogged forecast
cmp_df = cmp_df.apply(lambda x: np.exp(x))
show_forecast(cmp_df, prediction_size, 730, 'Roger Federer Page Views')

#%%
#adding holidays for better fit (grand slams)
#2019
#Australian Open:1/14/19, French Open:5/27/19, Wimbledon:7/1/19, US Open:8/26/19
#2018
#AO:1/15/18, FO:5/28/19, W:7/2/19, UO:8/27/19
#2017
#AO:1/16/17, FO:5/29/17, W:7/3/17, UO:8/28/17
#2016
#AO:1/18/16, FO:5/23/16, W:6/27/16, UO:8/29/16
#2015
#AO:1/19/15, FO:5/25/15, W:6/29/15, UO:8/31/15
grand_slams = pd.DataFrame({  
    'holiday': 'grand_slam',
    # 'ds': pd.to_datetime(['1/19/2015', '5/25/2015', '6/29/2015', '8/31/2015', #start dates
    #                     '1/18/2016', '5/23/2016', '6/27/2016', '8/29/2016', 
    #                     '1/16/2017', '5/29/2017', '7/3/2017', '8/28/2017',
    #                     '1/15/2018', '5/28/2018', '7/2/2018', '8/27/2018',
    #                     '1/14/2019', '5/27/2019', '7/1/2019', '8/26/2019']),
    'ds': pd.to_datetime(['2/1/2015', '6/7/2015', '7/12/2015', '9/13/2015', #finals
                        '1/31/2016', '6/5/2016', '7/10/2016', '9/11/2016', 
                        '1/29/2017', '6/11/2017', '7/16/2017', '9/10/2017',
                        '1/28/2018', '6/10/2018', '7/15/2018', '9/9/2018',
                        '1/27/2019', '6/9/2019', '7/14/2019', '9/8/2019']),
    'lower_window': -14,
    'upper_window': 2,
})

#%%
#new fit with holidays
m1 = Prophet(holidays=grand_slams)  
forecast1 = m1.fit(train_df_roger).predict(future)  

#%%
#plot forecasted predictions
fig = m1.plot(forecast1)

#%%
#plot components
fig2 = m1.plot_components(forecast1)
#

#%%
cmp_df1 = make_comparison_dataframe(df_roger, forecast1)
cmp_df1.tail()

#%%
#calculate MAPE & MAE
for err_name, err_value in calculate_forecast_errors(cmp_df1, prediction_size).items():
    print(err_name, err_value)

#%%
#visualize forecast
show_forecast(cmp_df1, prediction_size, 730, 'Roger Federer Page Views')

#%%
#visualize unlogged forecast
cmp_df1 = cmp_df1.apply(lambda x: np.exp(x))
show_forecast(cmp_df1, prediction_size, 730, 'Roger Federer Page Views')


#%%
#post:
'''
TDL:
need to figure out how to embed plotly charts

A couple of weeks ago, one of my coworker's introduced me to Prophet, and since then I've been meaning to mess around with the software to create some forecasts. While at my previous job, an enormous amount of effort went into creating time series regression models to forecast the effects that marketing would have on business KPI's, and to see a software that makes forecasting so much quicker and more accessible was really intriguing. 

I finally got around to choosing some time series data I wanted to work with, which ended up being the daily number of page views for the wikipedia page of the greatest tennis player of all time. The data was easily obtained from https://tools.wmflabs.org/pageviews/?project=en.wikipedia.org&platform=all-access&agent=user&range=all-time&pages=Roger_Federer|Rafael_Nadal|Novak_Djokovic|Andy_Murray, and after some quick data manipulation, I plotted out the page views. 

It's quickly apparent that the data has periods of low volume, and then has sudden large order of magnitude differences in short periods of extremely high volume. This makes a ton of sense, as the average tennis fan only really tunes in and thinks about Federer during the Grand Slams. To verify this, we can look at some of the high volume days:

There's a little bit of leadup throughout the tournament, but it isn't until championship day that the volume goes crazy

1/29/2017 - Roger vs. Rafa in the Australian Open Final; Federer's first grand slam since the 2012 Wimbledon title

7/16/2017 - Roger Wimbledon championship

1/28/2018 - Australian Open Championship

Additionally, on the smaller spikes:

9/14/2015 - day after federer lost to djokovic in the us open final

6/10/2018 - day when Nadal won french open. Fed didn't play, but had Nadal performed poorly, he would have lost his #1 ranking to Federer

1/27/2019 - Day of Australian Open Final, though he lost in fourth round. It looks like Fed always has a spiek on days of finals even if he doesn't win/show up in final/enter tournament

Due to the multiplicative nature of the data, I took logs of the data to make it easier to model. I also split the data into training and testing sets for cross validation, with the testing data being the latest year of data availability. Plugging the training data into Prophet provided the following forecast and plot components. 

The forecast seems to do a decent job at catching the lower volume points and inflection points, but misses by a significant margin of magnitude for the spikes. For the trend components, we can se that the trend goes up in 2017, and has been tailing off since, the days of the week with the highest volume are Sunday and Monday, and the yearly seasonality spikes during grand slams and larger ATP 1000 tournaments. When calculating the MAPE, we end up with 42.4%, which is way too high. 

With our initial forecast out of the way, I modeled grand slams into the model as well using the holiday argument, and included the dates while instructing Prophet to include into the lookback and lookahead windows 14 days behind, and 2 days ahead. 

This brings MAPE down to 33.6%, and the large spikes are fitting a lot more nicely. However, there are still a number of spikes that are not being fitted correctly by Prophet. A closer examination at these shows that these are other tournaments that Federer has won during this time period. 

How to improve MAPES
-add regressors for clay court season as fed usually is more irrelevant
-add big tournaments that fed usually wins (this would kind of be covered by seasonality though, no?)

-maybe this is just difficult to predict :(


'''
