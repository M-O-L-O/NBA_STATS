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

import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk

import bs4
from bs4 import BeautifulSoup

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

np.set_printoptions(threshold=sys.maxsize, suppress=True)

class NBAStats(Dataset):
    def __init__(self):
        self.stats
        self.columns

    def playerTrack(player, stat1=None, stat2=None, stat3=None, stat4=None, stat5=None, stat6=None):
        pass

    def scatterStats(index_1, index_2):
        pass

############## Put everything into  a class

# Download latest version of NBA database

path = kagglehub.dataset_download("eduardopalmieri/nba-player-stats-season-2425")
path = 'https://www.kaggle.com/datasets/eduardopalmieri/nba-player-stats-season-2425'

od.download(path, force=True)

data = pd.read_csv("nba-player-stats-season-2425\database_24_25.csv")

print("Read csv")

# Separate out the data headers into stats and non-stats
p, t, o, w, nba_stat_names, d =  np.split(data.columns,[1,2,3,4,24])
players = np.unique(data[p].to_numpy())

# Create raw data of only stats
raw_data = data.values[:,4:24]

#print(raw_data)
#print(data[nba_stat_names].values)

# Get size of the raw data
entries, columns = raw_data.shape

# Initialise player stats
stats = []

# Initialise nicknames
nicknames = pd.DataFrame(columns = ['Name', 'Team', 'Nickname 1', 'Nickname 2', 'Nickname 3', 'Nickname 4', 'Nickname 5', 'Nickname 6', 'Nickname 7', 'Nickname 8', 'Nickname 9', 'Nickname 10'])

nicknames['Name'] = players

# Save players to csv
#pd.DataFrame(players).to_csv('player_names.csv', index=False)

# Create average stats for each player from raw data

for player in players:
    
    suffix_status = False

    indices = np.repeat(data[p].to_numpy() == player, columns, axis=1)
    
    # get the shape for the data reshape
    index = int(np.mean(sum(indices))) 
    
    stats.append(np.mean(raw_data[indices].reshape((index, columns)), axis=0))
    
    # get nicknames from Basketball Reference - change to save to database instead
    player_lower = player.lower()
    
    cryl_char = [('[àáâãäå]+', 'a'), ('š', 's'), ('đ', 'd'), ('[çčć]+', 'c'), ('[èéêë]+', 'e'), ('[ìíîï]+', 'i'), ('[ðñòóôõö]+', 'o'), ('[ùúûü]+', 'u'), ('[ýÿ]+', 'y'),('ž', 'z')]
    
    for char, new_char in cryl_char:
        if re.search(char, player_lower):
            player_lower = re.sub(char, new_char, player_lower)

    #print(player_lower)
    
    try:
        forename, surname = re.sub('[^a-z- ]+', '', player_lower).split()
    except:
        suffix_status = True
        forename, surname, suffix = re.sub('[^a-z- ]+', '', player_lower).split()
    
        
    # For jnrs and seconds
    
    if forename == 'bronny':
        suffix_status = True

    # Get URL by using search on Basketball Reference instead!
    
    url_cheat = 'https://www.basketball-reference.com/search/search.fcgi?hint=&search={}+{}&pid=&idx='.format(forename, surname)
    
    nickname_str = [None] 
    
    r = requests.get(url_cheat)
    soup = BeautifulSoup(r.content, 'html.parser')
    
    try:
        div_cheat = soup.find('div', {"class":"note"})
        if div_cheat == None:
            raise Exception("None error - check div")
        _, nick_raw_string = div_cheat.get_text().split(': ')
        nickname_str = re.sub('[^A-za-z0-9ÀÁÂÃÄÅÆŠÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåšđçčćèéêëìíîïðñòóôõöùúûüýÿž~@#$^*()_+=[\]{}|\\,.?: -]+', '', nick_raw_string).split(', ')           
    except:
        pass
    else:
        div_search = soup.find('div', {"class":"search-item"})
        
        try:
            div_cheat = div_search.find_all('div', {"class":"note"})
        except:
            pass 
           
        if div_cheat != None:
            _, nick_raw_string = div_cheat.get_text().split(': ')
            nickname_str = re.sub('[^A-za-z0-9ÀÁÂÃÄÅÆŠÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåšđçčćèéêëìíîïðñòóôõöùúûüýÿž~@#$^*()_+=[\]{}|\\,.?: -]+', '', nick_raw_string).split(', ')   

        if div_search == None:
            raise Exception("None error - check div")

    # if suffix_status:    
    #     url = 'https://www.basketball-reference.com/players/{}/{}.html'.format(surname[0], surname[:5] + forename[:2] + '02')
    # else:
    #     url = 'https://www.basketball-reference.com/players/{}/{}.html'.format(surname[0], surname[:5] + forename[:2] + '01')
    
    # # For broken links
    # if player == 'Clint Capela':
    #     url = 'https://www.basketball-reference.com/players/{}/{}.html'.format(surname[0], surname[:5] + 'ca' + '01')
    # elif player == 'Armel Traoré':
    #     url = 'https://www.basketball-reference.com/players/{}/{}.html'.format(forename[0], forename[:5] + surname[:2] + '01')
 

    
    # try:
    #     #div_meta_check = soup.find('div', id='wrap').find('div', id='info').find('div', id='meta')
    #     div_meta = soup.find('div', id='meta')
    #     try:
    #         div_inner = div_meta.find_all('div')
    #         try:
    #             div = div_meta[1]
    #             print("CASE 1")
    #         except:
    #             div = div_meta
    #             print("Case 2")
                
    #         try:
    #             div_ps = div.find_all('p')
    #         except:
    #             ("Direct approach - div method failed")
    #             divs = soup.find('div', id='meta').find_all('p')    

    #         for i, para in enumerate(div_ps):
    #             #print(i,': ',[para])
    #             #print(i,': ',str(para))
                
    #             if '(' in str(para) and re.sub('[^A-za-z,() ]+', '', para.text)[0] == '(' and 'Full name' not in str(para):
    #                 #print(para.text)
    #                 nickname_str = [re.sub('[^A-za-z0-9ÀÁÂÃÄÅÆŠÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåšđçčćèéêëìíîïðñòóôõöùúûüýÿž, ]+', '', para.text).split(', ')]
    #                 break
            
    #         #soup.body.div(id="wrap").div(id="info").div(id="meta").div.p(third)
    #     except:
    #         raise Exception("Divs in div_meta not found")
    # except:
    #     div_fail = soup.find_all('div')
    #     raise Exception("No div meta found")
    
    div_team = soup.find('div', {"class":"search-item-team"})
    _, team_str = div_team.get_text().split(': ')
    print(team_str)

    nicknames.loc[nicknames.Name == player, 'Team'] = re.sub('[^A-za-z0-9ÀÁÂÃÄÅÆŠÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåšđçčćèéêëìíîïðñòóôõöùúûüýÿž~@#$^*()_+=[\]{}|\\,.?: -]+', '', team_str)   

    if nickname_str[0] != None:
        print(player + " nicknames are: ")
        for n, nickname in enumerate(nickname_str):
            print(nickname)    
    else:
        print(player + " has no nicknames")
    
    
    print("\n")
