# conduct analysis of which characters are best for each board state
import pandas as pd
import pickle
import statistics as stat
import numpy as np

data = pickle.load(open(
    "C:/AnacondaProjects/SBB/prod/training_data/training data 20211203-145100_data.p", 'rb'))
colnames = pickle.load(open(
    "C:/AnacondaProjects/SBB/prod/training_data/training data 20211203-145100_column_names.p", 'rb'))

# load training data
df = pd.DataFrame.sparse.from_spmatrix(data, columns = colnames['all_cols'])

# load chars to run through
stat_df = pd.read_csv('C:/AnacondaProjects/SBB/output/char_list.csv')

stat_df = stat_df.loc[stat_df.token == False]

# average win rate by turn number
win_df = pd.DataFrame(df[['turn_num','battle_not_lost']].values,
    columns = ['turn_num','battle_not_lost'])
avg_rate = win_df.groupby('turn_num').mean()[0:20]

# average win rate by position


# start a dataframe to calculate win rates for each character, turn number, and
# another dataframe for character and position
all_rate_df = pd.DataFrame(columns = ['char','upgraded', 'turn_num','win_rate'])

pos_rate_df = pd.DataFrame(columns = ['char','upgraded','win_rate']+['Position'+str(i)
    +'_win_rate' for i in range(1,8)])

# iterate for each character to get win rates and add to all_rate_df
# in a function because it needs to be repeated for upgraded characters
def _create_all_rate_(all_rate_df, pos_rate_df, upgraded):
    for n, row in stat_df.iterrows():
        print(n,'of',len(stat_df.index))
        name = row['name']
        group_cols = [i for i in df.columns if name in i]+['turn_num']

        if upgraded:
            char_col = 'Char_upgr_' + name
        else:
            char_col = 'Char_' + name

        # grab relevant columns
        char_df = pd.DataFrame(df[group_cols+['battle_not_lost']].values,
            columns = group_cols + ['battle_not_lost'])

        # calculate mean win rate in any position
        all_rate = char_df.groupby([char_col,'turn_num']) \
            ['battle_not_lost'].mean()

        all_rate = all_rate.loc[(all_rate.index.get_level_values(char_col) ==1)]
        all_rate.index = all_rate.index.get_level_values('turn_num')
        all_rate.name = 'win_rate'

        # fill in any indexes for turns not found
        missing_vals = [i for i in range(1,21) if i not in all_rate.index]
        all_rate= all_rate.append(pd.Series([np.nan for _ in range(len(missing_vals))],
            index = missing_vals, dtype='float64'))
        all_rate= all_rate.sort_index()

        # filter to first 20 turns and add cols for master data frame
        all_rate = all_rate[0:20]
        all_rate = pd.DataFrame(all_rate)
        all_rate = all_rate.reset_index()
        all_rate = all_rate.rename({'index':'turn_num',0:'win_rate'},axis=1)
        all_rate['char'] = name
        all_rate['upgraded'] = upgraded
        all_rate_df=all_rate_df.append(all_rate, ignore_index = True)

        # for each position, identify win rates of that character being in that position
        pos_rec = pd.Series(dtype='object')
        pos_rec['char'] = name
        pos_rec['upgraded'] = upgraded
        pos_rec['win_rate'] = char_df.groupby([char_col])['battle_not_lost'].mean()[1]
        for i in range(1,8):
            pos_df = char_df.groupby([char_col,'Position'+str(i)+'_'+name]) \
                ['battle_not_lost'].mean()
            pos_df = pos_df.loc[(pos_df.index.get_level_values(char_col) ==1) &
                (pos_df.index.get_level_values('Position'+str(i)+'_'+name) ==1)]
            if pos_df.empty:
                pos_rec['Position'+str(i)+'_win_rate'] = np.nan
            else:
                pos_rec['Position'+str(i)+'_win_rate'] = pos_df.values[0]

            # pos_df.index = pos_df.index.get_level_values('turn_num') - 1
            # pos_df = pos_df.loc[0:20]
            # all_rate['Position'+str(i)+'_win_rate'] = pos_df

        # calculate standard deviation
        pos_rec['std_dev'] = pos_rec[['Position'+str(i)+'_win_rate' for i in
            range(1,8)]].std()

        # "good position" will be over 1.75% based on some checks
        pos_rec['good_bound'] = pos_rec['win_rate'] + .0175
        pos_rec['bad_bound'] = pos_rec['win_rate'] - .0175

        result = []
        for i in range(1,8):
            if pos_rec['Position'+str(i)+'_win_rate'] > pos_rec['good_bound']:
                result.append(i)

        pos_rec['good_pos'] = result

        result = []
        for i in range(1,8):
            if pos_rec['Position'+str(i)+'_win_rate'] < pos_rec['bad_bound']:
                result.append(i)

        pos_rec['bad_pos'] = result

        pos_rec = pos_rec.drop(['good_bound','bad_bound','std_dev'])
        pos_rate_df = pos_rate_df.append(pos_rec, ignore_index=True)

    return(all_rate_df, pos_rate_df)

all_rate_df, pos_rate_df = _create_all_rate_(all_rate_df, pos_rate_df, upgraded = False)
all_rate_df, pos_rate_df = _create_all_rate_(all_rate_df, pos_rate_df, upgraded = True)

# add max vals
pos_cols = ['Position'+str(i)+'_win_rate' for i in range(1,8)]
pos_rate_df['max_val'] = pos_rate_df[pos_cols].max(axis=1)
pos_rate_df['wheremax_pos'] = pos_rate_df[pos_cols].idxmax(axis=1).str[8]

# generate optimal positions

all_rate_df.to_pickle('output/char_turn_win_rates.p')
pos_rate_df.to_pickle('output/char_position_win_rates.p')
import pdb; pdb.set_trace()
