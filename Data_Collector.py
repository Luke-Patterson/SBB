import time
import pandas as pd
import pickle
import scipy
import scipy.sparse as sp
import numpy as np
from Characters import master_char_list
from Heroes import master_hero_list
from Treasures import master_treasure_list
from Spells import master_spell_list
from c_Character import Character
from c_Spell import Spell

# matrix with labels for the columns
class Labeled_Matrix:
    def __init__(self, cols):
        self.col_labels = {i: n for n,i in enumerate(cols)}
        self.data = np.array([])

class Data_Collector:

    def __init__(self, game = None, save_interval = None,
        folder = 'output/', csv = False):
        self.board_collect = False
        self.purchased_collect = False
        self.game = game
        self.features = {}
        self.current_turn_data = {}
        self.current_game_data = {}
        self.all_data = {}
        self.game_id = 0
        self.save_interval = save_interval
        self.folder = folder
        self.csv=csv

    # start collecting data on the starting board of each combat
    def init_data_collect(self):
        self.board_collect = True
        self.purchased_collect = True

        # features used by both board and purchase data
        self.features['all_features'] = []

        # board only and purchase only features
        self.features['board_features'] = []
        self.features['purchased_features'] = []

        # further subcategories of features
        self.features['misc']=[]

        # define features related to each character
        self.features['char'] = []
        self.features['position'] = []

        # define purchase features
        self.features['purchased']=[]
        self.features['in_hand']=[]
        self.features['in_shop']=[]

        for char in master_char_list:
            if char.token == False:

                # add column indicating presence of character on the board.
                self.features['board_features'].append('Char_'+char.name)
                self.features['char'].append('Char_'+char.name)

                # add column indicating whether upgraded character on the board.
                self.features['board_features'].append('Char_upgr_'+char.name)
                self.features['char'].append('Char_upgr_'+char.name)

                # add column indicating whether a character was in hand
                self.features['all_features'].append('Char_in_hand_'+char.name)
                self.features['in_hand'].append('Char_in_hand_'+char.name)

                # add column indicating whether an upgraded character was in hand
                self.features['all_features'].append('Char_upgr_in_hand_'+char.name)
                self.features['in_hand'].append('Char_upgr_in_hand_'+char.name)

                # add column indicating whether a character was purchased
                self.features['purchased_features'].append('Char_purchased_'+char.name)
                self.features['purchased'].append('Char_purchased_'+char.name)

                # add column indicating whether a character was in the shop
                self.features['purchased_features'].append('Char_in_shop_'+char.name)
                self.features['in_shop'].append('Char_in_shop_'+char.name)

                # add position indicating the position of the chars
                for n in range(1,8):
                    self.features['board_features'].append('Position'+str(n) +'_'+char.name)
                    self.features['position'].append('Position'+str(n) +'_'+char.name)

        # note whether no character is in the position
        for n in range(1,8):
            self.features['board_features'].append('Position'+str(n) +'_None')
            self.features['position'].append('Position'+str(n) +'_None')

        # features indicating whether player is each hero
        self.features['hero'] = []
        for hero in master_hero_list:
            self.features['all_features'].append('Hero_'+hero.name)
            self.features['hero'].append('Hero_'+hero.name)

        # features indicating whether player has each treasure
        self.features['treasure'] = []
        for treasure in master_treasure_list:
            self.features['all_features'].append('Treasure_'+treasure.name)
            self.features['treasure'].append('Treasure_'+treasure.name)

        # features indicating which spells a player has cast this combat
        self.features['spell'] = []
        for spell in master_spell_list:
            self.features['all_features'].append('Spell_purchased_'+spell.name)
            self.features['spell'].append('Spell_purchased_'+spell.name)

            # add columns for whether
            self.features['purchased_features'].append('Spell_in_shop_'+spell.name)
            self.features['in_shop'].append('Spell_in_shop_'+spell.name)


        # turn counter
        self.features['all_features'].append('turn_num')
        self.features['misc'].append('turn_num')

        # total atk and hlth on board
        self.features['board_features'].append('total_atk')
        self.features['board_features'].append('total_hlth')
        self.features['char'].append('total_atk')
        self.features['char'].append('total_hlth')

        # number of characters in hand
        self.features['purchased_features'].append('char_num_hand')
        self.features['misc'].append('char_num_hand')

        # number of characters in board
        self.features['board_features'].append('char_num_board')
        self.features['char'].append('char_num_board')

        # how much gold is available
        self.features['purchased_features'].append('available_gold')
        self.features['purchased_features'].append('total_gold_this_turn')

        # whether roll was purchased
        self.features['purchased_features'].append('roll_purchased')

        # index values
        self.features['index_cols'] = ['player_id','game_id']

        # outcomes tracked
        self.features['outcome_cols'] = ['battle_not_lost']+['Final_Position_'+str(n) for n in range(1,9)] \
            +['Final_Position_numeric']

        self.all_data['board'] = None
        self.all_data['purchased'] = None

        self.current_turn_data['board'] = np.array([])
        self.current_game_data['board'] = np.array([])
        self.current_turn_data['purchased'] = np.array([])
        self.current_game_data['purchased'] = np.array([])

        self.features['board_cols'] =  self.features['index_cols'] + self.features['board_features'] +\
            self.features['all_features'] + self.features['outcome_cols']

        self.features['purchased_cols'] =  self.features['index_cols'] + self.features['purchased_features'] +\
            self.features['all_features'] + self.features['outcome_cols']


    # collect purchase data from current player
    def collect_purchase_data(self, player, purchase):

        # Note what was in shop, hand, and what purchase was made
        if self.purchased_collect:
            # start a dictionary for the record of the purchase
            purchase_record = {'player_id':player.player_id, 'game_id':self.game_id}
            purchase_record_addl = {k: 0 for k in self.features['purchased_features']
                + self.features['all_features']}
            purchase_record.update(purchase_record_addl)

            # note name of what was purchased
            if isinstance(purchase, Character):
                purchase_record['Char_purchased_'+purchase.name] = 1
            elif isinstance(purchase, Spell):
                purchase_record['Spell_purchased_'+purchase.name] = 1
            elif purchase=='roll':
                purchase_record['roll_purchased']=1

            # note what else was in the shop
            for obj in player.shop:
                if isinstance(obj, Character):
                    purchase_record['Char_in_shop_'+obj.name] = 1
                elif isinstance(obj, Spell):
                    purchase_record['Spell_in_shop_'+obj.name] = 1

            # note what else was in the hand
            for obj in player.hand:
                if obj.upgraded:
                    purchase_record['Char_upgr_in_hand_'+obj.name] = 1
                else:
                    purchase_record['Char_in_hand_'+obj.name] = 1

            # note which hero the player is
            purchase_record['Hero_'+player.hero.name] = 1

            # note which treasures the player has
            for t in player.treasures:
                purchase_record['Treasure_'+t.name] = 1

            # note other characteristics
            purchase_record['turn_num'] = self.game.turn_counter
            purchase_record['char_num_hand'] = len([i for i in player.hand])
            purchase_record['available_gold'] = player.current_gold
            purchase_record['total_gold_this_turn'] = player.total_gold_this_turn

            self.current_turn_data['purchased'] = np.append(self.current_turn_data['purchased'],
                purchase_record)

    # collect data from the board of current player
    def collect_board_data(self, player):

        # note board and position of each char
        if self.board_collect:
            # start dictionaries
            board_record = {'player_id':player.player_id, 'game_id':self.game_id}
            board_record_addl = {k: 0 for k in self.features['board_features'] +
                self.features['all_features']}
            board_record.update(board_record_addl)
            for pos, char in player.board.items():
                if char != None:
                    board_record['Position'+str(pos)+'_'+char.name] = 1
                    if char.upgraded:
                        board_record['Char_upgr_'+char.name] = 1
                    else:
                        board_record['Char_'+char.name] = 1
                else:
                    board_record['Position'+str(pos)+'_None'] = 1


            # note what was in the hand
            for obj in player.hand:
                if obj.upgraded:
                    board_record['Char_upgr_in_hand_'+obj.name] = 1
                else:
                    board_record['Char_in_hand_'+obj.name] = 1

            # note which hero the player is
            board_record['Hero_'+player.hero.name] = 1

            # note which treasures the player has
            for t in player.treasures:
                board_record['Treasure_'+t.name] = 1

            # record what was spells were purchased this turn
            for s in player.purchased_this_turn:
                if isinstance(s, Spell):
                    board_record['Spell_purchased_'+s.name] = 1

            board_record['turn_num'] = self.game.turn_counter
            board_record['char_num_board'] = len([i for i in player.board.values() if i != None])

            board_record['total_atk'] = sum([i.atk() for i in player.board.values() if i != None])
            board_record['total_hlth'] = sum([i.hlth() for i in player.board.values() if i != None])

            self.current_turn_data['board'] = np.append(self.current_turn_data['board'],
                board_record)

    # backfill whether combat was lost or not for each of the turn's results
    def backfill_combat_results(self):
        if self.board_collect:
            for rec in self.current_turn_data['board']:
                player = self.game.all_players[rec['player_id']]
                battle_not_lost = player.last_combat != 'lost'
                rec['battle_not_lost'] = int(battle_not_lost)
            self.current_game_data['board'] = np.append(self.current_game_data['board'],
                self.current_turn_data['board'])
            self.current_turn_data['board'] = np.array([])

        if self.purchased_collect:
            for rec in self.current_turn_data['purchased']:
                player = self.game.all_players[rec['player_id']]
                battle_not_lost = player.last_combat != 'lost'
                rec['battle_not_lost'] = int(battle_not_lost)
            self.current_game_data['purchased'] = np.append(self.current_game_data['purchased'],
                self.current_turn_data['purchased'])
            self.current_turn_data['purchased'] = np.array([])


    # backfill which position each player finished in
    def backfill_game_results(self):
        self.game_id += 1
        if self.board_collect:
            for rec in self.current_game_data['board']:
                player = self.game.all_players[rec['player_id']]
                for i in range(1,9):
                    if player.game_position == i:
                        rec['Final_Position_'+str(i)] = 1
                    else:
                        rec['Final_Position_'+str(i)] = 0
                rec['Final_Position_numeric'] = player.game_position

            # convert current_game_data into a sparse matrix and append to all data
            df = pd.DataFrame([i.values() for i in self.current_game_data['board']])
            raw_data = sp.csr_matrix(df.values)
            if self.all_data['board'] == None:
                self.all_data['board'] = raw_data
            else:
                self.all_data['board'] = scipy.sparse.vstack([self.all_data['board'],
                    raw_data])

            self.current_game_data['board'] = np.array([])

            if self.save_interval != None and self.game_id % self.save_interval == 0:
                self.export_data('board')

        if self.purchased_collect:
            for rec in self.current_game_data['purchased']:
                player = self.game.all_players[rec['player_id']]
                for i in range(1,9):
                    if player.game_position == i:
                        rec['Final_Position_'+str(i)] = 1
                    else:
                        rec['Final_Position_'+str(i)] = 0
                rec['Final_Position_numeric'] = player.game_position

            # convert current_game_data into a sparse matrix and append to all data
            df = pd.DataFrame([i.values() for i in self.current_game_data['purchased']])
            raw_data = sp.csr_matrix(df.values)
            if self.all_data['purchased'] == None:
                self.all_data['purchased'] = raw_data
            else:
                self.all_data['purchased'] = scipy.sparse.vstack([self.all_data['purchased'],
                    raw_data])

            self.current_game_data['purchased'] = np.array([])

            if self.save_interval != None and self.game_id % self.save_interval == 0:
                self.export_data('purchased')


    # export data as a pickled np matrix and or csv
    def export_data(self, data_type, drop = True,filename = None):
        if filename == None:
            filename='training data '+time.strftime("%Y%m%d-%H%M%S")
        assert data_type in ['purchased','board']
        pickle.dump(self.all_data[data_type], open(self.folder+
            filename+"_"+data_type+"_data.p", "wb" ) )

        pickle.dump(self.features, open( self.folder +
            filename+"_"+data_type+"_column_names.p", "wb" ) )

        # save as csv
        if self.csv:
            df = pd.DataFrame.sparse.from_spmatrix(self.all_data[data_type])
            df.columns = self.features[data_type+"_cols"]
            df.to_csv(self.folder+filename+'_'+data_type+'.csv', index = False)

        if drop == True:
            self.all_data[data_type] = None
