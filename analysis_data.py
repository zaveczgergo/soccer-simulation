import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import LinearSVC
from sklearn import metrics
from regressors import stats
from itertools import chain

def ml_reg(model, var): 
    
    errors = {}
    coefs = {}
    
    dependent = data[var]
    
    x_train, x_test, y_train, y_test = train_test_split(independent, dependent, test_size = 0.2, random_state = 0)
    
    reg = model
    reg.fit(x_train, y_train)
    
    y_pred_train = reg.predict(x_train)
    y_pred_test = reg.predict(x_test)
    
    errors["rmse_train"] = np.sqrt(metrics.mean_squared_error(y_train, y_pred_train))
    errors["rmse_test"] = np.sqrt(metrics.mean_squared_error(y_test, y_pred_test))
    # print(metrics.r2_score(y_train, y_pred_train))
    
    se = stats.coef_se(reg, x_train, y_train)
    se_list = [s.real for s in se]
    se_dict = {}
    independent_int = independent.columns.copy().insert(0, "Intercept")
    for s, feat in zip(se_list, independent_int):
        se_dict[feat] = s
    
    pval = stats.coef_pval(reg, x_train, y_train)
    pval_list = [p.real for p in pval]
    pval_dict = {}
    for p, feat in zip(pval_list, independent_int):
        pval_dict[feat] = p
    
    coef_dict = {}
    coef_dict["Intercept"] = reg.intercept_
    for coef, feat in zip(reg.coef_, independent.columns):
        coef_dict[feat] = coef
    
    return errors, coef_dict, se_dict, pval_dict

data = pd.read_csv("output/analysis_sample.csv", index_col = 0, low_memory = False)
data = data.loc[data["pos"] != "GK",:]

print(data.shape)
print(data.columns[data.isnull().any()])
data.dropna(subset = ["goal_scored", "assist", "shot", "shot_target", "pass",
                      "pass_good", "pass_key", "pass_long", "pass_short", "pass_through",
                      "pass_cross", "tackle_good", "tackle_bad", "interception", "foul",
                      "dribble", "control_bad", "corner", "clearance"], inplace = True, axis = 0)
print(data.shape)

pos_cat = pd.get_dummies(data["pos"])
independent = pd.concat([data.loc[:,"Acceleration_y":"Volleys"], data.loc[:,"Acceleration_y_own":"Volleys_other"], pos_cat.loc[:,"CAM":"ST"]], axis = 1)

dependent_list = ["goal_scored","assist","shot","shot_target","pass","pass_good","pass_key","pass_long","pass_short","pass_through","pass_cross","tackle_good","tackle_bad","interception","foul","dribble","control_bad","corner","clearance"]

model_A = LinearRegression()
model_B = Ridge(alpha=0.5)
model_C = Lasso()

rmse = {}
coef = {}
se = {}
pval = {}
for m in [model_A, model_B, model_C]:
    model_string = m.__class__.__name__
    rmse_model_dep = {}
    coef_model_dep = {}
    se_model_dep = {}
    pval_model_dep = {}
    
    for d in dependent_list:
        rmse_dep = ml_reg(m, d)[0]
        rmse_model_dep[d] = rmse_dep
        
        coef_dep = ml_reg(m, d)[1]
        coef_model_dep[d] = coef_dep        

        se_dep = ml_reg(m, d)[2]
        se_model_dep[d] = se_dep
        
        pval_dep = ml_reg(m, d)[3]
        pval_model_dep[d] = pval_dep 
        
    rmse[model_string] = rmse_model_dep
    coef[model_string] = coef_model_dep
    se[model_string] = se_model_dep
    pval[model_string] = pval_model_dep

rmse_df = pd.DataFrame(rmse).reset_index()

coef_df = pd.DataFrame(coef).reset_index()
coef_df = coef_df.melt(id_vars = "index")
coef_df.columns = ["dependent","model","coefficient"]
coef_df_coefficient = pd.DataFrame(coef_df["coefficient"].values.tolist())
#coef_df_coefficient = pd.json_normalize(coef_df["coefficient"])
#coef_df_coefficient = coef_df["coefficient"].apply(pd.Series)
#coef_df_coefficient = pd.DataFrame.from_records(coef_df["coefficient"].tolist())
coef_df = pd.concat([coef_df.drop("coefficient", axis = 1), coef_df_coefficient], axis = 1)
coef_df.sort_values(by = ["dependent", "model"], inplace = True)
coef_df = coef_df.melt(id_vars = ["dependent", "model"])
coef_df.columns = ["dependent","model","variable","coefficient"]

se_df = pd.DataFrame(se).reset_index()
se_df = se_df.melt(id_vars = "index")
se_df.columns = ["dependent","model","se"]
se_df_se= pd.DataFrame(se_df["se"].values.tolist())
se_df = pd.concat([se_df.drop("se", axis = 1), se_df_se], axis = 1)
se_df.sort_values(by = ["dependent", "model"], inplace = True)
se_df = se_df.melt(id_vars = ["dependent", "model"])
se_df.columns = ["dependent","model","variable","se"]

pval_df = pd.DataFrame(pval).reset_index()
pval_df = pval_df.melt(id_vars = "index")
pval_df.columns = ["dependent","model","pval"]
pval_df_pval= pd.DataFrame(pval_df["pval"].values.tolist())
pval_df = pd.concat([pval_df.drop("pval", axis = 1), pval_df_pval], axis = 1)
pval_df.sort_values(by = ["dependent", "model"], inplace = True)
pval_df = pval_df.melt(id_vars = ["dependent", "model"])
pval_df.columns = ["dependent","model","variable","pval"]

regression = pd.merge(coef_df, se_df, how = "inner", left_on = ["dependent", "model", "variable"], right_on = ["dependent", "model", "variable"])
regression = pd.merge(regression, pval_df, how = "inner", on = ["dependent", "model", "variable"])

dummy_list = ["Intercept","CAM","CB","CDM","CF","CM","LB","LM","LW","LWB","RB","RM","RW","RWB","ST"]
regression.loc[regression["variable"].isin(dummy_list), "se"] = np.nan 
regression.loc[regression["variable"].isin(dummy_list), "pval"] = np.nan

regression["lower_bound"] = regression["coefficient"] - 1.96 * regression["se"]
regression["upper_bound"] = regression["coefficient"] + 1.96 * regression["se"]
regression["keep"] = 0

regression.loc[(regression["pval"] < 0.05) | (regression["variable"].isin(dummy_list)), "keep"] = 1
#regression.loc[(regression["pval"] < 0.1) | (regression["variable"] == "Intercept"), "keep"] = 1

regression = regression.loc[regression["model"] == "LinearRegression", :]
#regression = regression.loc[regression["keep"] == 1, :]
regression.drop("model", axis = 1, inplace = True)
#regression.drop(["model", "keep"], axis = 1, inplace = True)

regression.sort_values(["dependent", "variable"], inplace = True)

rmse_df.to_csv("output/rmse.csv", index = False)
regression.to_csv("output/regression.csv", index = False)

#coef_df.to_csv("output/coefficients.csv", index = False)
#se_df.to_csv("output/se.csv", index = False)
#pval_df.to_csv("output/pval.csv", index = False)