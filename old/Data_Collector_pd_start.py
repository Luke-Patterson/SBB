import pandas as pd
import pickle
import numpy as np

# matrix with labels for the columns
# class Labeled_Matrix:
#     def __init__(self, cols):
#         self.col_labels = {i: n for n,i in enumerate(cols)}
#         self.data = np.array([])

class Data_Collector:

    def __init__(self, game):
        self.position_decision_collect = False
        self.purchase_decision_collect = False
        self.board_collect = False
        self.game = game
        self.board_features = {}
        self.current_turn_data = {}
        self.current_game_data = {}
        self.all_data = {}


    # start collecting data on the starting board of each combat
    def init_board_collect(self):
        self.board_collect = True

        self.board_features['all'] = []

        # define features related to each character
        self.board_features['char'] = []
        self.board_features['position'] = []

        for char in self.game.master_char_list:
            if char.token == False and char.inshop:

                # add column indicating presence of character on the board.
                self.board_features['all'].append('Char_'+char.name)
                self.board_features['char'].append('Char_'+char.name)

                # add position indicating the position of the chars
                for n in range(1,8):
                    self.board_features['all'].append('Position'+str(n) +'_'+char.name)
                    self.board_features['position'].append('Position'+str(n) +'_'+char.name)

        # features indicating whether player is each hero
        self.board_features['hero'] = []
        for hero in self.game.all_heroes:
            self.board_features['all'].append('Hero_'+hero.name)
            self.board_features['hero'].append('Hero_'+hero.name)

        # features indicating whether player has each treasure
        self.board_features['treasure'] = []
        for treasure in self.game.treasures:
            self.board_features['all'].append('Treasure_'+treasure.name)
            self.board_features['treasure'].append('Treasure_'+treasure.name)

        # turn counter
        self.board_features['all'].append('turn_num')

        # index values
        self.board_features['index_cols'] = ['player_id','game_id']

        # outcomes tracked
        self.board_features['outcome_cols'] = ['Final_Position_'+str(n) for n in range(1,9)] \
            +['Final_Position_numeric','battle_not_lost']


        self.all_data['board'] = pd.DataFrame(columns = self.board_features['index_cols'] +
            self.board_features['all'] + self.board_features['outcome_cols'])

        self.current_turn_data['board'] = pd.DataFrame()
        self.current_game_data['board'] = pd.DataFrame()

    # collect data from the board of current player
    def collect_board_data(self, player):

        # note board and position of each char
        if self.board_collect:
            # start dictionaries
            board_record = {'player_id':player.player_id, 'game_id':self.game.game_id}
            board_record_addl = {k: 0 for k in self.board_features['all']}
            board_record.update(board_record_addl)
            import pdb; pdb.set_trace()
            for pos, char in player.board.items():
                if char != None:
                    board_record['Char_'+char.name] = 1
                    board_record['Position'+str(pos)+'_'+char.name] = 1

            # note which hero the player is
            board_record['Hero_'+player.hero.name] = 1

            # note which treasures the player has
            for t in player.treasures:
                board_record['Treasure_'+t.name] = 1

            board_record['turn_num'] = self.game.turn_counter

            self.current_turn_data['board'] = np.append(self.current_turn_data['board'],
                board_record)



    # backfill whether combat was lost or not for each of the turn's results
    def backfill_combat_results(self):
        for rec in self.current_turn_data['board']:
            player = self.game.all_players[rec['player_id']]
            battle_not_lost = player.last_combat != 'lost'
            rec['battle_not_lost'] = battle_not_lost
        self.current_game_data['board'] = np.append(self.current_game_data['board'], self.current_turn_data['board'])
        self.current_turn_data['board'] = np.array([])

    # backfill which position each player finished in
    def backfill_game_results(self):
        for rec in self.current_game_data['board']:
            player = self.game.all_players[rec['player_id']]
            for i in range(1,9):
                if player.game_position == i:
                    rec['Final_Position_'+str(i)] = 1
                else:
                    rec['Final_Position_'+str(i)] = 0
            rec['Final_Position_numeric'] = player.game_position
        self.all_data['board'].data = np.append(self.all_data['board'].data, self.current_game_data['board'])
        self.current_game_data['board'] = np.array([])

    # export data as a pickled np matrix and or csv
    def export_data(self, data_type, filename = 'test_output', folder = 'output/', pickle_fmt = True, csv_fmt = False):
        # convert array of dictionaries to array of arrays
        df = pd.DataFrame([i.values() for i in self.all_data[data_type].data])
        raw_data = df.values
        import pdb; pdb.set_trace()
        # save as pickle
        if pickle_fmt:
            pickle.dump(self.all_data[data_type].data, open(folder+ filename+"_data.p", "wb" ) )
            pickle.dump(self.all_data[data_type].col_labels, open( folder + filename+"_column_names.p", "wb" ) )

        # save as csv
        if csv_fmt:
            df = pd.DataFrame(columns=self.all_data[data_type].col_labels.keys())
            df = df.append(pd.DataFrame(self.all_data[data_type].data))
            import pdb; pdb.set_trace()

            df.columns = self.all_data[data_type].col_labels.values()

            df.to_csv(folder+filename+'.csv')
