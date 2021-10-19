#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:43:57 2021

@author: zavecz
"""

import pandas as pd
import difflib
import fuzzymatcher
from fuzzywuzzy import fuzz, process

#https://stackoverflow.com/questions/13636848/is-it-possible-to-do-fuzzy-match-merge-with-python-pandas
#https://www.analyticsvidhya.com/blog/2021/07/fuzzy-string-matching-a-hands-on-guide/
#https://www.geeksforgeeks.org/fuzzywuzzy-python-library/

match = pd.read_csv("temp/data_match.csv", index_col = "index", low_memory = False)
fifa = pd.read_csv("CompleteDataset.csv", index_col = 0, low_memory = False)

print(match.shape)
print(fifa.shape)

#fifa['merge_name'] = fifa['Name'].apply(lambda x: difflib.get_close_matches(x, match['short_name'], n = 1, cutoff = 0.8))
#print(fifa['merge_name'].head())

match['merge_name'] = match['short_name'].apply(lambda x: difflib.get_close_matches(x, fifa['Name'], n = 1, cutoff = 0.7))
print(match.shape)
match["merge_name_string"] = match["merge_name"].apply(pd.Series)
print(match.shape)

#match.to_csv("output/data_merged_try.csv", index_label="index")

data = match.merge(fifa, how = "left", left_on = "merge_name_string", right_on = "Name")

#fuzzymatcher.fuzzy_left_join(match, fifa, left_on = "short_name", right_on = "Name")

#match["merge_name"] = match["short_name"].apply(lambda x: process.extract(x, fifa["Name"], limit=1)) 

data.to_csv("temp/data_merged.csv", index_label="index")

#40482 (0.7) vs 35432 (0.8)
print(data.shape)
print(data["merge_name"].isnull().sum())
data_clean = data[data["merge_name"] != "[]"]
print(data_clean.shape)
