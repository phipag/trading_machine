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
    LENDING_FEE: int = 0.003
    ONE_TIME_COSTS: int = 0

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

        # Buy or sell if at least one rule indicates it
        # Note: reduce function over bitwise and is faster than manual iteration
        self.__buy_signals: pd.Series = pd.Series(data=reduce(operator.or_, map(lambda rule: rule.buy_signals(), self.__trading_rules)), index=self.__closing_prices.index)
        self.__sell_signals: pd.Series = pd.Series(data=reduce(operator.or_, map(lambda rule: rule.sell_signals(), self.__trading_rules)), index=self.__closing_prices.index)

    @property
    def buy_signals(self) -> pd.Series:
        return self.__buy_signals

    @property
    def sell_signals(self) -> pd.Series:
        return self.__sell_signals

    # noinspection PySimplifyBooleanCheck
    def __remove_consecutive_buy_or_sell_signals(self):
        buy_signals = self.__buy_signals.to_numpy()
        sell_signals = self.__sell_signals.to_numpy()
        last_signal = None
        for i in range(len(buy_signals)):
            if buy_signals[i] == True and last_signal == 'buy':
                self.__buy_signals.iloc[i] = False
            elif sell_signals[i] == True and last_signal == 'sell':
                self.__sell_signals.iloc[i] = False
            # If the same signals occur at the same day remove the one which is identical to the last signal
            if buy_signals[i] == True and sell_signals[i] == True:
                if last_signal == 'buy':
                    self.__buy_signals.iloc[i] = False
                else:
                    self.__sell_signals.iloc[i] = False
            if buy_signals[i] == True:
                last_signal = 'buy'
            elif sell_signals[i] == True:
                last_signal = 'sell'

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
        if last_sell_signal_date <= last_buy_signal_date:
            self.__sell_signals.iloc[-1] = True
            self.__buy_signals.iloc[-1] = False

        # Remove all sell signals before the first buy signal, because nothing can be sold before something has been bought
        while True:
            first_sell_signal_date = self.__sell_signals[self.__sell_signals == True].index[0]
            first_buy_signal_date = self.__buy_signals[self.__buy_signals == True].index[0]
            if first_sell_signal_date <= first_buy_signal_date:
                self.__sell_signals.loc[first_sell_signal_date] = False
            else:
                break
        #Remove simultaneous buy and sell signals
        self.__sell_signals[self.__sell_signals & self.__buy_signals] = False
        self.__buy_signals[self.__sell_signals & self.__buy_signals] = False

        # Make sure there are no consecutive buy or sell signals
        self.__remove_consecutive_buy_or_sell_signals()

        # Now we are ready to calculate profit: There is at least one buy and one sell signal, the first signal is always a buy signal and the last signal is always a sell signal
        # Simulate transaction costs
        transaction_costs = self.__closing_prices.loc[self.__buy_signals[self.__buy_signals == True].index].sum() * self.TRANSACTION_COSTS
        transaction_costs += self.__closing_prices.loc[self.__sell_signals[self.__sell_signals == True].index].sum() * self.TRANSACTION_COSTS
        # Calculate net profit
        net_profit = self.__closing_prices.loc[self.__sell_signals[self.__sell_signals == True].index].sum() - self.__closing_prices.loc[self.__buy_signals[self.__buy_signals == True].index].sum()

        # Return net profit - transaction costs
        return net_profit - transaction_costs

    def calculate_net_profit_short(self) -> float:

        # If nothing is sold, profit is 0
        if len(self.__sell_signals[self.__sell_signals == True]) == 0:
            return 0.0

        # If no buy signal is generated insert it manually in the end
        if len(self.__buy_signals[self.__buy_signals == True]) == 0:
            self.__buy_signals.iloc[-1] = True

        # If the last signal is a sell signal, add a buy signal in the end
        last_sell_signal_date = self.__sell_signals[self.__sell_signals == True].index[-1]
        last_buy_signal_date = self.__buy_signals[self.__buy_signals == True].index[-1]
        if last_sell_signal_date >= last_buy_signal_date:
            self.__buy_signals.iloc[-1] = True
            self.__sell_signals.iloc[-1] = False

        # Remove all buy signals before the first sell signal, because nothing can be bought back before something has been sold
        while True:
            first_sell_signal_date = self.__sell_signals[self.__sell_signals == True].index[0]
            first_buy_signal_date = self.__buy_signals[self.__buy_signals == True].index[0]
            if first_buy_signal_date <= first_sell_signal_date:
                self.__buy_signals.loc[first_buy_signal_date] = False
            else:
                break

        # Make sure there are no consecutive buy or sell signals
        self.__remove_consecutive_buy_or_sell_signals()

        # Now we are ready to calculate profit: There is at least one buy and one sell signal, the first signal is always a buy signal and the last signal is always a sell signal
        # Simulate transaction costs
        transaction_costs = self.__closing_prices.loc[self.__buy_signals[self.__buy_signals == True].index].sum() * self.TRANSACTION_COSTS
        transaction_costs += self.__closing_prices.loc[self.__sell_signals[self.__sell_signals == True].index].sum() * self.TRANSACTION_COSTS

        lending_fee = ((self.__sell_signals[self.__sell_signals == True].index - self.__buy_signals[self.__buy_signals == True].index) * self.__closing_prices.loc[self.__sell_signals[self.__sell_signals == True].index].sum() * self.LENDING_FEE) / 360

        # Calculate net profit
        net_profit = self.__closing_prices.loc[self.__sell_signals[self.__sell_signals == True].index].sum() - self.__closing_prices.loc[self.__buy_signals[self.__buy_signals == True].index].sum()

        # Return net profit - transaction costs
        return net_profit - transaction_costs - lending_fee - self.ONE_TIME_COSTS