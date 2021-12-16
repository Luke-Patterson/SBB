import os
import sys
import datetime
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')
sys.path.append('C:/AnacondaProjects/sbb')

from NN_models import NN_Position_Model
from NN_models import XGB_Position_Model

# m = NN_Position_Model()
#
# m.load_training_data(data_files=['sample_input/training data 20211128-092615_data.p']
#     , names_file='sample_input/training data 20211128-092615_column_names.p',
#     max_train_size = 1000)
#
# start=datetime.datetime.now()
# m.train_bool(epochs=10)
# m.save_model(folder='sample_output/',filename='sample_board_prediction')
# print(datetime.datetime.now()-start, 'elapsed')
m = XGB_Position_Model()

m.load_training_data(data_files=['C:/AnacondaProjects/SBB/prod/training_data/'+file for
    file in os.listdir('C:/AnacondaProjects/SBB/prod/training_data/') if 'board'
    in file], max_train_size = 1000)

start=datetime.datetime.now()
m.train_bool(target_var='Position1_Baby Dragon',filter_var='Char_in_hand_Baby Dragon')
m.save_model(folder='sample_output/',filename='sample_board_prediction_xgb')
print(datetime.datetime.now()-start, 'elapsed')
