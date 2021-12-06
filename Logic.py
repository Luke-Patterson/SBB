#import torch
import pickle
from datetime import datetime
import numpy as np
import scipy as sp
import pandas as pd
import itertools
import random
import collections

class NN_Logic:

    def __init__(self):
        self.player = None
        self.purchase_toggle = False
        self.models = {}
        self.char_stats={}
        self.load_char_stats()

    def add_to_player(self, player):
        self.player = player
        self.player.logic = self

    def load_model(self, label, filepath):
        self.models[label] = pickle.load(open(filepath, 'rb'))

    def load_char_stats(self, filepath = 'C:/AnacondaProjects/SBB/prod/statistics/output/'):
        self.char_stats['pos_win_rates'] = pd.read_pickle(filepath+'char_position_win_rates.p')
        self.char_stats['turn_win_rates'] = pd.read_pickle(filepath+'char_turn_win_rates.p')
        self.char_stats['pos_win_rates']['wheremax_pos'] = self.char_stats['pos_win_rates']['wheremax_pos'].astype('int')

    def deploy_chars_decision(self):
        start = datetime.now()
        num_chars = len(self.player.hand)
        deploy_num = min((num_chars, 7))
        positions = [i for i in range(1,8)]
        pos_df = self.char_stats['pos_win_rates'].set_index(['char','upgraded'])

        # not doing anything with turn win rate data yet
        # turn_df = self.char_stats['turn_win_rates'].set_index(['char','upgraded'])
        #
        # # win rates in table capped at turn 20
        # if self.player.game.turn_counter > 20:
        #     turn_counter = 20
        # else:
        #     turn_counter = self.player.game.turn_counter
        #
        # turn_idx = [(i.name, i.upgraded, turn_counter) for i in self.player.hand]
        # turn_df = turn_df.loc[chars,:].fillna(0)

        # filter to the characters in hand, and fill any missing values with 0
        pos_idx = [(i.name, i.upgraded) for i in self.player.hand]
        pos_df = pos_df.loc[pos_idx,:]

        # possible to have two or more identical units so need to add a index level
        pos_df['id'] = [i for i in range(1,num_chars+1)]
        pos_df = pos_df.set_index('id', append = True)
        # start with top 7 win rate cards
        pos_df = pos_df.sort_values('max_val', ascending = False)
        select_df = pos_df.iloc[0:deploy_num,:]
        selections = {}
        conflicts = []
        for idx, row in select_df.iterrows():
            if row['wheremax_pos'] not in selections.keys():
                selections[row['wheremax_pos']] = idx
            else:
                conflicts.append(idx)

        # resolve conflicts
        # check to see if remaining positions in good or bad pos columns
        remain_df = pos_df.loc[conflicts]
        remaining_pos = [i for i in range(1,8) if i not in selections.keys()]
        for i in remaining_pos:
            remain_df['in_good'] = remain_df['good_pos'].apply(lambda x: i in x)
            good_cands = remain_df.loc[remain_df['in_good']].index
            # if there are open positions that match with "good pos" candidates,
            # assign one at random
            if len(good_cands) > 0:
                choice = random.choice(good_cands)
                selections[i] = choice
                conflicts.remove(choice)
                remain_df = pos_df.loc[conflicts]

        remain_df = pos_df.loc[conflicts]
        remaining_pos = [i for i in range(1,8) if i not in selections.keys()]
        for i in remaining_pos:
            if conflicts != []:
                remain_df['in_bad'] = remain_df['good_pos'].apply(lambda x: i in x)
                bad_cands = remain_df.loc[remain_df['in_bad']].index
                # if there are open positions that match with "bad pos" candidates,
                # assign one at random from those not in
                choice = random.choice(remain_df.drop(bad_cands).index)
                selections[i] = choice
                conflicts.remove(choice)
                remain_df = pos_df.loc[conflicts]

        assert len(selections.keys()) == deploy_num

        print(datetime.now() - start)

    def predict_board_win_prob(self, board_record):
        X = list(board_record.values())
        start = datetime.now()
        #predict=self.models['board'](torch.Tensor(x).float().to(torch.device('cuda:0')))
        predict= self.models['board'].predict_proba(sp.sparse.csr_matrix(X))
        print(datetime.now() - start)
        print(self.player)
        print(self.player.board)
        print('Round',self.player.game.turn_counter)
        print('Predicted win probability:',predict)
        import pdb; pdb.set_trace()
