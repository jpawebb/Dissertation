# -*- coding: utf-8 -*-
"""
FTSE 100 REPLICATION

@author: 44738
"""

import pandas as pd
import pandas_datareader as web
import inspireapi as inspire 
from datetime import datetime as dt 
from datetime import timedelta 
import numpy as np 
from pandas_datareader import data as pdr
import yfinance as yfin
import matplotlib.pyplot as plt
import matplotlib 
import matplotlib.dates as m
from matplotlib.ticker import MaxNLocator


url = 'https://en.wikipedia.org/wiki/FTSE_100_Index#Constituents_in_June_2021'
dfs = pd.read_html(url)
component_data = dfs[3]
symbols = list(component_data['EPIC'])
component_data.set_index('EPIC', inplace=True)

all_returns = {}

end = dt.today() 
start = end - timedelta(days=365)

print(f'Getting returns and impact scores for {len(symbols)} stocks')

return_data = {}

for stock in symbols:  
    try:
        # data = web.get_data_yahoo(stock, start, end)
        # returns = np.array(data['Adj Close'].pct_change())[1:]
        # company_return = np.sum(returns)
        impact_score = inspire.get_insight(stock)['impact_score']

        return_data[stock] = dict(score=impact_score)
        index = symbols.index(stock)
        print(f'{impact_score} | {stock}   {round(index / len(symbols) * 100, 2)}% complete')
    except Exception as e:
        print(e)
        print(f'Exception in getting stock data for {stock}')
        
final_df = pd.DataFrame.from_dict(return_data).T
final_df = final_df.sort_values(by='score', ascending=False)

mask =  final_df['score'] > 0
screened_df = final_df[mask]


""" Due to different weighting method, I have to pull the weights from latest
    weights factsheet on ftserussell.com """

weights = screened_df.copy()
weights = weights.drop(columns=['score'])
weights_list = [0.44, 1.08, 0.5, 0.98, 0.32, 0.47, 2.24, 0.49, 0.28, 0.5,
                0.41, 0.25, 0.61, 0.47, 1.49, 0.5, 0.72, 0.37, 0.29, 0.47, 
                0.21, 1.4, 0.42, 0.31, 0.34, 0.92, 0.38, 0.36, 0.26, 0.37,
                0.36, 0.35, 0.28, 1.89, 0.35, 0.84, 0.29, 0.39, 0.26, 3.36,
                0.75, 0.67, 0.52, 0.09, 0.55, 0.43, 0.22, 0.44, 0.33, 0.27,
                0.0, 0.89, 0.33, 0.56, 0.32, 1.67, 1.71]

# weights = weights.drop('ITV')

weights['raw_weight'] = weights_list
print(weights)
total = weights['raw_weight'].sum()
weights['new_weights'] = (weights['raw_weight'] / total)

print(list(weights['new_weights']))





