from typing import List

from pandas import Timestamp

from tm import StockDataProvider
from tm.trading_rules import BollingerBaender
from tm.trading_rules import ChandelierExit
from tm.trading_rules import TradingRule


def filter_for_active_rules(chromosome: List[int], trading_rules: List[TradingRule]) -> List[TradingRule]:
    # Resulting list of active rules
    active_rules = []
    # The currently considered on_off_index in the chromosome
    on_off_index = 0
    for rule in trading_rules:
        on_off_index += sum(rule.num_bits)
        # TODO: Hardcoded instance check is dirty and should be solved via an abstract StopLoss class for production usage
        if chromosome[on_off_index] == 1 or isinstance(rule, ChandelierExit) or isinstance(rule, BollingerBaender):
            active_rules.append(rule)
    return active_rules


def map_chromosome_to_trading_rule_parameters(chromosome: List[int], trading_rules: List[TradingRule]) -> List[List[int]]:
    # Resulting list of parameters
    parameters = []
    # The currently considered index in the chromosome
    current_index = 0
    for rule in trading_rules:
        rule_parameters = []
        for bits in rule.num_bits:
            bit_values = chromosome[current_index:current_index + bits]
            # Convert bit_values to integer
            int_value = int(''.join(map(str, bit_values)), 2)
            rule_parameters.append(int_value)
            current_index += bits
        # Add one bit for each rule because this is the on_off_index in the chromosome
        current_index += 1
        parameters.append(rule_parameters)
    return parameters


def calculate_absolute_buy_and_hold_returns(stock_data_provider: StockDataProvider, transaction_costs_percentage: int = 0.0025, early_out: Timestamp = None) -> float:
    if early_out is not None:
        last_price = stock_data_provider.history['Close'].loc[early_out]
    else:
        last_price = stock_data_provider.history['Close'].iloc[-1]
    first_price = stock_data_provider.history['Close'].iloc[0]
    transaction_costs = first_price * transaction_costs_percentage
    transaction_costs += last_price * transaction_costs_percentage

    return last_price - first_price - transaction_costs
