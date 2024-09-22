import streamlit as st

# Title of the main page
st.title('Performance Dashboard')

# Sidebar for navigation
st.sidebar.title('Navigation')
option = st.sidebar.radio('Select an option:', ('Individual Performance', 'Player Comparison'))

if option == 'Individual Performance':
    st.header('Individual Performance')
    # Add widgets and charts for individual performance here
    st.write('Here you can view individual performance metrics.')

elif option == 'Player Comparison':
    st.header('Player Comparison')
    # Add widgets and charts for player comparison here
    st.write('Here you can compare different players.')

# Run this in your command prompt or terminal to start the Streamlit app:
# streamlit run your_script_name.py
