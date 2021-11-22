from Game import *
from datetime import datetime

while True:
    start = datetime.now()
    #g=Game(verbose_lvl=0, treasure_test = True)

    #g=Game(verbose_lvl=4, treasure_test = True, mimic_test = True)
    #g=Game(verbose_lvl=4, seed = 748998327, treasure_test = True, mimic_test = True)

    g=Game(verbose_lvl=4, treasure_test = True)
    #g=Game(verbose_lvl=4, seed=2136842904, treasure_test = True)
    Player1= Player('Player1')
    Player2= Player('Player2')
    Player3= Player('Player3')
    Player4= Player('Player4')
    Player5= Player('Player5')
    Player6= Player('Player6')
    Player7= Player('Player7')
    Player8= Player('Player8')
    g.start_game(players=[Player1,Player2,Player3,Player4,Player5,Player6,Player7,Player8])
    print(datetime.now()-start)
