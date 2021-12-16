
import sys
import datetime
import os
import time
sys.path.append('C:/AnacondaProjects/sbb')
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')

from NN_models import XGB_Position_Model
import pandas as pd

m = XGB_Position_Model()

m.load_training_data(data_files=['training_data/'+file for file in os.listdir('training_data/') if 'board'
    in file])

m.filter_training_data('battle_not_lost')
m.store_filter_data()

# char_df = pd.read_csv('C:/AnacondaProjects/sbb/output/char_list.csv')
# char_df = char_df.loc[(char_df.token == False)]
# for n, row in char_df.iterrows():
#     print(row['name'])
#     char_var = 'Char_in_hand_'+row['name']
#     m.filter_training_data(char_var, use_filt_data=True)
#     for i in range(1,8):
#         print('Position',i)
#         # start=datetime.datetime.now()
#         target_var = 'Position'+str(i)+'_'+row['name']
#         m.train_bool(target_var)
#         m.save_model(folder='models/char_position/',filename='position'+str(i)+'_'+row['name']+'_model_'+time.strftime("%Y%m%d-%H%M%S"))
#         # print(datetime.datetime.now()-start, 'elapsed')
#     m.restore_filter_data()

# repeat for None position
for i in range(1,8):
    print('Position',i,'None')
    # start=datetime.datetime.now()
    target_var = 'Position'+str(i)+'_None'
    m.train_bool(target_var)
    m.save_model(folder='models/char_position/',filename='position'+str(i)+'_None_model_'+time.strftime("%Y%m%d-%H%M%S"))
    # print(datetime.datetime.now()-start, 'elapsed')
