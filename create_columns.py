#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 14:42:16 2021

@author: zavecz
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv("temp/data_merged.csv", index_col = 0, low_memory = False)

print(data.shape)

data["assist"] = data["Head passAssist"] + data["High passAssist"] + data["Shot_xAssist"] + data["Simple passAssist"] + data["Smart passAssist"] + data["TouchAssist"] + data["AccelerationAssist"] + data["Air duelAssist"] + data["CornerAssist"] + data["CrossAssist"] + data["Free Kick_xAssist"] + data["Free kick crossAssist"] + data["Goal kickAssist"]
#data["assist2"] = data[["Head passAssist", "High passAssist"]].sum(axis=1)
#print(data.loc[data["assist"] == data["assist2"],:].shape)
#print(data.loc[data["assist"] != data["assist2"],:].shape)

#shot_x and shot_y are the same while foul_x and foul_y are not
data["shot"] = data["Free kick shot"] + data["Shot_x"]
data["shot_target"] = data["Free kick shotAccurate"] + data["Shot_xAccurate"]
data["pass"] = data["Pass"] + data["Corner"] + data["Free kick cross"]
data["pass_good"] = (data["PassAccurate"] + data["CornerAccurate"] + data["Free kick crossAccurate"]) / data["pass"] * 100
data["pass_key"] = (data["PassKey pass"] + data["CornerKey pass"] + data["Free kick crossKey pass"]) # / data["pass"] * 100
data["pass_long"] = data["Launch"]
data["pass_short"] = data["pass"] - data["pass_long"]
data["pass_through"] = data["High passThrough"] + data["Smart passThrough"]
data["pass_cross"] = data["Cross"] + data["Free kick cross"]
data["tackle_good"] = data["Ground defending duelAccurate"]
data["tackle_bad"] = data["Ground defending duelNot accurate"]
int_cols = [c for c in data.columns if 'Interception' in c]
print(int_cols)
data["interception"] = data["Others on the ballInterception"] + data["PassInterception"] + data["Shot_xInterception"] + data["DuelInterception"]
#data["foul2"] = data["Foul_x"]
data["foul"] = data["Foul_y"]
#print(data["foul"].mean())
#print(data["foul2"].mean())
data["dribble"] = data["Ground attacking duelAccurate"]
print(data["dribble"].sum())
data["control_bad"] = data["Ground attacking duelNot accurate"]
data["corner"] = data["Corner"]
data["clearance"] = data["Clearance"]
#print(pd.crosstab(index = data["role_cluster"], columns = data["clearance"]))
#print(data.groupby("role_cluster")["clearance"].mean())

#pos = pd.concat([data[["Preferred Positions"]], data["Preferred Positions"].str.split(" ", expand = True)], axis = 1).iloc[:, 0:2]
pos = pd.concat([data[["Preferred Positions"]], data["Preferred Positions"].str.split(" ", expand = True)], axis = 1).iloc[:, 1]
pos = pd.DataFrame(pos)
pos.columns = ["pos"]
print(pos.columns)
data = pd.concat([data, pos], axis = 1)
print(data.groupby("pos")["clearance"].mean())

#data["home_dummy"] = np.where(data["player_id"].isin(data["players_home"]), 1, 0)
data["home_dummy"] = data.apply(lambda x: str(x["player_id"]) in str(x["players_home"]), axis=1)
data["away_dummy"] = data.apply(lambda x: str(x["player_id"]) in str(x["players_away"]), axis=1)

for dummy in [data["home_dummy"], data["away_dummy"]]:
    print(dummy.value_counts())

data.loc[data["home_dummy"] == True, "home"] = 1
data.loc[data["away_dummy"] == True, "home"] = 0
print(data["home"].value_counts())

data = data.loc[:,["competition_id","dateutc","label","winner","teamsData_teams_home","teamsData_teams_away","match_id","current_team_id","home",
                   "player_id","pos","short_name","Name","birth_date","Age","Nationality","Overall","Potential","Club","Value","Wage",
                   "Acceleration_y","Aggression","Agility","Balance","Ball control","Composure","Crossing","Curve","Dribbling","Finishing","Free kick accuracy","Heading accuracy","Interceptions","Jumping","Long passing","Long shots","Marking","Penalties","Positioning","Reactions","Short passing","Shot power","Sliding tackle","Sprint speed","Stamina","Standing tackle","Strength","Vision","Volleys",
                   "GK diving","GK handling","GK kicking","GK positioning","GK reflexes",
                   "playerank_score","goal_scored","minutes_played","assist","shot","shot_target","pass","pass_good","pass_key","pass_long","pass_short","pass_through","pass_cross","tackle_good","tackle_bad","interception","foul","dribble","control_bad","corner","clearance"]]

#for var in ["pass_good", "pass_key"]:
#    ax = sns.distplot(data[var], kde = False)
#ax = sns.distplot(data["pass_good"], kde = False)
#ax2 = sns.distplot(data["pass_key"], kde = False)

#analysis_sample = data[["goal_scored","assist", "shot", "shot_target"]]

print(data.shape)
#print(analysis_sample.shape)
#data.to_csv("output/testing.csv")
data.to_csv("temp/data_small.csv")
