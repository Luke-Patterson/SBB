# conduct analysis of which characters are best for each board state
import pandas as pd
import pickle
import statistics as stat
data = pickle.load(open(
    "C:/AnacondaProjects/SBB/prod/training_data/training data 20211203-145100_data.p", 'rb'))
colnames = pickle.load(open(
    "C:/AnacondaProjects/SBB/prod/training_data/training data 20211203-145100_column_names.p", 'rb'))

#
df = pd.DataFrame.sparse.from_spmatrix(data, columns = colnames['all_cols'])

# load chars to run through
stat_df = pd.read_csv('C:/AnacondaProjects/SBB/output/char_list.csv')

stat_df = stat_df.loc[stat_df.token == False]

win_df = pd.DataFrame(df[['turn_num','battle_not_lost']].values,
    columns = ['turn_num','battle_not_lost'])
avg_rate = win_df.groupby('turn_num').mean()[0:20]

# start a dataframe to calculate win rates for each character, turn number, and position
all_rate_df = pd.DataFrame(columns = ['char','upgraded', 'turn_num','win_rate']+['Position'+str(i)
    +'_win_rate' for i in range(1,8)])


# iterate through each character to populate win rates
# for n, row in stat_df.iterrows():
for n, row in stat_df.iloc[22:,:].iterrows():
    print(n,'of',len(stat_df.index))
    name = row['name']
    group_cols = [i for i in df.columns if name in i]+['turn_num']

    # get all columns with relevant information
    char_df = pd.DataFrame(df[group_cols+['battle_not_lost']].values,
        columns = group_cols + ['battle_not_lost'])

    all_rate = char_df.groupby(['Char_'+name,'turn_num']) \
        ['battle_not_lost'].mean()
    all_rate = all_rate.loc[(all_rate.index.get_level_values('Char_'+name) ==1)]
    all_rate.index = all_rate.index.get_level_values('turn_num')
    all_rate.name = 'win_rate'
    all_rate = all_rate[0:20]
    all_rate = pd.DataFrame(all_rate)
    all_rate = all_rate.reset_index()
    all_rate = all_rate.rename({'index':'turn_num'},axis=1)
    all_rate['char'] = name
    all_rate['upgraded'] = False

    for i in range(1,8):
        pos_df = char_df.groupby(['Char_'+name,'Position'+str(i)+'_'+name,'turn_num']) \
            ['battle_not_lost'].mean()
        pos_df = pos_df.loc[(pos_df.index.get_level_values('Char_'+name) ==1) &
            (pos_df.index.get_level_values('Position'+str(i)+'_'+name) ==1)]
        pos_df.index = pos_df.index.get_level_values('turn_num')
        pos_df = pos_df[0:20].reset_index(drop=True)
        all_rate['Position'+str(i)+'_win_rate'] = pos_df
    all_rate_df=all_rate_df.append(all_rate, ignore_index = True)
import pdb; pdb.set_trace()
