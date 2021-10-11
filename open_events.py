#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 16:02:15 2021

@author: zavecz
"""

import pandas as pd
import numpy as np

tags = pd.read_csv("temp/tags2name-part.csv")

#data_all = []
#for file in ["events_England.json", "events_European_Championship.json", "events_France.json", "events_Germany.json", "events_Italy.json", "events_Spain.json", "events_World_Cup.json"]:
#    data = pd.read_json(file)
#    print(data.shape)
#    data_all.append(data)
#events = pd.concat(data_all, axis=0, ignore_index=True)
#print(events.shape)

data_all = []
def open_json(file):
    df = pd.read_json(file)
    print(df.shape)
  
    df = df.explode("tags")
  
    df = df[~df["tags"].isnull()]  
    df["tags"] = df["tags"].apply(lambda x: x["id"] if isinstance(x["id"], dict) else x["id"])
    
    df["position1"] = df["positions"].apply(lambda x: x[0])
    df["position_length"] = df["positions"].apply(lambda x: len(x))
    df = df.loc[df["position_length"] == 2,:]
    df["position2"] = df["positions"].apply(lambda x: x[1])
    df = df.drop("position_length", axis = 1)
    df["position1_x"] = df["position1"].apply(lambda x: x["x"])
    df["position1_y"] = df["position1"].apply(lambda x: x["y"])
    df["position2_x"] = df["position2"].apply(lambda x: x["x"])
    df["position2_y"] = df["position2"].apply(lambda x: x["y"])
    df["distance"] = np.sqrt((df["position1_x"] - df["position2_x"]) ** 2 + (df["position1_y"] - df["position2_y"]) ** 2)
 
    df = df[["subEventName", "eventName", "tags", "playerId", "matchId", "teamId", "subEventId", "id", "distance"]]
    df = df.merge(tags, how="left", left_on = "tags", right_on = "tag")  
    df = df[["subEventName", "eventName", "description", "distance", "playerId", "matchId"]]
    
    #distance to be used later for grouping
    
    df_1 = df.groupby(by = ["matchId", "playerId", "subEventName", "description"]).size().reset_index()
    df_2 = df.groupby(by = ["matchId", "playerId", "eventName", "description"]).size().reset_index()

    df_1.columns = ["matchId", "playerId", "subEventName", "description", "event_count"]
    df_2.columns = ["matchId", "playerId", "eventName", "description", "event_count"]
    
    df_1 = df_1.pivot(index = ["matchId", "playerId"], columns = ["subEventName", "description"], values = "event_count")
    df_2 = df_2.pivot(index = ["matchId", "playerId"], columns = ["eventName", "description"], values = "event_count")
    
    df = pd.read_json(file)
    df_3 = df.groupby(by = ["matchId", "playerId", "subEventName"]).size().reset_index()
    df_4 = df.groupby(by = ["matchId", "playerId", "eventName"]).size().reset_index()
    df_3.columns = ["matchId", "playerId", "subEventName", "event_count"]
    df_4.columns = ["matchId", "playerId", "eventName", "event_count"]
    df_3 = df_3.pivot(index = ["matchId", "playerId"], columns = ["subEventName"], values = "event_count")
    df_4 = df_4.pivot(index = ["matchId", "playerId"], columns = ["eventName"], values = "event_count")
   
    df = df_1.merge(df_2, how = "left", left_on = ["matchId", "playerId"], right_on = ["matchId", "playerId"])
    df = df.merge(df_3, how = "left", left_on = ["matchId", "playerId"], right_on = ["matchId", "playerId"])
    df = df.merge(df_4, how = "left", left_on = ["matchId", "playerId"], right_on = ["matchId", "playerId"])

    df = df.fillna(0).reset_index()
    
    df.columns = df.columns.map(lambda x: "".join([str(i) for i in x]).strip())   
    df = df.loc[:, (df != 0).any(axis=0)]
    print(df.shape)
    data_all.append(df)
        
    #file_name = file.split('.')[0]
    #output = file_name + ".csv" 
    #df.to_csv(output)

for file in ["temp/events_England.json", "temp/events_European_Championship.json", "temp/events_France.json", "temp/events_Germany.json", "temp/events_Italy.json", "temp/events_Spain.json", "temp/events_World_Cup.json"]:
    open_json(file)

events = pd.concat(data_all, axis=0, ignore_index=True)
events = events.fillna(0)
print(events.shape)

events.to_csv("temp/events.csv", index_label="index")
