import sys
import torch
import tensorflow

import numpy as np
import pandas as pd
import opendatasets as od
import matplotlib.pyplot as plt

import kaggle
import kagglehub
from datetime import datetime
import matplotlib.dates as mdates

import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

np.set_printoptions(threshold=sys.maxsize)

class NBAStats(Dataset):
    def __init__(self):
        self.stats
        self.columns

    def playerTrack(player, stat1=None, stat2=None, stat3=None, stat4=None, stat5=None, stat6=None):
        pass

    def scatterStats(index_1, index_2):
        pass

# Download latest version of NBA database

path = kagglehub.dataset_download("eduardopalmieri/nba-player-stats-season-2425")
#path = 'https://www.kaggle.com/api/v1/datasets/download/eduardopalmieri/nba-player-stats-season-2425'
path = 'https://www.kaggle.com/datasets/eduardopalmieri/nba-player-stats-season-2425'
#print("Path done", path)

od.download(path, force=True)

data = pd.read_csv("nba-player-stats-season-2425\database_24_25.csv")
#data = pd.read_csv(path)

print("Read csv")

# Seperate out the data headers into stats and non-stats
p, t, o, w, nba_stat_names, d =  np.split(data.columns,[1,2,3,4,24])
players = np.unique(data[p].to_numpy())

# Create raw data of only stats
raw_data = data.values[:,4:24]

# Get size of the raw data
entries, columns = raw_data.shape

# Initialise player stats
stats = []

# Create average stats for each player from raw data
for player in players:
    indices = np.repeat(data[p].to_numpy() == player, columns, axis=1)
    
    # get the shape for the data reshape
    index = int(np.mean(sum(indices))) 
    
    stats.append(np.mean(raw_data[indices].reshape((index, columns)), axis=0))
    

#print(pd.DataFrame(nba_stat_names))

# stats = data[nba_stat_names].to_numpy()
stats = np.array(stats)

def scatterStats(index_1, index_2):

    plt.scatter(stats[:,index_1], stats[:,index_2])

    plt.title("Plot of {} against {}".format(nba_stat_names[index_1], nba_stat_names[index_2]))
    plt.xlabel(nba_stat_names[index_1])
    plt.ylabel(nba_stat_names[index_2])

    for i, txt in enumerate(players):
        names = np.array((txt.replace('-',' ').split(' ')))
        initials = ""
        
        for name in names:
            splitname = list(name)
            
            try:
                initials += splitname[0]
            except:
                pass
            
            
        plt.annotate(initials, (stats[i,index_1], stats[i,index_2]))

    plt.show()
    
    return True

def playerTrack(player, stat1=None, stat2=None, stat3=None, stat4=None, stat5=None, stat6=None):
    if player in players:
        indices = np.repeat(data[p].to_numpy() == player, columns + 1, axis=1)
        
        full_player_data = data.values[:,4:]
        
        # get the shape for the data reshape
        index = int(np.mean(sum(indices))) 
        
        player_data = np.array(full_player_data[indices].reshape((index, columns + 1))).T
        
        player_stats = player_data[:-1]
        player_dates = [datetime.strptime(i, '%Y-%m-%d') for i in player_data[-1]]
        
        fig, ax = plt.subplots(4,5)

        for i, stat in enumerate(player_stats):
            
            ax[i//5, i % 5].plot(player_dates, stat)
            ax[i//5, i % 5].set_ylabel(nba_stat_names[i])
            ax[i//5, i % 5].set_title("{} of {}".format(nba_stat_names[i], player))
            ax[i//5, i % 5].xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
            
            # Rotates and right-aligns the x labels so they don't crowd each other.
            for label in ax[i//5, i % 5].get_xticklabels(which='major'):
                label.set(rotation=30, horizontalalignment='right')   
        
        plt.subplots_adjust(wspace=0.3, hspace=0.75)
        
        plt.show()   
        return True
    else:
        return False
     

if __name__ == '__main__':
    screen = GraphWindow()
    
    screen.mainloop()
    # Input a players name and run playerTrack
    while True:
        playerTrackRun = False

        scatterStatsRun = False
        
        while not scatterStatsRun:
            
            numbers = input("""Input the two numbers for the stat 
categories separated by a space. 
The stat categories are:
    0    Minutes Played        1    Field Goals Made  2    Field Goals Attempted    3    Field Goal %
    4    3 Points Made         5    3 Point Attempts  6    3 Point %                7    Free Throws Made
    8    Free Throw Attempted  9    Free Throw %      10   Offensive Rebounds       11   Defensive Rebounds   
    12   Total Rebounds        13   Assists           14   Steals                   15   Blocks 
    16   Turnovers             17   Personal Fouls    18   Points                   19   Game Score 
        
        """).split()
            
            print(numbers)
            a, b = numbers[0], numbers[1]
            try:
                scatterStatsRun = scatterStats(int(a), int(b))
            except:
                pass
            
        while not playerTrackRun:
            player_name = input("Enter a player's name: ")
        
            playerTrackRun = playerTrack(player_name)
    
    




#nba_stats = torch.Tensor(data)





