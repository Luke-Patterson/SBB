
import sys
import datetime
import os
import time
import pickle
import pandas as pd
import scipy
sys.path.append('C:/AnacondaProjects/sbb')
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')

from NN_models import XGB_Position_Model

m = XGB_Position_Model()
names_file = 'sample_input/training data 20211128-092615_column_names.p'
m.load_model(label = 'board', filepath='sample_output/board_win_model 20211203-131225.p')
m.load_training_data(data_files=['C:/AnacondaProjects/SBB/prod/training_data/'+file for
    file in os.listdir('C:/AnacondaProjects/SBB/prod/training_data/') if '_data.p'
    in file],names_file=names_file)

train_columns = pickle.load(open(names_file, 'rb'))
sample_X = m.unseen_data[0:500,0:998]
preds = m.model.predict_proba(sample_X)
df = pd.DataFrame.sparse.from_spmatrix(sample_X, columns = train_columns[0:998])
df['preds'] = pd.DataFrame(preds)[1]

# test to see if there's a difference in prob for basic support char
new_rec1 = pd.Series([0 for _ in range(998)],index=df.columns[0:998])
new_rec2 = pd.Series([0 for _ in range(998)], index=df.columns[0:998])
new_rec3 = pd.Series([0 for _ in range(998)], index=df.columns[0:998])

new_rec1['turn_num'] = 2
new_rec2['turn_num'] = 2
new_rec3['turn_num'] = 2

new_rec1['Char_Baby Root'] = 1
new_rec2['Char_Baby Root'] = 1
new_rec3['Char_Baby Root'] = 1

new_rec1['Char_Labyrinth Minotaur'] = 1
new_rec2['Char_Labyrinth Minotaur'] = 1
new_rec3['Char_Labyrinth Minotaur'] = 1

new_rec1['Position1_Baby Root'] = 1
new_rec2['Position5_Baby Root'] = 1
new_rec3['Position5_Baby Root'] = 1

new_rec1['Position2_Labyrinth Minotaur'] = 1
new_rec2['Position4_Labyrinth Minotaur'] = 1
new_rec3['Position1_Labyrinth Minotaur'] = 1

def _predict_rec_(rec):
    return(m.model.predict_proba(scipy.sparse.csr_matrix(rec.values)))

print('Baby root 1, minotaur 2 pred:',_predict_rec_(new_rec1))
print('Baby root 5, minotaur 4 pred:',_predict_rec_(new_rec2))
print('Baby root 5, minotaur 1 pred:',_predict_rec_(new_rec3))
