import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Compound interest function
def calculate_compound_interest(P, r, t, n=12):
    return P * (1 + r/n)**(n*t)

# Streamlit app
def main():
    st.title("Credit Card Debt Compound Interest Simulator")
    
    # Input fields for initial debt, APR, and years
    principal = st.number_input("Enter the initial debt amount ($)", min_value=0.0, value=1000.0)
    apr = st.number_input("Enter the APR (Annual Percentage Rate in %)", min_value=0.0, value=20.0) / 100
    years = st.slider("Choose the number of years", min_value=1, max_value=30, value=5)
    
    # Create time range for X years
    months = np.arange(0, years * 12 + 1, 1)
    
    # Calculate the debt accumulation over time
    accumulated_debt = [calculate_compound_interest(principal, apr, month/12) for month in months]
    
    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(months / 12, accumulated_debt, label="Accumulated Debt", color='r')
    plt.xlabel("Years")
    plt.ylabel("Amount ($)")
    plt.title("Debt Accumulation Over Time")
    plt.grid(True)
    plt.legend()
    
    # Display the plot
    st.pyplot(plt)

if __name__ == '__main__':
    main()
