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
    df = df.loc[:, ["teamsData_teams_home", "teamsData_teams_away", "wyId"]]
    print(df.shape)
    data_all.append(df)
        
    #file_name = file.split('.')[0]
    #output = file_name + ".csv" 
    #df.to_csv(output)

for file in ["temp/matches_England.json", "temp/matches_European_Championship.json", "temp/matches_France.json", "temp/matches_Germany.json", "temp/matches_Italy.json", "temp/matches_Spain.json", "temp/matches_World_Cup.json"]:
    open_json_matches(file)

match_teams = pd.concat(data_all, axis=0, ignore_index=True)
print(match_teams.shape)

match_teams.to_csv("temp/match_team.csv", index_label="index")