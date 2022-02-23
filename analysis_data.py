#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 12:49:08 2021

@author: zavecz
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import LinearSVC
from sklearn import metrics

def ml_reg(model, var): 
    
    errors = {}
    coefs = {}
    
    dependent = data[var]
    
    x_train, x_test, y_train, y_test = train_test_split(independent, dependent, test_size = 0.2, random_state = 0)
    
    reg = model
    reg.fit(x_train, y_train)
    
    y_pred_train = reg.predict(x_train)
    y_pred_test = reg.predict(x_test)
    
    errors["mae_train"] = metrics.mean_absolute_error(y_train, y_pred_train)
    errors["mse_train"] = metrics.mean_squared_error(y_train, y_pred_train)
    errors["rmse_train"] = np.sqrt(metrics.mean_squared_error(y_train, y_pred_train))
    errors["mae_test"] = metrics.mean_absolute_error(y_test, y_pred_test)
    errors["mse_test"] = metrics.mean_squared_error(y_test, y_pred_test)
    errors["rmse_test"] = np.sqrt(metrics.mean_squared_error(y_test, y_pred_test))
    
    print(errors)
    print(reg.coef_)
    #return coefs

data = pd.read_csv("output/analysis_sample.csv", index_col = 0, low_memory = False)
print(data.columns)
data = pd.concat([data.loc[:,"Acceleration_y":"Volleys"], data.loc[:,"Acceleration_y_own":"Volleys_other"], data.loc[:,"assist":"clearance"]], axis = 1)
independent = data.loc[:,"Acceleration_y":"Volleys_other"]

print(data.columns)

model_A = LinearRegression()
model_B = Ridge(alpha=0.5)
model_C = Lasso()

for m in [model_A, model_B, model_C]:
    for d in ["assist", "shot", "pass", "interception", "foul"]:
        ml_reg(m, d)