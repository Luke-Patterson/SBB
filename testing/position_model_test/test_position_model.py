import sys
import datetime
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')

from NN_models import NN_Position_Model

m = NN_Position_Model()

m.load_training_data(data_file='sample_input/training data 20211127-161222_data.p'
    , names_file='sample_input/training data 20211127-161222_column_names.p')

start=datetime.datetime.now()
m.train_bool(epochs=1000)
m.save_model(folder='sample_output',filename='sample_board_prediction')
print(datetime.datetime.now()-start, 'elapsed')
