import math
from scipy.stats import norm 
import tkinter as tk
from tkinter import messagebox


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
# GUI Function
def calculate_option():
    try:
        # Getting values from the GUI fields
        stock_price = float(entry_stock_price.get())
        strike_price = float(entry_strike_price.get())
        time_to_expiration = float(entry_time_to_expiration.get())
        risk_free_rate = float(entry_risk_free_rate.get())
        volatility = float(entry_volatility.get())
        option_type = option_var.get()

        # Calculate the option price
        option_price = black_scholes_option_price(
            current_stock_price=stock_price,
            strike_price=strike_price,
            time_to_expiration_years=time_to_expiration,
            risk_free_rate=risk_free_rate,
            volatility=volatility,
            option_type=option_type
        )

        # Show the result
        messagebox.showinfo("Option Price", f"The {option_type} option price is: ${option_price:.2f}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")

# Create main window
root = tk.Tk()
root.title("Black-Scholes Option Calculator")

# Set window size
root.geometry("400x400")

# Create Labels and Entry fields
label_stock_price = tk.Label(root, text="Enter Stock Price (S):")
label_stock_price.pack()

entry_stock_price = tk.Entry(root)
entry_stock_price.pack()

label_strike_price = tk.Label(root, text="Enter Strike Price (K):")
label_strike_price.pack()

entry_strike_price = tk.Entry(root)
entry_strike_price.pack()

label_time_to_expiration = tk.Label(root, text="Enter Time to Expiration (years):")
label_time_to_expiration.pack()

entry_time_to_expiration = tk.Entry(root)
entry_time_to_expiration.pack()

label_risk_free_rate = tk.Label(root, text="Enter Risk-Free Rate (as decimal, e.g., 0.05 for 5%):")
label_risk_free_rate.pack()

entry_risk_free_rate = tk.Entry(root)
entry_risk_free_rate.pack()

label_volatility = tk.Label(root, text="Enter Volatility (as decimal, e.g., 0.2 for 20%):")
label_volatility.pack()

entry_volatility = tk.Entry(root)
entry_volatility.pack()

# Option type (Call or Put)
option_var = tk.StringVar(value="call")  # Default option type
label_option_type = tk.Label(root, text="Select Option Type:")
label_option_type.pack()

radio_call = tk.Radiobutton(root, text="Call", variable=option_var, value="call")
radio_call.pack()

radio_put = tk.Radiobutton(root, text="Put", variable=option_var, value="put")
radio_put.pack()

# Calculate button
calculate_button = tk.Button(root, text="Calculate Option Price", command=calculate_option)
calculate_button.pack(pady=20)

# Run the main event loop
root.mainloop()