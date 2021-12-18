## LIBRARY IMPORTS
# Import data visualization modules
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import data manipulation modules
import numpy as np
import pandas as pd

# Import ESPN Fantasy Football API
from ff_espn_api import League


## SET VARIABLES FOR DATA IMPORT SPECIFIC TO YOUR LEAGUE
# league_id can be found in the URL once you login to your ESPN fantasy football league, e.g. https://fantasy.espn.com/football/team?leagueId=XXXXXX&teamId=3&seasonId=2021
league_id = XXX #replace the X's with your league id 
year = 2021 #set the year you want to scrape data from

# While logged into your league, you can get your swid and s2 values through the Settings -> More tools -> Web Developer Tools
swid = '{XXX}' #your swid
espn_s2 = 'XXX' #your espn_s2


## EXTRACT DATA FROM THE WEBSITE
# Create object for extracted data
league = League(league_id, year, espn_s2, swid)

# Convert extracted data into a dataframe
league_2021 = pd.DataFrame(data = np.zeros(0))      # create dataframe of all zeros
df_columns = list(league.teams[0].__dict__.keys())  # get a list of columns for our dataframe   
df_columns.remove('roster')                         # remove 'roster' from list of columns
for d in range(len(league.teams)):                  # fill dataframe with extracted data
    team_df = pd.DataFrame(league.teams[d].__dict__, columns=df_columns)
    league_2021 = league_2021.append(team_df)
 

## CLEAN THE DATA
# Drop unnecessary columns
league_2021.drop(columns=[0, 'final_standing', 'logo_url', 'outcomes', 'streak_length', 'streak_type', 
                          'team_abbrev', 'mov', 'team_id'
                         ], axis=1, inplace=True)

# Rename some columns
league_2021.rename(columns={'division_id': 'division', 'scores': 'points', 'schedule': 'opponent', 
                            'points_against': 'points_against_tot', 'points_for': 'points_for_tot'
                           }, inplace=True)

# Add week to dataframe
league_2021.index.names = ['week']# add 'week' column
league_2021.reset_index(level='week', inplace=True)# add +1 to every week
league_2021['week'] = league_2021['week'].apply(lambda x: x + 1)

# Set week as index
league_2021 = league_2021.set_index(league_2021.week)
league_2021.drop('week', axis=1, inplace=True)

# Re-order columns to be more readable
new_cols = ['team_name', 'wins', 'losses', 'opponent', 'points', 'points_for_tot', 'points_against_tot', 'standing']
league_2021 = league_2021.reindex(columns=new_cols)

# Convert opponent column to string data type
league_2021['opponent'] = league_2021['opponent'].astype('string')

# Remove "Team" and "()" from opponent names
league_2021.opponent = league_2021.opponent.str[5:] #strips characters from beginning of opponent name
league_2021.opponent = league_2021.opponent.str.rstrip(')') #strips characters from end of opponent name


## VIEW THE DATA
league_2021
