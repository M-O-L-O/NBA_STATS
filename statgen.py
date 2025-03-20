import sys
import torch
import tensorflow
import re
import requests
import regex
import time

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

np.set_printoptions(threshold=sys.maxsize)

### Generates the stats and info from Kaggle - can return various stat/info categories

### Just raw info dumping don't include the functions yet

### Q) Separate all stats from each player? Or all together? 
### A) Keep together - have whole stat object and draw what is necessary from there

### Stats and info list:
###  - Each player profile - stats, other info
###  - Each stat category for all players
###  - Each team profile
###  - 

###  Stat names will never change so keep as a constant?

class NBAStats(Dataset):
    
    column_headers = ['Player', 'Tm', 'Opp', 'Res', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'GmSc', 'Data']
    
    def __init__(self):
        ### Initialise variables
        
        self.data = self.__getdata__()
        self.players = np.unique(self.data['Player'].to_numpy())
        self.teams = np.unique(self.data['Tm'].to_numpy())
        self.raw_data = self.data.values[:,4:24]
        self.stats = []
        self.nicknames = pd.DataFrame(columns = ['Name', 'Team', 'Nickname 1', 'Nickname 2', 'Nickname 3', 'Nickname 4', 'Nickname 5', 'Nickname 6', 'Nickname 7', 'Nickname 8', 'Nickname 9', 'Nickname 10'])
        self.data_x, self.data_y = self.raw_data.shape
    
    def __getdata__(self):
        ### Get data from KaggleHub
        path = kagglehub.dataset_download("eduardopalmieri/nba-player-stats-season-2425")
        path = 'https://www.kaggle.com/datasets/eduardopalmieri/nba-player-stats-season-2425'
        od.download(path, force=True)
        return pd.read_csv("nba-player-stats-season-2425\database_24_25.csv")

    def pullAllNames(self):
        
        letters = list(map(chr, range(97, 123)))
                
        for letter in letters:
            # Get list of every player from Basketball Reference
            url_all_players = 'https://www.basketball-reference.com/players/{}'.format(letter)
            
            r = requests.get(url_all_players)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            csv_text_letter = soup.find('pre', {"id":"csv_players"}).get_text().split("<!--ALREADYCSV -->")[1]
            
            file_name = "players_{}.csv".format(letter)
            
            with open(file_name, "w") as text_file:
                text_file.write(csv_text_letter)
                
    def playerLoop(self):
        
        ### Loops through all players and generates the necessary information for each         
        
        for player in self.players:
            
            self.statGen(player)
            
            self.nicknameGen(player)

    def statGen(self, player):
        ### STATS 
        # Generate the index for each stat 
        indices = np.repeat(self.data['Player'].to_numpy() == player, self.data_y, axis=1)
        index = int(np.mean(sum(indices))) 
        
        # Appends the average stats for this player
        self.stats.append(np.mean(self.raw_data[indices].reshape((index, self.data_y)), axis=0))

    def nicknameGen(self, player):
        ### NICKNAMES
        # Get nicknames from Basketball Reference - change to save to database instead
        player_lower = player.lower()
        
        cryl_char = [('[àáâãäå]+', 'a'), ('š', 's'), ('đ', 'd'), ('[çčć]+', 'c'), ('[èéêë]+', 'e'), ('[ìíîï]+', 'i'), ('[ðñòóôõö]+', 'o'), ('[ùúûü]+', 'u'), ('[ýÿ]+', 'y'),('ž', 'z')]
        
        for char, new_char in cryl_char:
            if re.search(char, player_lower):
                player_lower = re.sub(char, new_char, player_lower)
        
        try:
            forename, surname = re.sub('[^a-z- ]+', '', player_lower).split()
        except:
            suffix_status = True
            forename, surname, suffix = re.sub('[^a-z- ]+', '', player_lower).split()

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
        
        div_team = soup.find('div', {"class":"search-item-team"})
        _, team_str = div_team.get_text().split(': ')
        print(team_str)

        self.nicknames.loc[self.nicknames.Name == player, 'Team'] = re.sub('[^A-za-z0-9ÀÁÂÃÄÅÆŠÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖÙÚÛÜÝàáâãäåšđçčćèéêëìíîïðñòóôõöùúûüýÿž~@#$^*()_+=[\]{}|\\,.?: -]+', '', team_str)   
        
        """ 
        if nickname_str[0] != None:
            print(player + " nicknames are: ")
            for n, nickname in enumerate(nickname_str):
                print(nickname)    
        else:
            print(player + " has no nicknames") 
        """
    
    def player(self, player_name):
        # Create Player object?
        if player_name in self.players:
            return Player(player_name)

    def category(self, stat_name):
        # Create Category object?
        if stat_name in self.column_headers:
            return Category(stat_name)

    def team(self, team_name):
        # Create Team object?
        if team_name in self.teams:
            return Team(team_name)

