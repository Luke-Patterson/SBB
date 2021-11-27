from Heroes import *
from Treasures import *
from Characters import *
from Heroes import *
from Player import *
from Spells import *
from copy import deepcopy
from copy import copy
from Data_Collector import Data_Collector
import itertools
import random

class Game_Batch:
    def __init__(self):
        self.data_collector = None
        self.players = []

    def add_data_collector(self, dc):
        self.data_collector = dc

    def clear_players(self):
        self.players = []

    def generate_default_players(self):
        Player0= Player('Player0')
        Player1= Player('Player1')
        Player2= Player('Player2')
        Player3= Player('Player3')
        Player4= Player('Player4')
        Player5= Player('Player5')
        Player6= Player('Player6')
        Player7= Player('Player7')
        self.players=[Player0,Player1,Player2,Player3,Player4,Player5,Player6,Player7]

    # execute a set number of games
    def execute_game_batch(self, num, show_game_num=True, show_runtime = True, **kwargs):
        for n in range(num):
            if show_game_num:
                print('Game',n,'of',num)
            g=Game(**kwargs)
            if self.data_collector != None:
                g.data_collector = self.data_collector
                self.data_collector.game = g
            g.load_objs()

            start = datetime.now()

            self.clear_players()
            self.generate_default_players()
            g.run_game(players=self.players)

            if show_runtime:
                print(datetime.now()-start)


