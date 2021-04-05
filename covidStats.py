import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import math
import datetime

import datetime

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression


# %matplotlib inline


def getCovidVisualization():
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv', parse_dates=['Date'])
    df['Total Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)

    #Worldwide Cases

    worldwide_df = df.groupby(['Date']).sum()
    w_chart = worldwide_df.plot(figsize=(10,7))
    w_chart.set_xlabel('Date')
    w_chart.set_ylabel('# of Cases WorldWide')
    w_chart.title.set_text('Covid-19 Visualization')
    plt.savefig('static/worldCases.png')


    #United States vs.s Worldwide Cases and Deaths
    us_df = df[df['Country'] == 'US'].groupby(['Date']).sum()

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111)

    ax.plot(worldwide_df[['Total Cases']], label = "Worldwide")
    ax.plot(us_df[['Total Cases']], label = "United States")

    ax.set_xlabel('Date')
    ax.set_ylabel('# of Cases Total Cases')
    ax.title.set_text('World vs United States Total Cases')

    plt.legend(loc = 'upper left')
    plt.savefig('static/worldvsus.png')


    #Daily United States Cases and Deaths
    us_df = us_df.reset_index()
    us_df['Daily Confirmed'] = us_df['Confirmed'].sub(us_df['Confirmed'].shift())
    us_df['Daily Deaths'] = us_df['Deaths'].sub(us_df['Deaths'].shift())

    fig = plt.figure(figsize=(10,7))
    ax = fig.add_subplot(111)

    ax.bar(us_df['Date'], us_df['Daily Confirmed'], color='b', label='US Daily Confirmed Cases')
    ax.bar(us_df['Date'], us_df['Daily Deaths'], color='r', label='US Daily Deaths')

    ax.set_xlabel('Date')
    ax.set_ylabel('# of Cases and Deaths')

    ax.title.set_text('US Daily Cases and Deaths')
    plt.legend(loc='upper left')
    plt.savefig('static/usCasesAndDeaths.png')

    # Commented out IPython magic to ensure Python compatibility.

def getMLPrediction():
    df1 = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv',
                      parse_dates=['Date'])
    df1['Total Cases'] = df1[['Date', 'Country', 'Confirmed', 'Recovered', 'Deaths']].sum(axis=1)

    df = pd.DataFrame()
    df['Date'] = df1['Date']
    df['Cases'] = df1[['Date', 'Country', 'Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    df.tail(20)

    print(df['Cases'].size)
    slices = pd.DataFrame()
    n = 7  # Only provide 7 datapoints to predict
    for i in range(n + 1):
        name = f'Input{i + 1}' if i != n else 'Answer'
        slices[name] = df['Cases'].iloc[0 + i:df['Cases'].size - n + i].to_numpy()
    slices.tail(8)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x = slices['Input2']
    y = slices['Input6']
    ax.scatter(x, y, slices['Answer'], c=x + y)

    print(slices.columns)
    x = slices[[f'Input{i + 1}' for i in range(7)]]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    lrModel = LinearRegression()
    lrModel.fit(x_train, y_train)

    confidence = lrModel.score(x_test, y_test)
    print(confidence)
    lrModel.predict([x_test.iloc[10]])
    print(lrModel.predict([x_test.iloc[0]]), y_test.iloc[0])

    queueOfVals = slices.iloc[slices['Answer'].size - 1]
    del queueOfVals['Answer']
    for i in range(7):
        prediction = lrModel.predict([queueOfVals])
        newDataframe = pd.DataFrame()
        dictOfValues = {f'Input{i + 1}': queueOfVals.iloc[i + 1] for i in range(6)}
        dictOfValues['Input7'] = prediction
        newDataframe = newDataframe.append(dictOfValues, ignore_index=True)
    print(queueOfVals['Input1'])
    allPredictions = [queueOfVals[f'Input{i + 1}'] for i in range(7)]
    print(allPredictions)
    queueOfVals.head(10)

    plt.figure(figsize=(10, 5))
    ax = fig.add_axes([0, 0, 1, 1])

    low = min(allPredictions)
    high = max(allPredictions)
    plt.ylim([math.ceil(low - 0.5 * (high - low)), math.ceil(high + 0.5 * (high - low))])
    plt.ylabel('Number of Cases')
    plt.xlabel('Date')
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(7)]
    plt.bar(height=allPredictions, x=date_list)
    plt.savefig('static/predictionCovid.png')


