import sys
import torch
import tensorflow
import re
import requests
import regex

import numpy as np
import pandas as pd
import opendatasets as od
import matplotlib.pyplot as plt

import kaggle
import kagglehub
from datetime import datetime
import matplotlib.dates as mdates

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

# Set PyTorch print settings
torch.set_printoptions(threshold=10000, linewidth=140, precision=2)

# Clustering to match for prediction

#### Year column is all wrong - match year to season instead

# Get each players stats - historical data from somewhere (unchanging so save locally)
data = pd.read_csv('data/allPlayerStats.csv')

player_names = np.unique(data['Name'])

formatted_data  =[]

def dataFormat(raw_data, player_name):
    player_data = raw_data.loc[raw_data['Name'] == player_name]
    
    years_played = np.unique(player_data['Year'])
    
    headers = ['MP','FG','FGA','FG%','3P','3PA','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','Year','3P%']
    for i, year in enumerate(years_played):
        raw_player_year_x = torch.tensor(player_data.loc[player_data['Year'] == year][['MP','FG','FGA','FG%','3P','3PA','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','Year','3P%']].to_numpy(dtype=np.float32)[0])   
        
        games_played, games_started = np.sum(player_data.loc[player_data['Year'] == year]['G'].values), np.sum(player_data.loc[player_data['Year'] == year]['GS'].values) 
        games_proportion = torch.tensor(player_data.loc[player_data['Year'] == year]['G'].to_numpy(dtype = np.float32) / int(float(games_played)))
        
        new_rows = torch.cat((torch.tensor([float(games_played),float(games_started)]),torch.mul(raw_player_year_x, games_proportion.repeat(len(headers)))))
        
        formatted_data.append(new_rows)
    
    
    return torch.stack(formatted_data)
        
lebron = dataFormat(data, 'Danny Green')        
print(lebron)