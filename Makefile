objects = temp/cfo-data-analysis.db temp/*part.csv temp/events.gz temp/events*.json temp/events.csv temp/matches.gz temp/matches*.json temp/match_team.csv temp/data_match.csv temp/data_merged.csv temp/data_small.csv output/analysis_sample.csv output/rmse.csv output/regression.csv
all: $(objects)

output/regression.csv: analysis_data.py output/analysis_sample.csv
	python3 $<
output/rmse.csv: analysis_data.py output/analysis_sample.csv
	python3 $<
output/analysis_sample.csv: clean_data.py temp/data_small.csv
	python3 $<
temp/data_small.csv: create_columns.py temp/data_merged.csv
	python3 $<
temp/data_merged.csv: fifa_merge.py temp/data_match.csv input/CompleteDataset.csv
	python3 $<
temp/data_match.csv: merge_data.py temp/match-part.csv temp/match_team.csv temp/player_rank-part.csv temp/player-part.csv temp/events.csv
	python3 $<
temp/match_team.csv: open_matches.py temp/matches*.json
	python3 $<
temp/matches*.json:
	unzip -o temp/matches.gz -d temp/
temp/matches.gz:
	wget -O temp/matches.gz https://ndownloader.figshare.com/files/14464622
temp/events.csv: open_events.py temp/events*.json temp/tags2name-part.csv
	python3 $<
temp/events*.json:
	unzip -o temp/events.gz -d temp/
temp/events.gz:
	wget -O temp/events.gz https://ndownloader.figshare.com/files/14464685
temp/*part.csv: create_data.py temp/cfo-data-analysis.db
	python3 $<
temp/cfo-data-analysis.db: copy_data.py input/cfo-data.db
	python3 $<
