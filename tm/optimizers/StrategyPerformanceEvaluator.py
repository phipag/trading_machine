import operator
from functools import reduce
from typing import List

import pandas as pd

from tm.trading_rules import TradingRule


class StrategyPerformanceEvaluator:
    """
    A class which should calculate different performance metrics given a list of trading rule instances with initialized parameters.
    Please note that the trading rules hold the stock data as pandas Series in the property "TradingRule.history"
    """
    TRANSACTION_COSTS: int = 0.0025

    def __init__(self, trading_rules: List[TradingRule]):
        # Trading Rules should not be empty
        if len(trading_rules) == 0:
            raise ValueError('Cannot calculate performance for an empty list of trading rules.')

        # Validate that all trading rules hold the same market data (if there is more than one rule)
        if len(trading_rules) > 1:
            base_history = trading_rules[0].history
            for rule in trading_rules[1:]:
                if len(rule.history[rule.history['Close'] != base_history['Close']]) != 0:
                    raise ValueError('Please make sure that all trading rule instances hold the same market data.')

        self.__trading_rules: List[TradingRule] = trading_rules
        # Possible because all rules hold the same market data at this point
        self.__closing_prices: pd.Series = trading_rules[0].history['Close']

        # TODO: Improve this rule ("Buy and sell only if all rules say it")
        # Note: reduce function over bitwise and is faster than manual iteration
        self.__buy_signals: pd.Series = pd.Series(data=reduce(operator.and_, map(lambda rule: rule.buy_signals(), self.__trading_rules)), index=self.__closing_prices.index)
        self.__sell_signals: pd.Series = pd.Series(data=reduce(operator.and_, map(lambda rule: rule.sell_signals(), self.__trading_rules)), index=self.__closing_prices.index)

    def calculate_net_profit(self) -> float:
        # If nothing is bought, profit is 0
        if len(self.__buy_signals[self.__buy_signals == True]) == 0:
            return 0.0

        # If no sell signal is generated insert it manually in the end
        if len(self.__sell_signals[self.__sell_signals == True]) == 0:
            self.__sell_signals.iloc[-1] = True

        # If the last signal is a buy signal, add a sell signal in the end
        last_sell_signal_date = self.__sell_signals[self.__sell_signals == True].index[-1]
        last_buy_signal_date = self.__buy_signals[self.__buy_signals == True].index[-1]
        if last_sell_signal_date < last_buy_signal_date:
            self.__sell_signals.iloc[-1] = True

        # If the first signal is a sell signal, remove it, because nothing can be sold before something has been bought
        first_sell_signal_date = self.__sell_signals[self.__sell_signals == True].index[0]
        first_buy_signal_date = self.__buy_signals[self.__buy_signals == True].index[0]
        if first_sell_signal_date <= first_buy_signal_date:
            self.__sell_signals[first_sell_signal_date] = False

        # Now we are ready to calculate profit: There is at least one buy and one sell signal, the first signal is always a buy signal and the last signal is always a sell signal
        # Attention: There might still be a mismatch between the number of sell signals and the number of buy signals
        buy_sell_signals = pd.concat([self.__buy_signals[self.__buy_signals == True], self.__sell_signals[self.__sell_signals == True]], axis=1)
        buy_sell_signals.columns = ['buy', 'sell']
        buy_sell_signals = buy_sell_signals.loc[(buy_sell_signals['buy'].shift(1) != buy_sell_signals['buy']) & (buy_sell_signals['sell'].shift(1) != buy_sell_signals['sell'])]

        # Simulate transaction costs
        transaction_costs = self.__closing_prices.loc[buy_sell_signals[buy_sell_signals['buy'] == True].index].sum() * self.TRANSACTION_COSTS

        # Calculate net profit
        net_profit = self.__closing_prices.loc[buy_sell_signals[buy_sell_signals['sell'] == True].index].sum() - self.__closing_prices.loc[
            buy_sell_signals[buy_sell_signals['buy'] == True].index].sum()

        # Return net profit - transaction costs
        return net_profit - transaction_costs
