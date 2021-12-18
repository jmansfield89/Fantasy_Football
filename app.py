# SETUP
# Import libraries
import streamlit as st
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from ff_espn_api import League

# Set variables for data import specific to your league
year = 2021
league_id = st.secrets["league_id"]
swid = st.secrets["swid"]  # only needed if your league is private
espn_s2 = st.secrets["espn_s2"]  # only needed if your league is private

# IMPORT THE LEAGUE DATA AND CLEANSE
league = League(league_id, year, espn_s2, swid)
df_columns = list(league.teams[0].__dict__.keys())  # get a list of columns for our dataframe
df_columns.remove('roster')  # remove roster from list of columns

# Convert to a dataframe
league_2021 = pd.DataFrame(data=np.zeros(0))
for d in range(len(league.teams)):
    team_df = pd.DataFrame(league.teams[d].__dict__, columns=df_columns)
    league_2021 = league_2021.append(team_df)

# Drop unnecessary columns
league_2021.drop(columns=[0, 'final_standing', 'logo_url', 'outcomes', 'streak_length', 'streak_type',
                          'team_abbrev', 'mov', 'team_id', 'owner'
                          ], axis=1, inplace=True)

# Rename some columns
league_2021.rename(columns={'division_id': 'division', 'scores': 'points', 'schedule': 'opponent',
                            'points_against': 'points_against_tot', 'points_for': 'points_for_tot'
                            }, inplace=True)

# Add week to dataframe
league_2021.index.names = ['week']  # add 'week' column
league_2021.reset_index(level='week', inplace=True)  # add +1 to every week
league_2021['week'] = league_2021['week'].apply(lambda x: x + 1)

# Set week as index
league_2021 = league_2021.set_index(league_2021.week)
league_2021.drop('week', axis=1, inplace=True)

# Re-order columns to be more readable
new_cols = ['division', 'team_name', 'wins', 'losses', 'opponent', 'points', 'points_for_tot', 'points_against_tot',
            'standing']
league_2021 = league_2021.reindex(columns=new_cols)

# Convert opponent column to string data type
league_2021['opponent'] = league_2021['opponent'].astype('string')

# Remove "Team" and "()" from opponent names
league_2021.opponent = league_2021.opponent.str[5:]  # strips characters from beginning of opponent name
league_2021.opponent = league_2021.opponent.str.rstrip(')')  # strips characters from end of opponent name

# View the dataframe
st.dataframe(data=league_2021)  # , width=None, height=None)
