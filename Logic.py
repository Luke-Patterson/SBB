
class NN_Logic:

    def __init__(self):
        self.player = None

    def add_to_player(self, player):
        self.player = player
        self.player.logic = self

    def input_choose(self, choices, label):
