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
the lower and upper bounds of the coefficient estimates (*lower_bound*, *upper_bound*) and a dummy which is 1 when the *variable* is a, the  **Intercept**; b, a soccer **position** (*keep*); 
c, a statistically significant FIFA rating (being that individual level, team level for own team or team level for other team).
Within variables there are five main types: a, **Intercept** is the constant of the equation for each statistic (so for each statistic we have an **Intercept** in the *variable* column); b,
there are position dummies (**CAM**, **CB**, **CDM**, **CF**, **CM**, **LB**, **LM**, **LW**, **LWB**, **RB**, **RM**, **RW**, **RWB**, **ST**"); 
c, FIFA ratings - these are the individual level ratings; d, FIFA ratings with the suffix `_own` - these are the team level ratings for the own team in a given match; 
e, FIFA ratings with the suffix `_other` - these are the team level ratings for the other team playing in a given match.
It is important to add that when implementing the game, during the first try, in the equations I would keep all *variable*-s independent of the value of *keep*.
All statistics (*dependent*) should be kept obviously.
4. `regression_GK.csv`: GK statistics modeled following the logic of `regression.csv`
