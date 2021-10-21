import numpy as np


def calculate_execution_prices(mid, prices, amounts, volumes):
    """
    The method for calculating average execution prices of aggressive buy or sell. If the book does not have enough
    orders to execute a particular volume the price will be approximated. Given x as the maximum volume that can be
    executed, p the execution price, and v the desired volume we approximate the price as:
    mid + (p - mid) / x * v

    :param mid: current mid price
    :param prices: array-like of prices on one side of the book
    :param amounts: array-like of amounts on one side of the book
    :param volumes: array-like of volumes to buy/sell aggressively from the book
    :return: np.array of average execution prices
    """
    prices = np.array(prices)
    amounts = np.array(amounts)
    volumes = np.array(volumes)

    cumulative_volumes = np.cumsum(prices * amounts)
    total_volume = cumulative_volumes[-1]
    clipped_volumes = np.clip(volumes, a_min=None, a_max=total_volume)
    cumulative_amounts = np.cumsum(amounts)
    indices = np.searchsorted(cumulative_volumes, clipped_volumes)

    # Need to subtract the excessive amount
    excessive_amounts = (cumulative_volumes[indices] - clipped_volumes) / prices[indices]
    execution_prices = clipped_volumes / (cumulative_amounts[indices] - excessive_amounts)

    # Do the approximation if necessary.
    insufficient_amount_indices = volumes == clipped_volumes
    execution_prices[~insufficient_amount_indices] = mid + (execution_prices[~insufficient_amount_indices] - mid) \
                                                     / total_volume * volumes[~insufficient_amount_indices]

    return execution_prices
