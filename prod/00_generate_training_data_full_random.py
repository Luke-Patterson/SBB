# generate training data for randomly conducted games
import sys
sys.path.append('C:/AnacondaProjects/sbb')

from Game import *

dc = Data_Collector(folder='training_data/')
dc.init_data_collect()

gb = Game_Batch()

gb.add_data_collector(dc)

try:
    gb.execute_game_batch(50000, verbose_lvl=0)
except Exception as e:
    print(e)
    dc.export_data('board')
    dc.export_data('purchased')
    import pdb; pdb.set_trace()

dc.export_data('board')
dc.export_data('purchased')
