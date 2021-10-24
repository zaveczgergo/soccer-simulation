#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 22:08:07 2021

@author: zavecz
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data = pd.read_csv("temp/data_small.csv", index_col = 0, low_memory = False)

print(data.shape)
#datatype = data.dtypes.tolist()
datatype = dict(data.dtypes)
print(type(datatype))
print(datatype)
print(data['Aggression'].isna().sum())
print(data['Aggression'].count())
#data["Aggression_corr"] = data["Aggression"].apply(lambda x: x.split()[0] if "+" in x else x)
#data["Aggression_corr"] = data["Aggression"].astype(float) 
#data["Aggression_corr"] = pd.to_numeric(data["Aggression"], errors = "coerce") 
#print(data["Aggression_corr"].dtype)
#print(data['Aggression_corr'].isna().sum())
#print(data['Aggression_corr'].count())
#data["Aggression_corr"] = data["Aggression"].apply(lambda x: np.nan if x.str.contains("+") else x)

objects = data.select_dtypes("object").columns.tolist()
print(objects)
for element in ["dateutc","label","pos","short_name","Name","birth_date","Nationality","Club","Value","Wage"]:
    objects.remove(element)

for o in objects:
    o_1 = data[o].isna().sum()
    data[o] = pd.to_numeric(data[o], errors = "coerce")
    o_2 = data[o].isna().sum()
    print("Loss is: {} for {}".format(o_2-o_1,o))

print(objects)
for o in objects:
    data_o = data.groupby(["match_id","home"])[o].mean().reset_index()
    data_o = data_o.pivot(index = "match_id", columns = "home", values = o).reset_index()
    colname_home = o + "_home"
    colname_away = o + "_away"
    #colname_away = "{o}_away".format(o)
    data_o.columns = ["match_id", colname_home, colname_away]

    #    print(type(data_agression))
    #    print(data_agression)
    data = data.merge(data_o, how = "left", on = "match_id")

for o in objects:
    data.loc[data["home"] == 1, o + "_own"] = data[o + "_home"]
    data.loc[data["home"] == 1, o +"_other"] = data[o + "_away"]
    data.loc[data["home"] == 0, o + "_own"] = data[o + "_away"]
    data.loc[data["home"] == 0, o +"_other"] = data[o + "_home"]

#shape_old = data.shape[0]
#data.dropna(inplace = True)
#shape_new = data.shape[0]
#print("Loss due to average team ratings is {}".format(shape_old - shape_new))
#print(data.shape)
data.to_csv("output/analysis_sample.csv")
