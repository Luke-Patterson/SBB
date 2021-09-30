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
    def __init__(self, verbose_lvl=3, seed=None):
        self.char_pool=[]
        self.treasures = []
        self.turn_counter = 0
        self.players=[]
        self.winner = None
        self.verbose_lvl = verbose_lvl
        self.ghosts = []
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
        print(self.winner, 'is the winner!')

    def load_hero_list(self):
        # master_hero_list is from Heroes..py
        self.available_heroes= master_hero_list.copy()

    def load_char_pool(self):
        # master_char_list is from Characters.py
        self.char_pool=[]
        for char in master_char_list:
            if char.lvl==6:
                for i in range(10):
                    copy = deepcopy(char)
                    copy.id = i
                    copy.game = self
                    self.char_pool.append(copy)
            else:
                for i in range(15):
                    copy = deepcopy(char)
                    copy.id = i
                    copy.game = self
                    self.char_pool.append(copy)

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
        if self.verbose_lvl>=1:
            print('Entering shop phase')
        for p in self.players:
            p.do_shop_phase()

    def init_battle_phase(self):
        if self.verbose_lvl>=1:
            print('Entering combat')
        for p in self.players:
            p.deploy_for_battle()
        self.pair_opponents()

    def end_of_turn_effects(self):
        for p in self.players:
            p.end_of_turn_effects()
            p.check_for_death()
        self.check_for_winner()

    def check_for_winner(self):
        if len(self.players)==1:
            self.winner=self.players[0]

    # ========================Combat Resolution functions======================
    # function to pair opponents
    # TODO: currently randomly selects opponents. Need to adjust to match SBB algo
    def pair_opponents(self):
        queue = self.players.copy()
        self.combat_pairs={}
        if len(queue) % 2 != 0:
            queue.append(self.ghosts[-1])
        while queue != []:
            plyrA = random.choice(queue)
            queue.remove(plyrA)
            plyrB = random.choice(queue)
            queue.remove(plyrB)
            self.combat_pairs[plyrA] = plyrB
            self.combat_pairs[plyrB] = plyrA
            self.conduct_combat(plyrA, plyrB)


    def end_combat(self,plyrA,plyrB):
        pA_loss = plyrA.check_for_empty_board()
        pB_loss = plyrB.check_for_empty_board()
        def _life_loss_(loser, winner):
            char_count = len([i for i in winner.board.values() if i!=None and i.upgraded==False])
            upgr_char_count = len([i for i in winner.board.values() if i!=None and i.upgraded==True])
            life_loss = plyrB.lvl + char_count + 3 * upgr_char_count
            return life_loss

        if pA_loss and not pB_loss:
            life_loss_amt = _life_loss_(plyrA, plyrB)
            plyrA.life_loss(life_loss_amt)
        if pB_loss and not pA_loss:
            life_loss_amt = _life_loss_(plyrB, plyrA)
            plyrB.life_loss(life_loss_amt)

        for p in [plyrA,plyrB]:
            p.opponent = None
            p.clear_board()
            for char in p.hand:
                char.dmg_taken=0
                char.position=None

    def conduct_combat(self, plyrA, plyrB):


        # determine who goes first
        plyrs = [plyrA, plyrB]
        if Hermes_Boots in plyrA.treasures and Hermes_Boots not in plyrB.treasures:
            first_plyr = plyrA
        elif Hermes_Boots in plyrB.treasures and Hermes_Boots not in plyrA.treasures:
            first_plyr = plyrB
        else:
            first_plyr = random.choice([plyrA, plyrB])
        plyrs.remove(first_plyr)
        sec_plyr = plyrs[0]
        #act_plyr = first_plyr

        for p in plyrs:
            p.check_for_triggers('start of combat')

        plyrA.opponent = plyrB
        plyrB.opponent = plyrA

        if self.verbose_lvl >=2:
            print(plyrA,'fighting',plyrB)
            print(plyrA,'board:',plyrA.board)
            print(plyrA,'treasures:',plyrA.treasures)
            print(plyrB,'board:',plyrB.board)
            print(plyrB,'treasures:',plyrB.treasures)
        # check to see if combat starts
        if self.check_for_end_of_combat(plyrA,plyrB):
            self.end_combat(plyrA,plyrB)
            return

        def _find_next_unit(active_char,plyr):
            # make sure there isn't an empty board
            assert any([i!=None for i in plyr.board.values()])
            # check if it's all zero attack board
            all_zero_board = all([i.atk()<=0 for i in plyr.board.values() if i!=None])
            start_val = active_char
            first_loop = True
            while True:
                # skip to next position if position is empty. Will also skip over
                # zero attack units if there is a non-zero atk unit somewhere
                if plyr.board[active_char]==None or (plyr.board[active_char].atk()<=0
                    and all_zero_board==False):
                    if active_char == 7:
                        active_char = 1
                    else:
                        active_char += 1
                else:
                    break
                # if we've checked all positions but there still no eligible attacker, keep the same
                if active_char == start_val and first_loop==False:
                    break

            return active_char

        # note active position (position to attack next)
        active_char_1st = _find_next_unit(1, first_plyr)
        active_char_2nd = _find_next_unit(1, sec_plyr)

        # objects to track whose attacking next
        last_atk_1st_p = None
        last_atk_2nd_p = None

        # make first attack
        last_atk_1st_p = first_plyr.board[active_char_1st]
        first_plyr.board[active_char_1st].make_attack()

        self.combat_check_counter=0
        # exchange attacks until someone loses their entire board
        while True:
            self.combat_check_counter +=1
            # make sure combat hasn't ended
            if self.check_for_end_of_combat(first_plyr,sec_plyr):
                break

            # adjust second player's next attacker based on results
            # first, if empty, find the next unit
            if sec_plyr.board[active_char_2nd] == None:
                active_char_2nd = _find_next_unit(active_char_2nd, sec_plyr)

            # if not, see if it's the same as the last unit that attacked
            # if it is not the same unit, that same space will attack again
            elif sec_plyr.board[active_char_2nd] != last_atk_2nd_p:
                pass
            # if it is the same unit, find the next unit
            else:
                # wrap around the board if we're at position 7
                if active_char_2nd == 7:
                    active_char_2nd =0
                active_char_2nd = _find_next_unit(active_char_2nd + 1, sec_plyr)

            # second player attacks
            last_atk_2nd_p = sec_plyr.board[active_char_2nd]
            sec_plyr.board[active_char_2nd].make_attack()

            # repeat for first player's next attacker
            # make sure combat hasn't ended
            if self.check_for_end_of_combat(first_plyr,sec_plyr):
                break

            # adjust second player's next attacker based on results
            # first, if empty, find the next unit
            if first_plyr.board[active_char_1st] == None:
                active_char_1st = _find_next_unit(active_char_1st, first_plyr)
            # if not, see if it's the same as the last unit that attacked
            # if it is not the same unit, that same space will attack again
            elif first_plyr.board[active_char_1st] != last_atk_1st_p:
                pass
            # if it is the same unit, find the next unit
            else:
                # wrap around the board if we're at position 7
                if active_char_1st == 7:
                    active_char_1st =0
                active_char_1st = _find_next_unit(active_char_1st + 1, first_plyr)

            # first player attacks
            last_atk_1st_p = first_plyr.board[active_char_1st]
            first_plyr.board[active_char_1st].make_attack()

            if self.combat_check_counter >= 1000:
                raise 'over 1000 combat loops, possible hole in combat loop detection'

        self.end_combat(plyrA,plyrB)

    # TODO: make this check for only 0 power creatures left as well.
    def check_for_end_of_combat(self, plyrA, plyrB):
        result = False
        if all([i==None for i in plyrA.board.values()]) or all([i==None for i in plyrB.board.values()]):
            result = True
        elif all([i.atk()<=0 for i in plyrA.board.values() if i!=None]) and all([i.atk()<=0 for i in plyrB.board.values() if i!=None]):
            result = True
        return result

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
            i.owner = player
        shop = shop + random.sample(list(elig_spell_pool),1)
        assert len([i for i in shop if isinstance(i, Spell)])<=1
        return(shop)
