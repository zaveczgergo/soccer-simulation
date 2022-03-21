# Soccer Prediction

## description
This project intends to create and analyse a dataset containing match-player level data of soccer matches from five leagues (Bundesliga, LaLiga, Ligue1, Premier League, Serie A) 
in one season (2016-2017) and from two international cups. The idea is to predict player-level stats (e. g.: *assists*, *goals*, *tackles*, etc ...) 
based on player abilities (measured as fifa ratings). So far data collection, merging, wrangling and cleaning are done. Predictions are also done (except for **GK**-s), but fine-tuning is yet to come.

## use
Typing `make` in the shell should run all codes and create the `temp` (not uploaded to git, in `.gitignore`) and `output` data files 
1, from `input` files (not uploaded to git, in `.gitignore`) and 2, from files downloaded directly to `temp` with `wget`.
`Makefile` contains all the dependencies, so how `py` files build up the intermediate and final datasets, `analysis_sample.csv`.

## outputs
1. `analysis_sample.csv`: the data on which modeling is done. 
2. `rmse.csv`: root mean squared errors to select among models.
3. `regression.csv`: the statistics modeled (*dependent*), the variable on the right side of the equation (*variable*), 
the point estimate of the coefficient (*coefficient*), the standard error of the coefficent (*se*), the p-value of the coefficient (*pval*), 
the lower and upper bounds of the coefficient estimates (*lower_bound*, *upper_bound*) and a dummy which is 1 when the *variable* is either **Intercept** or a soccer **position** (*keep*).
