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
torch.set_printoptions(threshold=10000, linewidth=140, precision=2, edgeitems=8)

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

    columns = torch.transpose(torch.cat(X),0,1)
    # - you want to get rid of column index 0 as it is year, which shouldn't be normalised
    # should the games played be normalised? yes as it doesnt make a big diff
    # set mean to 0 and standard deviations to 1?
    
    means = torch.tensor([torch.nanmean(column, 0).item() for column in columns])
    stds = torch.tensor([nanstd(column, 0).item() for column in columns])
    means[0] = 0
    stds[0] = 1
    
    print(means, stds)
    
    for x in X: 
        X_out.append(torch.div( torch.abs( x - means.repeat(len(x), 1) ), stds.repeat(len(x), 1) ))
    
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
    # NOW THAT DISTANCE IS NORMALISED, SHOULD EMPTY YEARS BE 1+ STANDARD DEVIATIONS??
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
    
    # Should be returning scalar?? determining total distance from each? 
    # Create average per year distance?
    
    return  torch.nanmean(dist_vec, 0)

print(X[50].size(), X[5].size())
print(dist(X[50], X[5]))

print(X[67].size(), X[420].size())
print(dist(X[67], X[420]))

def dist_all(input):
    ### WAY TOO SLOW - REMAKE MATRIX TO DO ALL AT ONCE?
    ### -- Doesn't work as the dist function works one on one - adapt to make it work for all?
    ### Find way to expand matrices in mass
    ### STACK EM VERT AND REPEAT WITH ROTATED STACKS - STACK VERTICALLY AND SUBTRACT? THEN DO CALCULATION?
    
    ### NEED TO ADD DIST FUNCTION
    
    dist_mat = torch.zeros((len(input) - 1, len(input) - 1))
    dist_sub = torch.zeros((len(input) - 1, len(input) - 1))
    
    for k in range(len(dist_mat)):
        # Truncate so shapes match
        # mean * (3n + k) / 2
        
        pre_row_mat = input[:-(k+1)]
        pre_row_sub = input[(k+1):]
        
        dim_set = 0
        
        dim_row = np.minimum([d.size(dim_set) for d in pre_row_mat], [d.size(dim_set) for d in pre_row_sub])
        
        dist_mat[k,:-k] = [k.narrow(dim_set, 0, j) for j,k in zip(dim_row, pre_row_mat)]   
        dist_sub[k,:-k] = [k.narrow(dim_set, 0, j) for j,k in zip(dim_row, pre_row_sub)]
        
        # Add the mirror.
        dist_mat[k:,-(k + 1)] = torch.fliplr(input[:-(k+1)])
        dist_sub[k:,-(k + 1)] = torch.fliplr(input[:-(k+1)]) 
    
    dist_mat -= dist_sub
    
    dist_out = torch.zeros(input.size())

    mask_new = torch.zeros((8,8))
    
    for k, row in enumerate(dist_mat):
        mask_new[k:] = row[:-k]
        mask_new[:k] = torch.fliplr(row[-k:])
        
    mask_up = torch.zeros((9,9))
    mask_down = torch.zeros((9,9))
    
    mask_up[:-1, :-1] = torch.triu(mask_new)
    mask_down[1:, 1:] = torch.tril(mask_new)

    dist_out = mask_up + mask_down
    
    # for i in range(len(input)):
    #     player1 = input[i]
    #     for j in range(i):
    #         if i == j:
    #             pass
    #         else:
    #             player2 = input[j]
    #             dist_mat[i,j] = dist_mat[j,i] = torch.nanmean(dist(player1,player2)).item() 
                
    return dist_out
            
dist_matrix = dist_all(X)
d_m_np = dist_matrix.numpy() #convert to Numpy array
dmf = pd.DataFrame(d_m_np) #convert to a dataframe
dmf.to_csv("distance_matrix",index=False)
print(dist_matrix) 

# Determine whether distance is within the neighbourhood (set epsilon value - 0.5 or 1 standard deviation? - adjust depending on what outputs)
def RangeQuery(dist_store, index, mpts = 10, eps = 26 * 0.75):
    # Creates tuples of the distances of all with 
    all_dists = sorted(enumerate(dist_store[index]), key=lambda i: i[1])
    
    # 
    if torch.sum(all_dists[0,:mpts]).item() < eps:
        return [all_dists[index] for index in all_dists[1,:mpts]]
    else:
        return []

# Uses DBSCAN algorithm - will assign labels to all points or assign them as noise - needs epsilon and mpts input
def DBSCAN(X,mpts,eps=0.65):
    # Determine core objects for each object (neighbourhod has at least mpts)
    # If not core object, noise
    # Cluster where every point is core object and within each others neighbourhoods
    pass

# Uses HDBSCAN algorithm - will create MST and determine (?) epsilon value from there - needs mpts input
def HDBSCAN(X,mpts):
    # Compute core distance (distance of point x from mpts'th nearest point)
    # Retrospectively set epsilon using core distance (epsilon > core distance)
    # Mutual Reachability Distance (MRD): maximum of respective core distances and distance between the points
    # Compute minimum spanning tree using MRD - all points either core distance or distance exceeds that
    # Expand MST to get MST_ext by adding self-edge with core distance as weight (I think it will then eliminate all connections that exceed the core distances)
    # Remove in decreasing order and add labels
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
