''' 因子研究 - 因子分組與報酬計算 '''

import pandas as pd
import numpy as np
from Factor.report import Report

class Backtest:

    def __init__(self, factor: pd.DataFrame, payoff: pd.DataFrame):
        """
        因子表、當沖損益表
        """
        self.factor = factor
        self.payoff = payoff

    def sim(self, ngroups: int):
        """
        模擬回測績效並產生各類報表
        """
        ### 依因子值大小分組
        factor_ = self.factor.stack().reset_index()
        factor_.columns = ['datetime', 'asset', 'Factor']

        def group(x):
            x['group'] = pd.qcut(x.Factor, ngroups, labels=list(range(1, ngroups+1)))
            return x

        factor_ = factor_.groupby('datetime', group_keys=False).apply(group)
        factor_pvt = factor_.pivot(index='datetime', columns='asset', values='group')
        
        payoff_table = pd.DataFrame()
        for i in range(1, ngroups+1):
            l = [*range(1, ngroups+1)] + [np.nan]
            l.remove(i)
            weight = factor_pvt.replace(l, 0)
            weight = weight.replace(i, 1)
            weight = weight.shift(1).astype(np.float64).fillna(0)
            payoff_ = (weight * self.payoff).dropna(how='all')
            payoff_table['G'+str(i)] = (payoff_.sum(axis=1) / weight.sum(axis=1)).fillna(0)    

        taiex = pd.read_feather('/Users/kuanhsu/Desktop/code/Python/FILE/報酬指數.ftr')
        taiex = taiex.set_index('datetime', drop=True)
        taiex.index = pd.to_datetime(taiex.index)
        taiex = taiex.reindex(weight.index)
        taiex['payoff'] = taiex.Close.pct_change(1)  
        taiex = taiex.fillna(0)

        payoff_table['hedge'] = payoff_table['G1'] - payoff_table['G'+str(ngroups)]
        payoff_table['benchmark'] = taiex.payoff
        payoff_table['excess_return'] = payoff_table.hedge - payoff_table.benchmark
        equity_table = payoff_table.cumsum() + 1

        return Report(self.factor, self.payoff, payoff_table, equity_table)