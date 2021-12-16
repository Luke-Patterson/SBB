# generate training data for randomly conducted games
import sys
sys.path.append('C:/AnacondaProjects/sbb')

from Game import *

dc = Data_Collector(folder='training_data/')
dc.init_data_collect()

gb = Game_Batch()

gb.add_data_collector(dc)

for _ in range(5):
    gb.execute_game_batch(10000, verbose_lvl=0)
    dc.export_data('board')
    dc.export_data('purchased')
