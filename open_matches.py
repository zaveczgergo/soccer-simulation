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
    df["teamsData_teams_home"] = df["teamsData"].apply(lambda x: list(x.keys())[0])
    df["teamsData_teams_away"] = df["teamsData"].apply(lambda x: list(x.keys())[1])
    print(df.shape)
    
    teams_dict = df["teamsData"].values
    teams_dict_agg = []
    for e in teams_dict:
        e_df = pd.DataFrame.from_dict(e, orient="index")
        teams_dict_agg.append(e_df)
    teams_dict_df = pd.concat(teams_dict_agg)
    teams_dict_df["lineup"] = teams_dict_df["formation"].apply(lambda x: x["lineup"])
    players_list = []
    for i in range(11):
        players = teams_dict_df["lineup"].apply(lambda x: x[i]["playerId"])
        players_list.append(players)
    players_df = pd.concat(players_list, axis = 1)
    players_df = pd.concat([teams_dict_df["side"],players_df], axis = 1)
    players_df["onelist"] = players_df.iloc[:,1:12].apply(lambda x: list(x), axis = 1)
    players_df = players_df.loc[:,["side","onelist"]].reset_index()
    players_df['match'] = (players_df.index / 2 + 1).astype(int)
    players_df = players_df.pivot(index = "match", columns = "side", values = ["index", "onelist"]).reset_index()
    players_df.columns = map(lambda x: ".".join([str(i) for i in x]).strip(), players_df.columns)
    players_df = players_df.iloc[:, 1:5]
    players_df.columns = ["teamsData_teams_away", "teamsData_teams_home", "players_away", "players_home"]
    players_df = players_df.iloc[:, 2:4]
    data = pd.concat([df,players_df], axis = 1)
    data = data.loc[:, ["teamsData_teams_home", "teamsData_teams_away", "players_home", "players_away", "wyId"]]
    print(data.shape)
 
    data_all.append(data)
        
    #file_name = file.split('.')[0]
    #output = file_name + ".csv" 
    #df.to_csv(output)

for file in ["temp/matches_England.json", "temp/matches_European_Championship.json", "temp/matches_France.json", "temp/matches_Germany.json", "temp/matches_Italy.json", "temp/matches_Spain.json", "temp/matches_World_Cup.json"]:
    open_json_matches(file)

match_teams = pd.concat(data_all, axis = 0, ignore_index=True)
print(match_teams.shape)
print(match_teams.columns)

match_teams.to_csv("temp/match_team.csv", index_label="index")