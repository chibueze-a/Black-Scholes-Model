import math
from scipy.stats import norm # type: ignore

def black_scholes_option_price(
    current_stock_price,
    strike_price,
    time_to_expiration_years,
    risk_free_rate,
    volatility,
    option_type='call'
):
    """
    Calculate the Black-Scholes price for a European call or put option.

    Parameters:
    current_stock_price : float : Current price of the underlying stock (S)
    strike_price : float : Strike price of the option (K)
    time_to_expiration_years : float : Time to expiration in years (T)
    risk_free_rate : float : Risk-free annual interest rate (r)
    volatility : float : Annualized standard deviation of the stock’s returns (σ)
    option_type : str : 'call' or 'put'

    Returns:
    float : Option price based on the Black-Scholes model
    """
    numerator = math.log(current_stock_price / strike_price) + \
                (risk_free_rate + 0.5 * volatility**2) * time_to_expiration_years
    denominator = volatility * math.sqrt(time_to_expiration_years)
    
    d1 = numerator / denominator
    d2 = d1 - volatility * math.sqrt(time_to_expiration_years)
    
    if option_type == 'call':
        option_price = (
            current_stock_price * norm.cdf(d1)
            - strike_price * math.exp(-risk_free_rate * time_to_expiration_years) * norm.cdf(d2)
        )
    elif option_type == 'put':
        option_price = (
            strike_price * math.exp(-risk_free_rate * time_to_expiration_years) * norm.cdf(-d2)
            - current_stock_price * norm.cdf(-d1)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    return option_price


# ------------------------------------------------------------

stock_price = 100.0
strike_price = 100.0
time_to_expiration = 1.0  # years
risk_free_interest_rate = 0.05  # 5%
volatility = 0.2  # 20%

call_option_price = black_scholes_option_price(
    current_stock_price=stock_price,
    strike_price=strike_price,
    time_to_expiration_years=time_to_expiration,
    risk_free_rate=risk_free_interest_rate,
    volatility=volatility,
    option_type='call'
)

put_option_price = black_scholes_option_price(
    current_stock_price=stock_price,
    strike_price=strike_price,
    time_to_expiration_years=time_to_expiration,
    risk_free_rate=risk_free_interest_rate,
    volatility=volatility,
    option_type='put'
)

print(f"Call Option Price: ${call_option_price:.2f}")
print(f"Put Option Price:  ${put_option_price:.2f}")