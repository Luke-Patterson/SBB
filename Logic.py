import torch
import pickle
from datetime import datetime

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
        x = list(board_record.values())
        start = datetime.now()
        predict=self.models['board'](torch.Tensor(x).float().to(torch.device('cuda:0')))
        print(datetime.now() - start)
        import pdb; pdb.set_trace()
