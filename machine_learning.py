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

# TASK: Clustering to match for prediction

# Set PyTorch print settings
torch.set_printoptions(threshold=10000, linewidth=140, precision=2)

# Get each players stats - historical data from somewhere (unchanging so save locally)
data = pd.read_csv('data/allPlayerStatsNew.csv')


def dataFormat(raw_data, player_name):
    
    # Inputs Dataframe and outputs a tensor with data on player X formatted how we want (years combined and useless stuff stripped)

    player_data = raw_data.loc[raw_data['Name'] == player_name]
    
    years_played = np.unique(player_data['Year'])
    
    formatted_data = []
    
    headers = ['PTS','MP','AST','STL','BLK','TRB','TOV','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','FT','FTA','FT%','eFG%','ORB','DRB','PF',]
    
    for i, year in enumerate(years_played):
        interm = player_data.loc[player_data['Year'] == year][headers]
        raw_player_year_x = torch.from_numpy(interm.to_numpy(dtype=np.float32))   
        
        games_played, games_started = np.sum(player_data.loc[player_data['Year'] == year]['G'].values), np.sum(player_data.loc[player_data['Year'] == year]['GS'].values) 
        games_proportion = torch.tensor(player_data.loc[player_data['Year'] == year]['G'].to_numpy(dtype = np.float32) / int(float(games_played)))
        
        
        if len(games_proportion) == 1:
            multipl = raw_player_year_x[0]
            games_section = torch.tensor([float(year), float(games_played),float(games_started)])
        
        else:
            #print(raw_player_year_x.size(), games_proportion.size())
            multipl = torch.matmul(torch.transpose(raw_player_year_x, 0, 1), games_proportion.T)
            games_section = torch.tensor([float(year), float(games_played),float(games_started)])
        
        # Should all condense into one line
        # if want to include name, add in front of float games
        new_rows = torch.cat((games_section,multipl))
        
        formatted_data.append(new_rows)
        if new_rows.size() != torch.Size([26]):
            raise Exception("At year {}, problem occured".format(year))
    
    return torch.stack(formatted_data)     
        
# Convert it into a torch tensor - auto with dataFormat

def allDataFormat(raw_data):
    
    # Formats all data into suitable tensor
    player_names = np.unique(data['Name'])
    
    X = []
    for player in player_names:
        X.append(dataFormat(data, player))
    
    return X

# Just realised name not needed - can exclude

X = allDataFormat(data)

print(X[5])
print(X[50])
print(X[150])

### DBSCAN Algorithm

# Stages

# 1) Compute line of career against other line: point-by-point comparison - for differing lengths,  

# 2) Compute core distance

# Make distance function
def dist(player1=torch.Tensor, player2=torch.Tensor):
    # find which has highest years
    
    # Using matrices of player data - pull column of years and use to replace len
    year1, year2 = len(player1), len(player2)
    
    min_it = int(np.min([year1,year2]))
    
    # Here add rows instead of expand_as (unless expand_as adds a row)
    if year1 < year2:
        player1.expand_as(player2)
    elif year1 > year2:
        player2.expand_as(player2)
        
    # Subtract matrices from each other to get distances
    dist_vec = torch.abs(torch.subtract(player1,player2))
    
    # If the years dont match, fill gap rows with mean multipliers
    try:    
        dist_vec[:min_it] = torch.torch.mean(dist_vec[min_it:], 1) * 1.5
    except:
        pass
    
    
    
    # for every year, find the distance between each player in each stat category and record
    
    dist_vec = (player1 - player2)


# Test different versions: 
# - career averages with length as stat
# - have career year as axis (best) - DBSCAN
# - seperate to make multiple models by each  and then compare overlap between models 
# Weightings by pace of each era?


# Do groupings by career progression


# For each cluster, match the timelines of the players



