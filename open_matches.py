#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 18:13:46 2021

@author: zavecz
"""

import pandas as pd
import re
import json

data_all = []
def open_json_matches(file):
    df = pd.read_json(file)
    print(df.shape)
      
    df["teamsData_teams"] = df["teamsData"].apply(lambda x: list(x.keys()))
    
    df["team_1"] = df["teamsData"].apply(lambda x: list(x.keys())[0])
    df["team_2"] = df["teamsData"].apply(lambda x: list(x.keys())[1])
    
    df["side_1"] = df["teamsData"].apply(lambda x: list(x.items())[0][1].get("side"))
    df["side_2"] = df["teamsData"].apply(lambda x: list(x.items())[1][1].get("side"))
    
    df["players_1"] = df["teamsData"].apply(lambda x: list(x.items())[0][1].get("formation").get("lineup"))
    df["players_2"] = df["teamsData"].apply(lambda x: list(x.items())[1][1].get("formation").get("lineup"))
    
    df_1 = df.explode("players_1")
    df_1["player_id_1"] = df_1["players_1"].apply(lambda x: x.get("playerId"))
    df_1_match = df_1.groupby(by = ["wyId"])[["team_1","side_1"]].first()
    df_1_players = df_1.groupby(by = ["wyId"])["player_id_1"].apply(list)
    
    df_2 = df.explode("players_2")
    df_2["player_id_2"] = df_2["players_2"].apply(lambda x: x.get("playerId"))
    df_2_match = df_2.groupby(by = ["wyId"])[["team_2","side_2"]].first()
    df_2_players = df_2.groupby(by = ["wyId"])["player_id_2"].apply(list)
    
    df_match = pd.merge(df_1_players, df_2_players, how = "inner", on = "wyId")
    df_match = pd.merge(df_match, df_1_match, how = "inner", on = "wyId")
    df_match = pd.merge(df_match, df_2_match, how = "inner", on = "wyId")
    df_match = df_match.reset_index()
    print(df_match.shape)
    print(df_match.index)
    
    df_match["teamsData_teams_home"] = df_match["team_1"]
    df_match.loc[df_match["side_1"] == "away", "teamsData_teams_home"] = df_match["team_2"]
    
    df_match["teamsData_teams_away"] = df_match["team_2"]
    df_match.loc[df_match["side_1"] == "away", "teamsData_teams_away"] = df_match["team_1"]
    
    df_match["players_home"] = df_match["player_id_1"]
    df_match.loc[df_match["side_1"] == "away", "players_home"] = df_match["player_id_2"]
    
    df_match["players_away"] = df_match["player_id_2"]
    df_match.loc[df_match["side_1"] == "away", "players_away"] = df_match["player_id_1"]
    
    df_match.drop(["player_id_1", "player_id_2", "team_1", "side_1", "team_2", "side_2"], inplace = True, axis = 1)

    print(df_match.shape)
 
    data_all.append(df_match)
        
    #file_name = file.split('.')[0]
    #output = file_name + ".csv" 
    #df.to_csv(output)

for file in ["temp/matches_England.json", "temp/matches_European_Championship.json", "temp/matches_France.json", "temp/matches_Germany.json", "temp/matches_Italy.json", "temp/matches_Spain.json", "temp/matches_World_Cup.json"]:
    open_json_matches(file)

match_teams = pd.concat(data_all, axis = 0, ignore_index=True)
print(match_teams.shape)
print(match_teams.columns)

match_teams.to_csv("temp/match_team.csv", index_label="index")