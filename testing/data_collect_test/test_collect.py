import sys
sys.path.append('C:/Users/Luke/AnacondaProjects/sbb')

from Game import *

g=Game(verbose_lvl=4)
g.load_objs()
dc = Data_Collector(game=g)
g.data_collector = dc
dc.init_board_collect()

for _ in range(2):
    start = datetime.now()

    Player1= Player('Player1')
    Player2= Player('Player2')
    Player3= Player('Player3')
    Player4= Player('Player4')
    Player5= Player('Player5')
    Player6= Player('Player6')
    Player7= Player('Player7')
    Player8= Player('Player8')
    g.run_game(players=[Player1,Player2,Player3,Player4,Player5,Player6,Player7,Player8])
    g.reset_game()

dc.export_data('board', csv_fmt = True)