class RetiredPlayers(Dataset):
    
    def __init__(self):
        self.player_stats = pd.read_csv('player_each_year_all.csv')
        self.player_name_data = pd.read_excel("data/allnbaplayer_final.xlsx")
        #self.player_stats = self.pullAllData("data/allnbaplayer_final.xlsx", "everyplayerstats.csv")
        
    def pullAllData(self, path_out="data/allPlayersStats_new.csv", path_in="data/allnbaplayer_final.xlsx"):        
        data = pd.read_excel(path_in)
        players = np.array([data["Player-additional"], data["Player"]]).T

        last_player = 0

        headers = ['Season', 'Age', 'Team', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Awards']

        player_stats = pd.DataFrame()

        try:
            already_scanned = pd.read_csv(path_out)

            last_player = np.max(list(np.where(players == already_scanned['Name'].values[-1])))

            player_stats = pd.concat([player_stats, already_scanned])
        except:
            pass

        for url_part, player in players[last_player + 1:]:
            
            # Get list of every player from Basketball Reference
            url_all_players = 'https://www.basketball-reference.com/players/{}/{}.html'.format(url_part[0], url_part)
            
            r = requests.get(url_all_players)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            per_game_table = pd.read_html(str(soup.find('table', {"id":"per_game_stats"})))[0]
            print(per_game_table.columns)
            print(per_game_table)
            print(player)
            per_game_stats = per_game_table.loc[per_game_table['Pos'].notnull()]
            
            per_game_stats = per_game_stats[pd.to_numeric(per_game_stats['Age'], errors='coerce').notnull()]
            
            szn_unq = per_game_stats['Season'].values
            season_comp = list(np.unique(szn_unq.astype(str)))
            print(season_comp)
            year_list = [season_comp.index(season) + 1 for season in per_game_stats['Season'].values]
            
            
            per_game_stats.insert(0, 'Year', year_list)
            per_game_stats.insert(0, 'Name', str(player))
            
            print(player)
            player_stats = pd.concat([player_stats, per_game_stats])
            player_stats.to_csv(path_out)
            
            time.sleep(3.5)
        
        print(player_stats[player_stats['Age'].map(len) != 2])
        player_stats.drop(player_stats[player_stats['Age'].map(len) != 2]).to_csv('player_each_year_all.csv')
        
        return player_stats
    
    def playerCareer(self, player_name):
        return self.player_stats.loc[self.player_stats['Name'] == player_name]

    def plotCareerStats(self, player_name, stat1, stat2 = 'Year', stat3 = None):
        player_stats = self.playerCareer(player_name)
    
        # Stat 1 is a stat category
        
        # Stat 2 is always year or season or age
        
        if stat2 == 'Year' or 'Season' or 'Age':
                
            fig = plt.figure()
            
            x = player_stats[stat1].values
            y = player_stats[stat2].values
            
            if stat2 == 'Season':
                y = [int(a[:4]) for a in y]
                
            if stat3:
                ax = plt.axes(projection ='3d')
                
                # defining all 3 axis
                
                z = player_stats[stat3].values
                print(x,y,z)
                ax.plot3D(x, y, z, 'blue')
                ax.scatter(x, y, z, color ='green')
                ax.set_title('Plot of {} and {} against {}'.format(stat1, stat3, stat2))
                plt.show()
            else:
                fig.plot(x,y)
                plt.show()
            
    def pullGameByGameStats(self, player_name):        
        # Get player's Basketball Reference ID
        player_data = self.player_stats.loc[self.player_stats['Name'] == player_name]
        url_part = self.player_name_data.loc[self.player_name_data['Player'] == player_name]["Player-additional"].values[0]
        
        game_by_game_stats = pd.DataFrame()
        
        print(url_part)
        
        seasons = [int(p[:4]) + 1 for p in np.unique(player_data['Season'].to_numpy())]
        
        for season in seasons:
            url_season = 'https://www.basketball-reference.com/players/{}/{}/gamelog/{}'.format(url_part[0], url_part, season)
            
            r = requests.get(url_season)
            soup = BeautifulSoup(r.content, 'html.parser')
            
            per_game_table = pd.read_html(str(soup.find('table', {"id":"pgl_basic"})))[0]
            print(per_game_table.columns)
            per_game_stats = per_game_table.loc[per_game_table['GS'].notnull()]
            
            per_game_stats['Name'] = str(player_name)
            try:
                per_game_stats['Tot_Games'] = range(np.maximum(game_by_game_stats['Tot_Games'].to_numpy) + 1, np.maximum(game_by_game_stats['Tot_Games'].to_numpy) + len(per_game_stats) + 1)
            except:
                per_game_stats['Tot_Games'] = range(1, len(per_game_stats) + 1) 
                        
            game_by_game_stats = pd.concat([game_by_game_stats, per_game_stats])
            formatted_player_name = re.sub(' +', '_', player_name).lower()
            game_by_game_stats = game_by_game_stats.loc[game_by_game_stats['Unnamed: 7'].notnull()]
            game_by_game_stats.to_csv("data/playbyplay/{}_game_by_game_stats.csv".format(formatted_player_name))
            
            
            time.sleep(3.5)
    
    def plotGameByGame(self):
        pass
    
    def gameByGameBreakdown(self):
        pass

retirees = RetiredPlayers()

retirees.pullAllData("allPlayerStatsNew.csv")

retirees.pullGameByGameStats('LeBron James')

retirees.plotCareerStats('LeBron James','3P%', 'Season', 'AST') 
    
class Player():
    def __init__(self, ):
        pass

class Category():
    def __init__(self):
        pass

class Team():
    def __init__(self):
        pass
    
    