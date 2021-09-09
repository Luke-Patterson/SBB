from Heroes import *
from Treasures import *
from Characters import *
from Heroes import *
from copy import deepcopy
import itertools
import random

class Game:
    def __init__(self):
        self.char_pool=[]
        self.treasures = []
        self.turn_counter = 0
        self.players=[]

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

        import pdb; pdb.set_trace()

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
                self.available_heroes.remove(p)
            unchosen_heroes = p.select_hero(choices[p])
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
        for p in self.players:
            p.start_of_turn_effects()

    def init_shop_phase(self):
        for p in self.players:
            p.do_shop_phase()

    def init_battle_phase(self):
        pass

    def end_of_turn_effects(self):
        for p in self.players:
            p.end_of_turn_effects()

    # functions for players to call generate a shop
    def generate_shop(self, player):
        if self.turn_counter <= 2:
            shop_size=3
        elif self.turn_counter > 2 and self.turn_counter <= 5:
            shop_size=4
        else:
            shop_size=5
        elig_pool = [i for i in self.char_pool if i.lvl <= player.lvl]
        elig_spell_pool = [i for i in self.spells if i.lvl <= player.lvl]
        shop = random.sample(shop_size, elig_pool) + random.sample(1, elig_spell_pool)

        return(shop)
