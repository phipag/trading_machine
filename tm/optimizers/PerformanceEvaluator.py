from typing import List

import pandas as pd

from tm.trading_rules import TradingRule


class PerformanceEvaluator:
    """
    A class which should calculate different performance metrics given a list of trading rule instances with initialized parameters.
    Please note that the trading rules hold the stock data as pandas Series in the property "TradingRule.history"
    """
    __trading_rules: List[TradingRule]
    __buy_signals: pd.Series
    __sell_signals: pd.Series
    __closing_prices: pd.Series

    def __init__(self, trading_rules: List[TradingRule]):
        # Trading Rules should not be empty
        if len(trading_rules) == 0:
            raise ValueError('Cannot calculate performance for an empty list of trading rules.')

        # Validate that all trading rules hold the same market data
        if len(trading_rules) > 1:
            base_history = trading_rules[0].history
            for rule in trading_rules[1:]:
                if len(rule.history[rule.history['Close'] != base_history['Close']]) != 0:
                    raise ValueError('Please make sure that all trading rule instances hold the same market data.')

        self.__trading_rules = trading_rules
        # Possible because all rules hold the same market data at this point
        self.__closing_prices = trading_rules[0].history['Close']

        # Calculate buy signals and sell signals
        self.__buy_signals = pd.Series(data=True, index=self.__closing_prices.index)
        self.__sell_signals = pd.Series(data=True, index=self.__closing_prices.index)
        for rule in self.__trading_rules:
            # TODO: Improve this rule ("Buy and sell only if all rules say it")
            self.__buy_signals &= rule.buy_signals()
            self.__sell_signals &= rule.sell_signals()

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
        if first_sell_signal_date < first_buy_signal_date:
            self.__sell_signals[first_sell_signal_date] = False

        # Now we are ready to calculate profit: There is at least one buy and one sell signal, the first signal is always a buy signal and the last signal is always a sell signal
        # TODO: No we are not yet :-D The number of sell signals does not match the number of buy signals -.-
