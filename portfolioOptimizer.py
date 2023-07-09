"""
Module for optimizing a portfolio with transaction costs.
"""

import numpy as np
from scipy.optimize import minimize

def optimize_portfolio_with_transaction_costs(returns_arr, transaction_costs_arr):
    """
    Optimize portfolio with transaction costs.
    """
    num_assets = len(returns_arr)

    def objective(weights):
        portfolio_return = np.sum(returns_arr * weights)
        return -portfolio_return

    def constraint(weights):
        return np.sum(weights) - 1.0

    bounds = [(0, 1) for _ in range(num_assets)]
    initial_weights = np.ones(num_assets) / num_assets
    constraints = [
        {'type': 'eq', 'fun': constraint},
        {'type': 'ineq', 'fun': lambda x: transaction_costs_arr - np.sum(np.abs(x - initial_weights))}
    ]

    result = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    optimal_weights = result.x

    return optimal_weights

def print_weights(opt_weights):
    """
    Print the optimal weights of the portfolio.
    """
    print("Optimal Portfolio Weights:", opt_weights)

# Example usage
returns_example = np.array([0.05, 0.03, 0.04, 0.02])
transaction_costs_example = np.array([0.01, 0.02, 0.015, 0.01])

optimal_weights_example = optimize_portfolio_with_transaction_costs(returns_example, transaction_costs_example)
print_weights(optimal_weights_example)
