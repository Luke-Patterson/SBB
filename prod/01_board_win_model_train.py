
import sys
import datetime
import os
import time
#sys.path.append('C:/AnacondaProjects/sbb')
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')

from NN_models import NN_Position_Model

m = NN_Position_Model()

m.load_training_data(data_files=['training_data/'+file for file in os.listdir('training_data/') if '_data.p'
    in file], names_file='training_data/board_base_column_names.p', max_train_size = 150000)

start=datetime.datetime.now()
m.train_bool(epochs=500)
m.save_model(folder='models/',filename='board_win_model '+time.strftime("%Y%m%d-%H%M%S"))
print(datetime.datetime.now()-start, 'elapsed')
