import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv('player_stats.csv')

data = load_data()

# Function to calculate integer stats
def convert_to_int(df):
    int_columns = ['Goals', 'Assists', 'Minutes', 'Shots Total', 'Shots On', 'Key Passes',
                   'Yellow Cards', 'Red Cards', 'Duels Total', 'Duels Won', 'Penalties Scored', 'Penalties Missed', 'Appearances']
    df[int_columns] = df[int_columns].fillna(0).astype(int)
    return df

# Radar chart function without calculated columns and adjusted label distance
def radar_chart(df, players, stats):
    num_vars = len(stats)

    # Set up the radar chart layout
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Complete the loop

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Find the max and min values for each stat to normalize them
    max_values = df[stats].max().values
    min_values = df[stats].min().values

    # Draw one radar chart per player
    for player in players:
        player_data = df[df['Name'] == player][stats].values.flatten()
        normalized_data = [(value - min_val) / (max_val - min_val) if max_val != min_val else 0
                           for value, max_val, min_val in zip(player_data, max_values, min_values)]
        normalized_data += normalized_data[:1]  # Complete the loop
        ax.plot(angles, normalized_data, linewidth=2, label=player)
        ax.fill(angles, normalized_data, alpha=0.25)

    # Add labels to each axis
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stats, fontsize=12)


    # Remove y-ticks for each axis (no scale display)
    ax.set_yticklabels([])  # Hide radial grid labels
    ax.spines['polar'].set_visible(False)
    ax.grid(color='lightgrey', linewidth=0.8)

    # Show the legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    st.pyplot(fig)



# Display statistics as cards under the radar chart
def display_stats_as_cards(df, players, stats):
    for player in players:
        st.subheader(f'Statistics for {player}')
        player_data = df[df['Name'] == player][stats].iloc[0]

        cols_per_row = 3  # You can adjust the number of columns per row
        stat_items = list(player_data.items())  # Convert ItemsView to list

        # Iterate through the stats and display them in rows and columns
        for i in range(0, len(stat_items), cols_per_row):
            cols = st.columns(min(cols_per_row, len(stat_items) - i))
            for col, (stat, value) in zip(cols, stat_items[i:i + cols_per_row]):
                col.metric(label=stat, value=f"{int(value) if isinstance(value, (int, float)) and value.is_integer() else f'{value:.2f}'}")

# Title of the main page
st.title('Who deserves the 2024 Ballon d\'Or?')

# Sidebar for navigation
st.sidebar.title('Navigation')
option = st.sidebar.radio('Select an option:', ('Individual Performance (Deepdive by League)', 'Player Comparison'))

if option == 'Individual Performance (Deepdive by League)':
    st.header('Individual Performance (Deepdive by League)')

    # Player selection
    players = data['Name'].unique()
    selected_player = st.selectbox('Select a Player:', players)

    # Competition selection - dynamically filtered based on selected player
    player_competitions = data[data['Name'] == selected_player]['Competition'].unique().tolist()
    competitions = player_competitions + ['TOTAL']
    selected_competition = st.selectbox('Select a Competition:', competitions)

    # Filter data based on selection
    if selected_competition == 'TOTAL':
        player_data = data[data['Name'] == selected_player]
    else:
        player_data = data[(data['Name'] == selected_player) & (data['Competition'] == selected_competition)]

    if not player_data.empty:
        # Convert integer stats after filtering the data
        player_data = convert_to_int(player_data)

        # Statistics selection (no calculated stats)
        stats_options = ['Appearances', 'Goals', 'Assists', 'Minutes', 'Shots Total', 'Shots On',
                         'Key Passes', 'Yellow Cards', 'Red Cards', 'Duels Total', 'Duels Won',
                         'Penalties Scored', 'Penalties Missed']
        selected_stats = st.multiselect('Select Statistics:', stats_options, default=['Appearances', 'Goals', 'Assists', 'Minutes'])

        # Sum or get the first row based on the selected competition
        if selected_competition == 'TOTAL':
            total_stats = player_data[selected_stats].sum().to_dict()
        else:
            total_stats = player_data[selected_stats].iloc[0].to_dict()

        # Display statistics as cards, placed side by side
        cols_per_row = 3  # You can adjust the number of columns per row
        stat_items = list(total_stats.items())

        # Iterate through the stats and display them in rows and columns
        for i in range(0, len(stat_items), cols_per_row):
            cols = st.columns(min(cols_per_row, len(stat_items) - i))
            for col, (stat, value) in zip(cols, stat_items[i:i + cols_per_row]):
                # Ensure integer stats are displayed without decimals
                col.metric(label=stat, value=f"{int(value)}")
    else:
        st.write("No data available for this player in the selected competition.")

elif option == 'Player Comparison':
    st.header('Player Comparison')

    # Player selection with default "Erling Haaland" and "Vinícius Jr."
    players = data['Name'].unique()
    selected_players = st.multiselect('Select Players:', players, default=['Erling Haaland', 'Vinícius Jr.'])

    # Statistics selection (no calculated stats)
    stats_options = ['Appearances', 'Goals', 'Assists', 'Minutes', 'Shots Total', 'Shots On',
                     'Key Passes', 'Yellow Cards', 'Red Cards', 'Duels Total', 'Duels Won',
                     'Penalties Scored', 'Penalties Missed']
    selected_stats = st.multiselect('Select Statistics for Comparison:', stats_options, default=['Appearances', 'Goals', 'Assists', 'Minutes'])

    if len(selected_players) > 0 and len(selected_stats) > 0:
        st.subheader('Spider Graph Comparison')
        radar_chart(data, selected_players, selected_stats)

        st.subheader('Detailed Statistics for Selected Players')
        display_stats_as_cards(data, selected_players, selected_stats)

# Run this in your command prompt or terminal to start the Streamlit app:
# streamlit run your_script_name.py
