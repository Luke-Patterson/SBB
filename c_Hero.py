from copy import deepcopy
from Effects import Player_Effect

class Hero:
    def __init__(self, name:str, abils=None, reverse_abils=None, life=40):
        self.name=name
        self.life=life
        self.abils=abils
        if abils!=None:
            for i in self.abils:
                i.source = self
        self.reverse_abils=reverse_abils
        self.owner=None

    def apply_effects(self):
        if self.abils!=None:
            for abil in self.abils:
                self.owner.effects.append(abil)
                if isinstance(abil, Player_Effect):
                    abil.apply_effect(self)
                if hasattr(abil, 'trigger'):
                    self.owner.triggers.append(abil.trigger)

    def remove_effects(self):
        if self.abils!=None:
            for abil in self.abils:
                self.owner.effects.remove(abil)
                if isinstance(abil, Player_Effect):
                    abil.reverse_effect(self)
                if hasattr(abil, 'trigger'):
                    self.owner.triggers.remove(abil.trigger)

    def __repr__(self):
        return self.name
