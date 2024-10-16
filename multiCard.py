import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate compound interest
def calculate_compound_interest(P, r, t, n=12):
    return P * (1 + r/n)**(n*t)

# Streamlit app
def main():
    st.title("Multi-Card Credit Card Debt Simulator")

    # Section for adding multiple cards
    st.subheader("Add Credit Cards")
    
    # Number of cards to add
    num_cards = st.number_input("How many credit cards do you want to simulate?", min_value=1, max_value=10, value=1)

    cards = []  # List to store card information
    
    # Loop to display cards in 3-column layout
    for i in range(0, num_cards, 3):  # Iterate in steps of 3
        cols = st.columns(3)  # Create 3 columns
        
        # Display cards in current row
        for j in range(3):
            if i + j < num_cards:  # Ensure we don't exceed the total number of cards
                with cols[j]:  # Display card in this column
                    card_name = st.text_input(f"Card {i+j+1} Name", f"Card {i+j+1}")
                    principal = st.number_input(f"Debt amount for {card_name} ($)", min_value=0.0, value=1000.0, key=f"principal_{i+j}")
                    apr = st.number_input(f"APR for {card_name} (%)", min_value=0.0, value=20.0, key=f"apr_{i+j}") / 100

                    # Store card details
                    cards.append({
                        'name': card_name,
                        'principal': principal,
                        'apr': apr
                    })

    # Select the number of years to simulate
    years = st.slider("Choose the number of years", min_value=1, max_value=30, value=5)

    # Toggle to switch between individual graphs and merged total graph
    show_merged = st.checkbox("Show merged total debt graph")

    # Generate data for each card
    months = np.arange(0, years * 12 + 1, 1)
    accumulated_debts = {}  # Dictionary to store accumulated debt for each card

    for card in cards:
        accumulated_debts[card['name']] = [calculate_compound_interest(card['principal'], card['apr'], month/12) for month in months]

    # Plotting
    plt.figure(figsize=(10, 6))

    if show_merged:
        # Plot merged total debt graph
        total_accumulated_debt = np.sum([accumulated_debts[card['name']] for card in cards], axis=0)
        plt.plot(months / 12, total_accumulated_debt, label="Total Debt", color='r')
        plt.title("Total Debt Accumulation Over Time")
    else:
        # Plot individual graphs for each card
        for card in cards:
            plt.plot(months / 12, accumulated_debts[card['name']], label=card['name'])
        plt.title("Debt Accumulation Over Time by Card")
    
    plt.xlabel("Years")
    plt.ylabel("Amount ($)")
    plt.grid(True)
    plt.legend()
    
    # Display the plot
    st.pyplot(plt)

if __name__ == '__main__':
    main()
