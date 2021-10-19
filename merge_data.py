#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 21:19:29 2021

@author: zavecz
"""

import pandas as pd

match = pd.read_csv("temp/match-part.csv", index_col = "index")
match_teams = pd.read_csv("temp/match_team.csv", index_col = "index") 
player_rank = pd.read_csv("temp/player_rank-part.csv", index_col = "index")
player = pd.read_csv("temp/player-part.csv", index_col = "index")
events = pd.read_csv("temp/events.csv", index_col = "index")

data = match.merge(match_teams, how = "left", left_on = "wy_id", right_on = "wyId")
data = data.merge(player_rank, how = "left", left_on = "wy_id", right_on = "match_id")
data = data.merge(player, how = "left", left_on = "player_id", right_on = "wy_id")
data = data.merge(events, how = "left", left_on = ["match_id", "player_id"], right_on = ["matchId", "playerId"])

for df in [match, match_teams, player_rank, player, events, data]:
    print(df.columns)
    print(df.shape)

data.drop(["wy_id_x","wy_id_y","current_national_team_id","current_team_id","middle_name"], axis=1)
    
data.to_csv("temp/data_match.csv", index_label="index")
