''' 因子研究 - 回測結果分析 '''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Report:
    
    def __init__(self, factor: pd.DataFrame, payoff: pd.DataFrame, payoff_table: pd.DataFrame, equity_table: pd.DataFrame):
        """
        因子表、當沖報酬表、每日報酬表、每日淨值表
        """
        self.factor = factor
        self.payoff = payoff
        self.payoff_table = payoff_table
        self.equity_table = equity_table

    def display(self, name: str = 'Unnamed Factor'):
        """
        繪製淨值走勢圖
        """
        ### 分組淨值走勢
        plt.style.use('bmh')
        plt.figure(figsize=(12, 6), dpi=200)
        for col in self.equity_table.columns:
            if col[0] == 'G':
                plt.plot(self.equity_table[col], label=col)
        plt.legend()
        plt.ylabel('Equity')
        plt.xlabel('Time')
        plt.title('Grouping Result', fontsize=16)

        ### 多空對沖淨值走勢
        plt.style.use('bmh')
        plt.figure(figsize=(12, 6), dpi=200)
        plt.plot(self.equity_table.hedge, label='hedge')
        plt.plot(self.equity_table.benchmark, label='benchmark')
        plt.legend()
        plt.ylabel('Equity')
        plt.xlabel('Time')
        plt.title(name, fontsize=16)

    def stats(self):
        """
        詳細回測數據
        """
        factor_rank = self.factor.rank(axis=1)
        payoff_rank = self.payoff.rank(axis=1)
        ic = self.payoff.corrwith(self.factor.shift(1), axis=1)
        ic_rank = payoff_rank.corrwith(factor_rank.shift(1), axis=1)
        ir = (ic.mean() / ic.std()) * np.sqrt(252)
        ir_rank = (ic_rank.mean() / ic_rank.std()) * np.sqrt(252)
        period = len(self.payoff_table.index)
        totalRet = self.equity_table.hedge[-1] - 1
        totalRetBM = self.equity_table.benchmark[-1] - 1
        ret = (1+totalRet)**(252/period) - 1 if totalRet > -1 else -((1-totalRet)**(252/period) - 1)
        retBM = (1+totalRetBM)**(252/period) - 1 if totalRetBM > -1 else -((1-totalRetBM)**(252/period) - 1)
        vol = self.payoff_table.hedge.std() * np.sqrt(252)
        mdd = abs((self.equity_table.hedge / self.equity_table.hedge.cummax() - 1).min())
        winRate = (self.payoff_table.hedge > 0).sum() / len(self.payoff_table.hedge)
        info = (self.payoff_table.excess_return.mean() / self.payoff_table.excess_return.std()) * np.sqrt(252)

        result = pd.Series(
            data=[
                np.round(ic.mean(), 2),
                np.round(ic_rank.mean(), 2),
                np.round(ir, 2),
                np.round(ir_rank, 2),
                np.round(totalRet*100, 2),
                np.round(totalRetBM*100, 2),
                np.round(ret*100, 2),
                np.round(retBM*100, 2),
                np.round(vol*100, 2),
                np.round(mdd*100, 2),
                np.round(winRate*100, 2),
                np.round(info, 2)
            ],
            index=[
                'IC Mean',
                'Rank IC',
                'ICIR',
                'Rank ICIR',
                'Total Return [%]',
                'Total Benchmark Return [%]',
                'Return [%]',
                'Benchmark Return [%]',
                'Volatility [%]',
                'MDD [%]',
                'Win Rate [%]',
                'Information Ratio'
            ]
        )

        return result