
import sys
import datetime
import os
sys.path.append('C:/AnacondaProjects/sbb')

from NN_models import NN_Position_Model

m = NN_Position_Model()

m.load_training_data(data_files=['training_data/'+file for file in os.listdir('training_data/') if '_data'
    in file], names_file='training_data/board_base_column_names.p')

start=datetime.datetime.now()
m.train_bool(epochs=1000)
m.save_model(folder='models',filename='board_win_model')
print(datetime.datetime.now()-start, 'elapsed')
