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

# Standard Deviation ignoring NaN values
def nanstd(o, dim, keepdim=False):
    result = torch.sqrt(
                torch.nanmean(
                    torch.pow( torch.abs(o-torch.nanmean(o,dim=dim).unsqueeze(dim)),2),
                    dim=dim
                )
            )
    
    if keepdim:
        result = result.unsqueeze(dim)
        
    return result

# Get each players stats - historical data from somewhere (unchanging so save locally)
data = pd.read_csv('data/allPlayerStatsNew.csv')

headers = ['PTS','MP','AST','STL','BLK','TRB','TOV','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','FT','FTA','FT%','eFG%','ORB','DRB','PF',]

len_tensor = len(headers)

def dataFormat(raw_data, player_name, headers = ['PTS','MP','AST','STL','BLK','TRB','TOV','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','FT','FTA','FT%','eFG%','ORB','DRB','PF',]
    ):
    
    # Inputs Dataframe and outputs a tensor with data on player X formatted how we want (years combined and useless stuff stripped)
    # Normalise first??
    
    player_data = raw_data.loc[raw_data['Name'] == player_name]
    
    years_played = np.unique(player_data['Year'])
    
    formatted_data = []
    
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
            multipl = torch.matmul(torch.transpose(raw_player_year_x, 0, 1), games_proportion.t())
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
    
    # After got all data correct, normalise
    X_out = []
    #    Return normalised distance using Z score (SHOULD THIS BE A PRECURSORY STEP BEFORE CALCULATING DISTANCE??? - NORMALISE STATS THEN CALCULATE DISTANCE??)
    #    RIGHT NOW IT'LL NORMALISE THE DISTANCE BETWEEN EACH STAT

    for x in X: 
        columns = torch.transpose(torch.cat(x),0,1)
        # - you want to get rid of column index 0 as it is year, which shouldn't be normalised
        # should the games played be normalised? yes as it doesnt make a big diff
        # set mean to 0 and standard deviations to 1?
        means = torch.tensor([torch.nanmean(column, 0).item() for column in columns])
        stds = torch.tensor([nanstd(column, 0).item() for column in columns])
        means[0] = torch.zeros(len(means[0]))
        stds[0] = torch.ones(len(stds[0]))
        
        
        for datum in x:
            X_out.append(torch.div( (datum - means.repeat(len(datum), 1) ), stds.repeat(len(datum), 1) ))
    
    return X_out

# Just realised name not needed - can exclude

X = allDataFormat(data)

#print(torch.cat(X).size())

### DBSCAN Algorithm

# Stages

# 1) Compute line of career against other line: point-by-point comparison - for differing lengths,  

# 2) Compute core distance

#    Make distance function
def dist(player1=torch.Tensor, player2=torch.Tensor):
    # find which has highest years
    
    # Using matrices of player data - pull column of years and use to replace len -- len works as one by one years
    year1, year2 = len(player1), len(player2)
    
    min_it = int(np.min([year1,year2]))
    
    
    # Here calculate dist between same shape parts then append the mean to fill the end
    
    if year1 < year2:
        # Player 1 less years
        dist_half = torch.abs(torch.subtract(player1,player2[:min_it]))
        dist_vec = torch.cat( (dist_half, (1.5 * torch.nanmean(dist_half, 0)).repeat(year2 - year1,1)) )
    elif year1 > year2:
        # Player 2 less years
        dist_half = torch.abs(torch.subtract(player2,player1[:min_it]))
        dist_vec = torch.cat( (dist_half, (1.5 * torch.nanmean(dist_half, 0)).repeat(year1 - year2,1)) )
    else:
        dist_vec = torch.abs(torch.subtract(player1,player2))
        
    return dist_vec

print(dist(X))

def DBSCAN():
    
    pass

def RangeQuery():
    pass


# 3) Use core distance to determine which to group together

# Test different versions: 
# - career averages with length as stat
# - have career year as axis (best) - DBSCAN
# - seperate to make multiple models by each  and then compare overlap between models 
# Weightings by pace of each era?


# Do groupings by career progression


# For each cluster, match the timelines of the players



##### ARCHIVE

#    Determine ranges for normalisation
def determineAverages(form_data):
    columns = torch.transpose(torch.cat(form_data),0,1)
    #return [int(torch.max(column)) for column in columns]
    returns = [(torch.nanmean(column, 0).item(), nanstd(column, 0).item()) for column in columns]
    return returns, len(returns)
