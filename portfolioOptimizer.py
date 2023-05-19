#Uses MIP
import numpy as np
from scipy.optimize import minimize

def optimize_portfolio_with_transaction_costs(returns, transaction_costs):
    num_assets = len(returns)

    def objective(weights):
        portfolio_return = np.sum(returns * weights)
        return -portfolio_return

    def constraint(weights):
        return np.sum(weights) - 1.0

    bounds = [(0, 1) for _ in range(num_assets)]
    constraints = [{'type': 'eq', 'fun': constraint},
                   {'type': 'ineq', 'fun': lambda x: transaction_costs - np.sum(np.abs(x - initial_weights))}]

    initial_weights = np.ones(num_assets) / num_assets

    result = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    optimal_weights = result.x

    return optimal_weights

def print_weights(optimal_weights):
    print("Optimal Portfolio Weights:", optimal_weights)

# Example usage
returns = np.array([0.05, 0.03, 0.04, 0.02])
transaction_costs = np.array([0.01, 0.02, 0.015, 0.01])

optimal_weights = optimize_portfolio_with_transaction_costs(returns, transaction_costs)
print_weights(optimal_weights)
