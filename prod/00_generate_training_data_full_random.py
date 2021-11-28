# generate training data for randomly conducted games
import sys
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')

from Game import *

dc = Data_Collector(save_interval=100000,folder='training_data/')
dc.init_board_collect()

gb = Game_Batch()

gb.add_data_collector(dc)

gb.execute_game_batch(50000, verbose_lvl=0)

dc.export_data('board')
