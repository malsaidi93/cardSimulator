import streamlit as st
import numpy as np
import plotly.graph_objects as go

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

    # Plotting with Plotly
    fig = go.Figure()

    if show_merged:
        # Plot merged total debt graph
        total_accumulated_debt = np.sum([accumulated_debts[card['name']] for card in cards], axis=0)
        fig.add_trace(go.Scatter(x=months / 12, y=total_accumulated_debt, mode='lines', name="Total Debt", line=dict(color='red')))
        fig.update_layout(title="Total Debt Accumulation Over Time", xaxis_title="Years", yaxis_title="Amount ($)")
    else:
        # Plot individual graphs for each card
        for card in cards:
            fig.add_trace(go.Scatter(x=months / 12, y=accumulated_debts[card['name']], mode='lines', name=card['name']))

        fig.update_layout(title="Debt Accumulation Over Time by Card", xaxis_title="Years", yaxis_title="Amount ($)")

    # Display the interactive Plotly graph
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()
