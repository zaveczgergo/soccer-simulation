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

data = pd.read_csv("output/analysis_sample.csv", index_col = 0, low_memory = False)

data_analysis = pd.concat([data.loc[:,"Acceleration_y":"Volleys"],data.loc[:,"Acceleration_y_own":"Volleys_other"],data["assist"]], axis = 1)
data_analysis = pd.concat([data.loc[:,"Acceleration_y":"Volleys"],data["assist"]], axis = 1)
data_analysis["missing"] = data_analysis.isna().sum(axis = 1)
#print(data_analysis["missing"].value_counts())
#print(data_analysis.loc[data_analysis["missing"] > 0, :].shape[0])

data_nonmissing = data_analysis.dropna()
#print(data_analysis.shape)
#print(data_nonmissing.shape)

independent = data_nonmissing.loc[:,"Acceleration_y":"Volleys_other"]
#independent = data_nonmissing.loc[:,"Acceleration_y":"Volleys_other"]
dependent = data_nonmissing["assist"]

X_train, X_test, y_train, y_test = train_test_split(independent, 
                                                    dependent, 
                                                    test_size = 0.2, 
                                                    random_state = 0)

print("Training set has {} cases.".format(X_train.shape[0]))
print("Testing set has {} cases.".format(X_test.shape[0]))

clf_A = LinearRegression()
reg = clf_A.fit(X_train, y_train)
y_pred = clf_A.predict(X_test)
#y_train = clf_A.predict(X_train)
print(clf_A.coef_)
#print(reg.get_params())

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

clf_B = Ridge(alpha=0.5)
reg_r = clf_B.fit(X_train, y_train)
y_pred_r = clf_B.predict(X_test)
#y_train = clf_A.predict(X_train)
print(clf_B.coef_)
#print(reg.get_params())

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_r))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_r))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred_r)))

clf_C = Lasso()
reg_l = clf_C.fit(X_train, y_train)
y_pred_l = clf_C.predict(X_test)
#y_train = clf_A.predict(X_train)
print(clf_C.coef_)
coefs = dict(zip(independent.columns, clf_C.coef_.tolist()))
print(coefs)
print(type(clf_C.coef_.tolist()))
#print(reg.get_params())

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_l))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_l))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred_l)))

#clf_D = LinearSVC()
#reg_s = clf_D.fit(X_train, y_train)
#y_pred_s = clf_D.predict(X_test)
#y_train = clf_A.predict(X_train)
#print(clf_D.coef_)
#print(reg.get_params())

#print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_l))
#print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_l))
#print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred_l)))
#print(data["playerank_score"].corr(data["Overall"]))