# define class for executing a single game
class Game:
    def __init__(self, verbose_lvl=3, seed=None, treasure_test = False, mimic_test=False):
        self.char_pool=[]
        self.init_char_pool=[]
        self.treasures = []
        self.turn_counter = 0
        self.active_players=[]
        self.all_players=[]
        self.winner = None
        self.verbose_lvl = verbose_lvl
        self.ghosts = []
        self.available_heroes=[]
        self.game_id = 0
        if seed!=None:
            self.seed=seed
            self.seed_specified = True
        else:
            self.seed=random.randint(1,10000000000)
            self.seed_specified = False
        random.seed(self.seed)
        print('Game Seed:', self.seed)
        self.data_collector = None

        # testing params
        self.treasure_test = treasure_test
        self.mimic_test = mimic_test

    def reset_game(self):
        game_id = self.game_id
        data_collector = self.data_collector
        if self.seed_specified:
            self.__init__(self.verbose_lvl, self.seed, self.treasure_test, self.mimic_test)
        else:
            self.__init__(self.verbose_lvl, None, self.treasure_test, self.mimic_test)
        self.game_id = game_id
        self.data_collector = data_collector

        # reset objects
        self.char_pool = self.orig_char_pool.copy()
        for i in self.char_pool:
            old_id = i.id
            i.__init__(i.name, i.type, i.base_atk, i.base_hlth, i.lvl,i.abils,i.keyword_abils,i.alignment,i.token,i.inshop)
            i.id = old_id
            i.game = self
            i.origin = "game copy"
        self.available_heroes = self.all_heroes.copy()
        for i in self.all_heroes:
            i.owner = None

        for i in self.spells:
            i.owner = None
            i.current_cost = i.base_cost
            i.selected_target = None

        self.load_treasures()

    def check_obj_nums(self):
        print('Heroes:', len(self.available_heroes))
        print('Spells:', len(self.spells))
        print('Treasures:', len(self.treasures))
        print('Characters:', len([i for i in self.char_universe if i.id==0]))

    def check_for_missing_objs(self):
        master_list = pd.read_excel('input/Story Book v63.4.xlsx', sheet_name = None)
        master_treasures = master_list['Treasures']['Name']
        master_chars = master_list['Characters']['Name']
        master_spells = master_list['Spells']['Name']
        master_heroes = master_list['Heroes']['Name']

        engine_treasures = [i.name for i in self.treasures]
        engine_chars = [i.name for i in self.char_universe if i.id==0]
        engine_spells = [i.name for i in self.spells]
        engine_heroes = [i.name for i in self.available_heroes]

        print('Missing Heroes:', [i for i in master_heroes if i not in engine_heroes])
        print('Missing Characters:', [i for i in master_chars if i not in engine_chars])
        print('Missing Spells:', [i for i in master_spells if i not in engine_spells])
        print('Missing Treasures:', [i for i in master_treasures if i not in engine_treasures])

    def load_objs(self):
        self.load_hero_list()
        self.load_char_pool()
        self.load_treasures()
        self.load_spells()

    # functions for start of the game.
    def run_game(self,players):
        self.game_id += 1
        # set up initial states
        self.active_players=players
        self.all_players={n: i for n,i in enumerate(players)}
        for n, p in enumerate(self.active_players):
            p.player_id = n
            p.game=self
            for opp in self.active_players:
                if opp != p:
                    p.opponent_history.append(opp)

        # self.check_obj_nums()
        # self.check_for_missing_objs()
        # import pdb; pdb.set_trace()

        # have players select heros
        self.select_heroes_phase()

        # start the turns
        for p in self.active_players:
            p.check_for_triggers('start of game')
        while self.winner==None:
            self.complete_turn()
        if self.verbose_lvl >= 1:
            print(self.winner, 'is the winner!')

    def load_hero_list(self):
        # master_hero_list is from Heroes..py
        self.available_heroes= master_hero_list.copy()
        self.all_heroes= master_hero_list.copy()

    def add_to_char_pool(self, char):
        char.set_zone('pool')
        self.char_pool.append(char)


    def load_char_pool(self):
        # master_char_list is from Characters.py
        self.char_pool=[]
        self.master_char_list=master_char_list
        for char in master_char_list:
            if char.token == False and char.inshop:
                if char.lvl==6:
                    for i in range(10):
                        copy_char = deepcopy(char)
                        copy_char.id = i
                        copy_char.game = self
                        copy_char.origin = "game copy"
                        self.add_to_char_pool(copy_char)
                else:
                    for i in range(15):
                        copy_char = deepcopy(char)
                        copy_char.id = i
                        copy_char.game = self
                        copy_char.origin = "game copy"
                        self.add_to_char_pool(copy_char)
        self.char_universe=copy(self.char_pool)
        self.orig_char_pool=copy(self.char_pool)

    def assign_id(self, char):
        id_num = len([i for i in self.char_universe if i.name==char.name]) + 1
        char.id = id_num


    def load_treasures(self):
        # master_treasure_list is from Treasures.py
        self.treasures=master_treasure_list

    def load_spells(self):
        # master_spell_list is from Treasures.py
        self.spells=master_spell_list

    # each player selects one of four heros
    def select_heroes_phase(self):
        choices = {}
        for p in self.active_players:
            choices[p] = random.sample(self.available_heroes, 4)
            p.choose_hero(choices[p])

            p.life = p.hero.life


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

        for p in self.active_players:
            p.start_of_turn_effects()

    def init_shop_phase(self):
        if self.verbose_lvl>=1:
            print('Entering shop phase')
        for p in self.active_players:
            p.do_shop_phase()
            if self.verbose_lvl>=4:
                print(p,'Hand:',p.hand)
                print(p,'Treasures:',p.treasures)

    def init_battle_phase(self):
        if self.verbose_lvl>=1:
            print('Entering combat')
        for p in self.all_players.values():
            p.deploy_for_battle()

        for p in self.active_players:

            # collect data on what the starting board of each player looks like
            if self.data_collector != None:
                self.data_collector.collect_board_data(p)

        self.pair_opponents()

        # fill in results of combat
        if self.data_collector != None:
            self.data_collector.backfill_combat_results()

    def end_of_turn_effects(self):
        for p in self.active_players:
            p.end_of_turn_effects()
            p.check_for_death()
        for p in self.ghosts:
            p.end_of_turn_effects()
        self.check_for_winner()

    def check_for_winner(self):
        if len(self.active_players)==1:
            self.winner=self.active_players[0]
            self.winner.game_position = 1

            # fill in final position
            if self.data_collector != None:
                self.data_collector.backfill_game_results()

    # ========================Combat Resolution functions======================
    # function to pair opponents
    def pair_opponents(self):
        queue = self.active_players.copy()
        self.combat_pairs={}
        if len(queue) % 2 != 0:
            queue.append(self.ghosts[-1])
        while queue != []:
            plyrA = queue[0]
            queue.remove(plyrA)
            plyrB = [i for i in plyrA.opponent_history if i in queue][0]
            queue.remove(plyrB)
            self.combat_pairs[plyrA] = plyrB
            self.combat_pairs[plyrB] = plyrA
            self.conduct_combat(plyrA, plyrB)

            # note how many rounds it's been since each opponent was last played
            plyrA.opponent_history.remove(plyrB)
            plyrA.opponent_history.append(plyrB)
            plyrB.opponent_history.remove(plyrA)
            plyrB.opponent_history.append(plyrA)

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
            plyrA.last_combat = 'lost'
            plyrB.last_combat = 'won'

        elif pB_loss and not pA_loss:
            life_loss_amt = _life_loss_(plyrB, plyrA)
            plyrB.life_loss(life_loss_amt)
            plyrA.last_combat = 'won'
            plyrB.last_combat = 'lost'

        else:
            plyrA.last_combat = 'draw'
            plyrB.last_combat = 'draw'

        for p in [plyrA,plyrB]:
            p.last_opponent = p.opponent
            p.opponent = None
            p.check_for_triggers('end of combat')
            p.clear_board()
            for char in p.hand:
                char.dmg_taken=0
                char.position=None
                char.last_position = None
                char.eob_atk_mod=0
                char.eob_hlth_mod=0

    def conduct_combat(self, plyrA, plyrB):

        # determine who goes first
        plyrs = [plyrA, plyrB]
        if any([i.name == "Hermes' Boots" for i  in plyrA.treasures]) \
            and any([i.name == "Hermes' Boots" for i  in plyrB.treasures]) == False:
            first_plyr = plyrA
        elif any([i.name == "Hermes' Boots" for i  in plyrB.treasures]) \
            and any([i.name == "Hermes' Boots" for i  in plyrA.treasures]) == False:
            first_plyr = plyrB
        else:
            first_plyr = random.choice([plyrA, plyrB])
        plyrs.remove(first_plyr)
        sec_plyr = plyrs[0]
        plyrs = [plyrA, plyrB]
        #act_plyr = first_plyr


        plyrA.opponent = plyrB
        plyrB.opponent = plyrA

        if self.verbose_lvl >=2:
            print(plyrA,'fighting',plyrB)
            print(plyrA,'board:',plyrA.board)
            print(plyrA,'treasures:',plyrA.treasures)
            print(plyrB,'board:',plyrB.board)
            print(plyrB,'treasures:',plyrB.treasures)

        # for p in plyrs:
        #     p.check_for_triggers('start of combat')
        self.check_for_simult_triggers('start of combat', first_plyr, sec_plyr)

        for p in plyrs:
            p.check_effects()


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
                raise Exception('over 1000 combat loops, possible hole in combat loop detection')

        self.end_combat(plyrA,plyrB)

    def check_for_end_of_combat(self, plyrA, plyrB):
        result = False
        if all([i==None for i in plyrA.board.values()]) or all([i==None for i in plyrB.board.values()]):
            result = True
        elif all([i.atk()<=0 for i in plyrA.board.values() if i!=None]) and all([i.atk()<=0 for i in plyrB.board.values() if i!=None]):
            result = True

        # corner case for when soltek ancient is blocking daamge from a flying unit perpetually
        else:
            # check if one side has all 0 atk creatures
            break_combat = False
            for p in [plyrA, plyrB]:
                if p == plyrA:
                    opp_p = plyrB
                else:
                    opp_p = plyrA
                all_zero = all([i.atk()<=0 for i in p.board.values() if i!=None])

                # if so, verify they are all covered by soltek ancient and there's only flying units on the other side
                if all_zero:

                    def _soltak_ancient_check(char):
                        check_pos_map = {5:[1,2], 6:[2,3],7:[3,4]}
                        sresult = False
                        if char.position in check_pos_map.keys():
                            for i in check_pos_map[char.position]:
                                if char.get_owner().board[i] != None and char.get_owner().board[i].name =='Soltak Ancient':
                                    sresult = True
                        return sresult

                    soltek_covers = []
                    all_soltek = False
                    backrow = []
                    for m in range(5,8):
                        if p.board[m] != None:
                            backrow.append(p.board[m])
                            if _soltak_ancient_check(p.board[m]):
                                soltek_covers.append(p.board[m])
                    if soltek_covers == backrow and soltek_covers!=[]:
                        all_soltek=True

                        all_opp_flying = False
                        if all([(i.flying) or (i.atk()<=0) for i in opp_p.board.values() if i != None]):
                            all_opp_flying = True
                            break_combat = True

            if break_combat:
                result = True

        return result

    # function for checking simultaneous triggers between both players
    def check_for_simult_triggers(self, type, plyr1, plyr2):

        # define an object that sets the order of priority for each trigger
        # lower number = resolves sooner.
        if type == 'start of combat':
            trigger_priority = {
                'Ambrosia Effect trigger':1,
                'Fallen Angel atk check trigger':1,
                'Fallen Angel hlth check trigger':1,
                'Shrivel Effect trigger':2,
                'Ivory Owl trigger':3,
                'Lordy trigger':3,
                'Prince Arthur trigger':3,
                'Heartwood Elder Buff trigger':3,
                'Ashwood Elm trigger':4,
                'Shoulder Faeries trigger':5,
                'Robin Wood trigger':6,
                'Helm of the Ugly Gosling Effect trigger':6,
                'The Round Table trigger':7,
                'other heroes': 8,
                'other chars': 9,
                'other treasures':10,
                'other spells':11,
                'Lightning Dragon triggered effect':12
            }

        plyr1_triggers = [i for i in plyr1.triggers if i.type == type]
        plyr2_triggers = [i for i in plyr2.triggers if i.type == type]


        # assign priority to triggers
        plyr1_priority = {}
        plyr2_priority = {}

        for trig in plyr1_triggers:
            if trig.name in trigger_priority.keys():
                plyr1_priority[trig] = trigger_priority[trig.name]

            # set default priority if not specifically named
            elif isinstance(trig.source.source, Character):
                plyr1_priority[trig] = trigger_priority['other chars']
            elif isinstance(trig.source.source, Treasure):
                plyr1_priority[trig] = trigger_priority['other treasures']
            elif isinstance(trig.source.source, Hero):
                plyr1_priority[trig] = trigger_priority['other heroes']
            elif isinstance(trig.source.source, Player):
                plyr1_priority[trig] = trigger_priority['other spells']

        for trig in plyr2_triggers:
            if trig.name in trigger_priority.keys():
                plyr2_priority[trig] = trigger_priority[trig.name]

            # set default priority if not specifically named
            elif isinstance(trig.source.source, Character):
                plyr2_priority[trig] = trigger_priority['other chars']
            elif isinstance(trig.source.source, Treasure):
                plyr2_priority[trig] = trigger_priority['other treasures']
            elif isinstance(trig.source.source, Hero):
                plyr2_priority[trig] = trigger_priority['other heroes']
            elif isinstance(trig.source.source, Player):
                plyr2_priority[trig] = trigger_priority['other spells']

        # make sure we've assigned a priority to all triggers
        assert len(plyr1_triggers) == len(plyr1_priority.keys())
        assert len(plyr2_triggers) == len(plyr2_priority.keys())

        # invert priority dictionary values and keys
        plyr1_inv_priority = {}
        for k, v in plyr1_priority.items():
            if v not in plyr1_inv_priority.keys():
                plyr1_inv_priority[v] = []
            plyr1_inv_priority[v].append(k)

        plyr2_inv_priority = {}
        for k, v in plyr2_priority.items():
            if v not in plyr2_inv_priority.keys():
                plyr2_inv_priority[v] = []
            plyr2_inv_priority[v].append(k)

        # resolve triggers in each priority level in order
        for i in range(1, max(trigger_priority.values())+1):
            if i in plyr1_inv_priority.keys():
                plyr1.resolve_triggers(type, plyr1_inv_priority[i])
            if i in plyr2_inv_priority.keys():
                plyr2.resolve_triggers(type, plyr2_inv_priority[i])

    # functions for players to call generate a shop
    def generate_shop(self, player, first_shop = False):
        # reminder: Masquerade Ball has a lot of similar code, modifications
        # here may need to be carried over there
        if self.turn_counter <= 2:
            shop_size=3
        elif self.turn_counter > 2 and self.turn_counter <= 5:
            shop_size=4
        else:
            shop_size=5
        if any([i.name == 'Staff of the Old Toad' for i in player.treasures]):
            if player.lvl<=3:
                elig_pool = [i for i in self.char_pool if i.lvl == player.lvl]
            else:
                elig_pool = [i for i in self.char_pool if i.lvl <= player.lvl and i.lvl>=4]
        else:
            elig_pool = [i for i in self.char_pool if i.lvl <= player.lvl]

        # remove any quest characters that a player has already gotten this game
        elig_pool = [i for i in elig_pool if i.name not in player.quest_chars_gained]

        elig_spell_pool = [i for i in self.spells if i.lvl <= player.lvl]

        # hardcoded Pied Piper shop effect
        if player.hero.name == 'Pied Piper':
            elig_animals = [i for i in self.char_pool if i.lvl <= player.lvl and
                'Animal' in i.type]

            if any([i.name == 'Staff of the Old Toad' for i in player.treasures]):
                if player.lvl<=3:
                    elig_animals = [i for i in elig_animals if i.lvl == player.lvl]
                else:
                    elig_animals = [i for i in elig_animals if i.lvl <= player.lvl and i.lvl>=4]

            selected = random.choice(elig_animals)
            selected.owner = player
            selected.change_atk_mod(1)
            selected.change_hlth_mod(1)
            elig_pool.remove(selected)
            shop = [selected] + random.sample(list(elig_pool),shop_size)
        else:
            shop = random.sample(list(elig_pool),shop_size)

        # hard coding peter pants having a lvl 2 character in first turn's shop
        if self.turn_counter == 1 and player.hero.name == 'Peter Pants' and first_shop:
            elig_pool = [i for i in self.char_pool if i.lvl==2 and i not in shop]
            selected = random.choice(elig_pool)
            shop.remove(shop[0])
            shop.append(selected)

        for i in shop:
            self.char_pool.remove(i)
            i.owner = player
            i.set_zone('shop')
        if player.check_spells_in_shop():
            spell_count = 1
            if player.hero.name == 'Potion Master':
                spell_count = 2
            shop = shop + random.sample(list(elig_spell_pool),spell_count)
            #assert len([i for i in shop if isinstance(i, Spell)])<=1
        return(shop)

    def generate_partial_shop(self, player):
        # reminder: Masquerade Ball has a lot of similar code, modifications
        # here may need to be carried over there
        if self.turn_counter <= 2:
            shop_size=3
        elif self.turn_counter > 2 and self.turn_counter <= 5:
            shop_size=4
        else:
            shop_size=5
        if any([i.name == 'Staff of the Old Toad' for i in player.treasures]):
            if player.lvl<=3:
                elig_pool = [i for i in self.char_pool if i.lvl == player.lvl]
            else:
                elig_pool = [i for i in self.char_pool if i.lvl <= player.lvl and i.lvl>=4]
        else:
            elig_pool = [i for i in self.char_pool if i.lvl <= player.lvl]

        # remove any quest characters that a player has already gotten this game
        elig_pool = [i for i in elig_pool if i.name not in player.quest_chars_gained]

        elig_spell_pool = [i for i in self.spells if i.lvl <= player.lvl]
        addl_char_num = max(0, shop_size - len([i for i in player.shop if isinstance(i, Character)]))

        # hardcoded Pied Piper shop effect
        if player.hero.name == 'Pied Piper':
            elig_animals = [i for i in self.char_pool if i.lvl <= player.lvl and
                'Animal' in i.type]

            if any([i.name == 'Staff of the Old Toad' for i in player.treasures]):
                if player.lvl<=3:
                    elig_animals = [i for i in elig_animals if i.lvl == player.lvl]
                else:
                    elig_animals = [i for i in elig_animals if i.lvl <= player.lvl and i.lvl>=4]

            selected = random.choice(elig_animals)
            elig_pool.remove(selected)
            if addl_char_num > 0:
                addl_shop = [selected]
                selected.owner = player
                selected.change_atk_mod(1)
                selected.change_hlth_mod(1)
                if addl_char_num > 1:
                    addl_shop = addl_shop + random.sample(list(elig_pool),addl_char_num - 1)
            else:
                addl_shop = random.sample(list(elig_pool),addl_char_num)
        else:
            addl_shop = random.sample(list(elig_pool),addl_char_num)
        for i in addl_shop:
            self.char_pool.remove(i)
            i.owner = player
            i.set_zone('shop')

        if player.check_spells_in_shop():
            spell_count = 1
            if player.hero.name == 'Potion Master':
                spell_count = 2
            spell_count = spell_count - len([i for i in player.shop if isinstance(i, Spell)])
            if spell_count > 0:
                addl_shop = addl_shop + random.sample(list(elig_spell_pool),spell_count)

        return(addl_shop)
