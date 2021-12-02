#import torch
import pickle
from datetime import datetime
import numpy as np

class NN_Logic:

    def __init__(self):
        self.player = None
        self.purchase_toggle = False
        self.models = {}

    def add_to_player(self, player):
        self.player = player
        self.player.logic = self

    def load_model(self, label, filepath):
        self.models[label] = pickle.load(open(filepath, 'rb'))

    def predict_board_win_prob(self, board_record):
        X = list(board_record.values())
        start = datetime.now()
        #predict=self.models['board'](torch.Tensor(x).float().to(torch.device('cuda:0')))
        predict= self.models['board'].predict_proba(np.array([X]))
        print(datetime.now() - start)
        print(self.player.board)
        print('Round',self.player.game.turn_counter)
        print('Predicted win probability:',predict)

        import pdb; pdb.set_trace()
