import pandas as pd
import os
import re
from itertools import chain

path = os.path.join(os.getcwd(), 'ncaa_2017_games.txt')
names = ['date', 'win_team', 'win_team_score', 'lose_team', 'lose_team_score', 'crap']
specs = [(0, 10), (10, 36), (36, 40), (40, 64), (64, 68), (69, 1000)]
games = pd.read_fwf(path, names=names, colspecs=specs)

# remove @ from team name
for col in ['win_team', 'lose_team']:
    games[col] = games[col].apply(lambda x: re.sub('@', '', x))


# for a given team, return the unique list of all teams that beat them
def get_champs(team):
    return list(games.loc[games['lose_team'] == team, 'win_team'].unique())


# initialize
all_champs = [['Villanova']]
new_champs = ['Villanova']
num_new_champs = 1
# search until no new champs are found
while num_new_champs > 0:
    print(num_new_champs, new_champs)
    for team in all_champs[-1]:
        # get the new champs based on the most recently added champs
        new_champs = get_champs(team)
        # dedupe against champs already contained in the main list (chain flattens the main list)
        new_champs = [c for c in new_champs if c not in list(chain(*all_champs))]
    num_new_champs = len(new_champs)
    all_champs.append(new_champs)

# summarize
print('\n')
total_teams = len(pd.concat([games['win_team'], games['lose_team']]).unique())
transitive_champs = len(list(chain(*all_champs)))

print('Total teams: ' + str(total_teams))
print('Transitive champs: ' + str(transitive_champs))
print('Non-transitive champs: ' + str(total_teams - transitive_champs))
