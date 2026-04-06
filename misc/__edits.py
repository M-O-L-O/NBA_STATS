#### USE FOR CHANGES TO CSV

import pandas as pd
import numpy as np

def remove_row_by_phrase(csv, phrase):
    return csv.drop(csv[csv['Age'].str.contains(phrase, na=False)].index)
    
def remove_empty(csv):
    return csv.loc[csv['Season'].notnull()]
   
    
data = pd.read_csv("data/allPlayerStats-all.csv")
    
remove_row_by_phrase(remove_empty(data), 'Did not play').to_csv('player_each_year_all.csv')