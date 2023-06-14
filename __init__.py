''' 因子研究 - 因子庫 '''

import pandas as pd
import numpy as np
from Factor.backtest import Backtest


def CPV(data: pd.DataFrame):

    ### 計算日內價量相關係數
    data.datetime = pd.to_datetime(data.datetime).dt.date
    close = data.pivot_table(index='datetime', columns='asset', values='Close', aggfunc=lambda x: list(x))
    volume = data.pivot_table(index='datetime', columns='asset', values='Volume', aggfunc=lambda x: list(x))
    vecF = np.vectorize(lambda x, y: np.corrcoef(x, y)[0][1])
    corr_pvt = pd.DataFrame(vecF(close, volume), index=close.index, columns=close.columns)
    
    pv_corr_avg = corr_pvt.rolling(20).mean()
    pv_corr_avg = pv_corr_avg.sub(pv_corr_avg.mean(axis=1), axis=0)
    pv_corr_avg = pv_corr_avg.div(pv_corr_avg.std(axis=1), axis=0)
    pv_corr_std = corr_pvt.rolling(20).std()
    pv_corr_std = pv_corr_std.sub(pv_corr_std.mean(axis=1), axis=0)
    pv_corr_std = pv_corr_std.div(pv_corr_std.std(axis=1), axis=0)
    pv_corr = pv_corr_avg + pv_corr_std
    pv_corr = pv_corr.ffill()

    open = data.pivot_table(index='datetime', columns='asset', values='Open', aggfunc='first').ffill()
    close = data.pivot_table(index='datetime', columns='asset', values='Close', aggfunc='last').ffill()
    payoff = (close - open) / open

    return Backtest(pv_corr, payoff)

