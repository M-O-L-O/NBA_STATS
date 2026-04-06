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


data = pd.read_excel("data/allnbaplayer_final.xlsx")
players = np.array([data["Player-additional"], data["Player"]]).T

last_player = 0

headers = ['Season', 'Age', 'Team', 'Lg', 'Pos', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Awards']

player_stats = pd.DataFrame()

try:
    already_scanned = pd.read_csv("allPlayerStats.csv")

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
    per_game_stats = per_game_table.loc[per_game_table['Season'].notnull()]
    
    per_game_stats['Year'] = range(1, len(per_game_stats) + 1)
    per_game_stats['Name'] = str(player)
    
    print(player)
    player_stats = pd.concat([player_stats, per_game_stats])
    player_stats.to_csv("allPlayerStats-all.csv")
    
    time.sleep(3.5)

