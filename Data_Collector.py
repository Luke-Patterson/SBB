import time
import pandas as pd
import pickle
import scipy.sparse as sp
import numpy as np
from Characters import master_char_list
from Heroes import master_hero_list
from Treasures import master_treasure_list
from Spells import master_spell_list

# matrix with labels for the columns
class Labeled_Matrix:
    def __init__(self, cols):
        self.col_labels = {i: n for n,i in enumerate(cols)}
        self.data = np.array([])

class Data_Collector:

    def __init__(self, game = None):
        self.position_decision_collect = False
        self.purchase_decision_collect = False
        self.board_collect = False
        self.game = game
        self.board_features = {}
        self.current_turn_data = {}
        self.current_game_data = {}
        self.all_data = {}
        self.game_id = 0


    # start collecting data on the starting board of each combat
    def init_board_collect(self):
        self.board_collect = True

        self.board_features['all'] = []

        # define features related to each character
        self.board_features['char'] = []
        self.board_features['position'] = []

        for char in master_char_list:
            if char.token == False:

                # add column indicating presence of character on the board.
                self.board_features['all'].append('Char_'+char.name)
                self.board_features['char'].append('Char_'+char.name)

                # add column indicating whether upgraded character on the board.
                self.board_features['all'].append('Char_upgr_'+char.name)
                self.board_features['char'].append('Char_upgr_'+char.name)

                # add position indicating the position of the chars
                for n in range(1,8):
                    self.board_features['all'].append('Position'+str(n) +'_'+char.name)
                    self.board_features['position'].append('Position'+str(n) +'_'+char.name)

        # features indicating whether player is each hero
        self.board_features['hero'] = []
        for hero in master_hero_list:
            self.board_features['all'].append('Hero_'+hero.name)
            self.board_features['hero'].append('Hero_'+hero.name)

        # features indicating whether player has each treasure
        self.board_features['treasure'] = []
        for treasure in master_treasure_list:
            self.board_features['all'].append('Treasure_'+treasure.name)
            self.board_features['treasure'].append('Treasure_'+treasure.name)

        # features indicating which spells a player has cast this combat
        self.board_features['spell'] = []
        for spell in master_spell_list:
            self.board_features['all'].append('Spell_'+spell.name)
            self.board_features['spell'].append('Spell_'+spell.name)

        # turn counter
        self.board_features['all'].append('turn_num')

        # index values
        self.board_features['index_cols'] = ['player_id','game_id']

        # outcomes tracked
        self.board_features['outcome_cols'] = ['battle_not_lost']+['Final_Position_'+str(n) for n in range(1,9)] \
            +['Final_Position_numeric']


        self.all_data['board'] = Labeled_Matrix(self.board_features['index_cols'] +
            self.board_features['all'] + self.board_features['outcome_cols'])

        self.current_turn_data['board'] = np.array([])
        self.current_game_data['board'] = np.array([])


    # collect data from the board of current player
    def collect_board_data(self, player):

        # note board and position of each char
        if self.board_collect:
            # start dictionaries
            board_record = {'player_id':player.player_id, 'game_id':self.game_id}
            board_record_addl = {k: 0 for k in self.board_features['all']}
            board_record.update(board_record_addl)
            for pos, char in player.board.items():
                if char != None:
                    board_record['Char_'+char.name] = 1
                    board_record['Position'+str(pos)+'_'+char.name] = 1
                    if char.upgraded:
                        board_record['Char_upgr_'+char.name] = 1

            # note which hero the player is
            board_record['Hero_'+player.hero.name] = 1

            # note which treasures the player has
            for t in player.treasures:
                board_record['Treasure_'+t.name] = 1

            for s in player.names_of_spells_this_turn:
                board_record['Spell_'+s] = 1

            board_record['turn_num'] = self.game.turn_counter

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
            self.all_data['board'].data = np.append(self.all_data['board'].data,
                self.current_game_data['board'])
            self.current_game_data['board'] = np.array([])

    # export data as a pickled np matrix and or csv
    def export_data(self, data_type, filename = 'training data '+time.strftime("%Y%m%d-%H%M%S"),
        folder = 'output/', pickle_fmt = True, csv_fmt = False):

        df = pd.DataFrame([i.values() for i in self.all_data[data_type].data])

        # save as pickle
        if pickle_fmt:
            # convert to sparse matrix
            sm = sp.csr_matrix(df.values)
            pickle.dump(sm, open(folder+ filename+"_data.p", "wb" ) )
            pickle.dump(self.all_data[data_type].col_labels, open( folder +
                filename+"_column_names.p", "wb" ) )

        # save as csv
        if csv_fmt:
            df.columns = self.all_data[data_type].col_labels.keys()
            df.to_csv(folder+filename+'.csv', index = False)
