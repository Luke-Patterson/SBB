# generate training data for randomly conducted games
import sys
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')
sys.path.append('C:/AnacondaProjects/sbb')
sys.path.append('C:/AnacondaProjects/sbb/Graphviz/bin')

from Game import *
from Logic import *


dc = Data_Collector()
dc.init_board_collect()

gb = Game_Batch()
gb.add_data_collector(dc)

l = NN_Logic()
l.load_model(label = 'board', filepath='sample_output/board_win_model 20211202-154502.p')

gb.logic = l

gb.execute_game_batch(10000, verbose_lvl=4)

dc.export_data('board')
