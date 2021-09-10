from Heroes import *
from Treasures import *
from Characters import *
from Heroes import *
from Player import *
from Spells import *
from copy import deepcopy
import itertools
import random

class Game:
    def __init__(self, verbose_lvl=2, seed=None):
        self.char_pool=[]
        self.treasures = []
        self.turn_counter = 0
        self.players=[]
        self.winner = None
        self.verbose_lvl = verbose_lvl
        if seed!=None:
            self.seed=seed
        else:
            self.seed=random.randint(1,10000000000)
        random.seed(self.seed)

    # functions for start of the game.
    def start_game(self,players):
        # set up initial states
        self.players=players
        for p in self.players:
            p.game=self
        self.load_hero_list()
        self.load_char_pool()
        self.load_treasures()
        self.load_spells()

        # have players select heros
        self.select_heroes_phase()

        # start the turns
        while self.winner==None:
            self.complete_turn()

    def load_hero_list(self):
        # master_hero_list is from Heroes..py
        self.available_heroes= master_hero_list

    def load_char_pool(self):
        # master_char_list is from Characters.py
        self.char_pool=[]
        for char in master_char_list:
            if char.lvl==6:
                for _ in range(10):
                    self.char_pool.append(deepcopy(char))
            else:
                for _ in range(15):
                    self.char_pool.append(deepcopy(char))

    def load_treasures(self):
        # master_treasure_list is from Treasures.py
        self.treasures=master_treasure_list

    def load_spells(self):
        # master_spell_list is from Treasures.py
        self.spells=master_spell_list

    # each player selects one of four heros
    def select_heroes_phase(self):
        choices = {}
        for p in self.players:
            choices[p] = random.sample(self.available_heroes, 4)
            for h in choices[p]:
                self.available_heroes.remove(h)
            unchosen_heroes = p.choose_hero(choices[p])
            for h in unchosen_heroes:
                self.available_heroes.append(h)


    # functions to facilitate turns
    def complete_turn(self):
        self.start_of_turn_effects()
        self.init_shop_phase()
        self.init_battle_phase()
        self.end_of_turn_effects()

    def start_of_turn_effects(self):
        self.turn_counter += 1
        if self.verbose_lvl>=1:
            print('Round', self.turn_counter, 'starts')

        for p in self.players:
            p.start_of_turn_effects()

    def init_shop_phase(self):
        for p in self.players:
            p.do_shop_phase()

    def init_battle_phase(self):
        for p in self.players:
            p.deploy_for_battle()
        self.pair_opponents()

    def end_of_turn_effects(self):
        for p in self.players:
            p.end_of_turn_effects()
        self.check_for_winner()

    def check_for_winner(self):
        pass

    # function to pair opponents
    # TODO: currently randomly selects opponents. Need to adjust to match SBB algo
    def pair_opponents(self):
        queue = self.players.copy()
        self.combat_pairs={}
        while queue != []:
            plyr1 = random.choice(queue)
            queue.remove(plyr1)
            plyr2 = random.choice(queue)
            queue.remove(plyr2)
            self.combat_pairs[plyr1] = plyr2
            self.combat_pairs[plyr2] = plyr1

    # functions for players to call generate a shop
    def generate_shop(self, player):
        if self.turn_counter <= 2:
            shop_size=3
        elif self.turn_counter > 2 and self.turn_counter <= 5:
            shop_size=4
        else:
            shop_size=5
        elig_pool = [i for i in self.char_pool if i.lvl <= player.lvl]
        for i in elig_pool:
            i.zone= 'pool'
        elig_spell_pool = [i for i in self.spells if i.lvl <= player.lvl]
        shop = random.sample(list(elig_pool),shop_size)
        for i in shop:
            self.char_pool.remove(i)
        shop = shop + random.sample(list(elig_spell_pool),1)
        return(shop)
