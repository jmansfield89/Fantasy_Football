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
league = League(league_id, year, espn_s2, swid)
