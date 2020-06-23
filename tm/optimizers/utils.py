from typing import List

from tm import StockDataProvider
from tm.trading_rules import TradingRule


# TODO: Currently only supports integer values (what happens if a trading rules wants a float parameter?)
def map_chromosome_to_trading_rule_parameters(chromosome: List[int], trading_rules: List[TradingRule]) -> List[List[int]]:
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
            # bits + 1 because the last bit represents the turn on/off binary variable for the trading rule
            current_index += bits + 1
        parameters.append(rule_parameters)
    return parameters


def calculate_absolute_buy_and_hold_returns(stock_data_provider: StockDataProvider) -> float:
    first_price = stock_data_provider.history['Close'].iloc[0]
    last_price = stock_data_provider.history['Close'].iloc[-1]
    return last_price - first_price