#print(pd.DataFrame(nba_stat_names))

# Save nicknames

nicknames.to_csv('nicknames_doc.csv')

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

def lemmaPlayers():
    # using player names, generates word bank for probabilistic comparison
    # Do I add nicknames manually or do I leave it as the four rules (see notes)
    pass

player_name_bank = lemmaPlayers()

def nameComp(name):
    # take a name input and ignore spelling errors and differences in format to get the right player
    
    # Can i add nicknames? draw from nba reference?
    
    # Turn name into an array of all name components
    name_plain = re.sub('[^A-za-z ]+', '', name.lower()).split() 
    
    print(name_plain)
    
    # Create adjacent word bank/lemmatization for each player name? - call func.
    
    # Check if more than one word is in the name inputted, and if there's any punctuation
    if len(name_plain) == 1:
        # one name case - check against surnames first
        
        # check against forenames
        
        # return highest prob
        pass
    elif len(name_plain) == 2:
        # two name case - calc probs for each word
        
        # return highest match
        pass
    else:
        if name_plain[2] == 'jnr' or np.unique(name_plain[2]) == 'i':
            # use first two words
            pass
        else:
            # error - no name with three names
            pass
            
         
if __name__ == '__main__':
    #screen = GraphWindow()
    
    #screen.mainloop()
    # Input a players name and run playerTrack
    
    for player in players:
        forename, surname = player.split()
        
        url = 'https://www.basketball-reference.com/players/g/{}.html'.format(surname[:5] + forename[:2])
        
        with open(url) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        soup.findAll('div,attrs={"id":"meta"}')
        soup.body.div(id="wrap").div(id="info").div(id="meta").div.p(third)
        nickname_str = BeautifulSoup("p", 'html.parser')
    
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





