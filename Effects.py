
class Effect:
    def __init__(self,name, effect_func=None, reverse_effect_func = None, condition = lambda x: True,
        modifier = None):
        self.name = name
        self.effect_func = effect_func
        self.reverse_effect_func = reverse_effect_func
        self.condition = condition
        self.source = None
        self.modifier = modifier

    def add_to_obj(self, obj):
        self.source = obj
        if self.modifier!=None:
            self.modifier.source = obj

    def __repr__(self):
        return self.name

# Effect that modifiers level of treasures a player gets
# Effect is added to a player object's effect attribute
class Treasure_Level_Mod(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier)
        self.type='Treasure Level Modifier'

    def apply_effect(self, base_lvl):
        return self.effect_func(base_lvl)

# Effect that affects a player
# Effect is added to a player object's effect attribute
class Player_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier)
        self.type='Hero Effect'

    def apply_effect(self, source):
        self.effect_func(self, source.owner)
        source.owner.effects.append(self)

    def reverse_effect(self, source):
        self.reverse_effect_func(self, source.owner)
        source.owner.effects.remove(self)

# Effect that provides a support bonus for supporting characters
# Effect is added to a character object's abil attribute
class Support_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier)
        self.type='Support Effect'

    def apply_effect(self, char):
        self.effect_func(char, self.source)

    def reverse_effect(self, char):
        self.reverse_effect_func(char, self.source)

# Effect that occurs on a character's death
# Effect is added to a character object's abil attribute
class Death_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier)
        self.type='Death Effect'

    def apply_effect(self, char):
        self.effect_func(char)

# Effect that affects a character on purchase
# Effect is added to a player's abil attribute
class Purchase_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier)
        self.type='Purchase Effect'

    def apply_effect(self, eff, char):
        self.effect_func(char, eff)

# Static effects that will only affect the character itself and are always
# on regardless of zone
# Effect is added to a character object's abil attribute
class Local_Static_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier)
        self.type='Local Static Effect'

    def add_to_obj(self, obj):
        self.source = obj
        self.apply_effect(obj)

    def apply_effect(self, selfchar):
        self.effect_func(selfchar)

    def reverse_effect(self, selfchar):
        self.reverse_effect_func(selfchar)

# Static effects that will affect all characters a player has (with conditions)
# Effect is added to both a character and player object's effect attribute
class Global_Static_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier)
        self.type='Global Static Effect'
        self.source = None

    def apply_effect(self, obj):
        self.effect_func(obj)

    def reverse_effect(self, obj):
        self.reverse_effect_func(obj)

# effect that modifies objects in a player's shop
# Effect is added to a player's effect attribute. Character's costs/stats are
# modified, but effect is not stored in character's effect attribute
class Shop_Effect(Effect):
    def __init__(self, name:str, char_effect_func = None, char_reverse_effect_func = None,
            spell_effect_func = None, spell_reverse_effect_func=None,
            condition = lambda x: True, modifier= None):
        super().__init__(name, condition, modifier)

        self.effect_func = lambda x: print('wrong effect passed')
        self.reverse_effect_func = lambda x: print('wrong effect passed')

        self.type='Shop Effect'
        self.source = None
        self.char_effect_func = char_effect_func
        self.char_reverse_effect_func = char_reverse_effect_func
        self.spell_effect_func = spell_effect_func
        self.spell_reverse_effect_func = spell_reverse_effect_func

    def apply_effect(self, obj):
        if self.char_effect_func != None and obj.__class__.__name__=='Character' and self.condition(obj):
            self.char_effect_func(obj)
        if self.spell_effect_func != None and obj.__class__.__name__=='Spell' and self.condition(obj):
            self.spell_effect_func(obj)

    def reverse_effect(self, char):
        if self.char_reverse_effect_func != None and obj.__class__.__name__=='Character':
            self.char_reverse_effect_func(obj)
        if self.spell_reverse_effect_func != None and obj.__class__.__name__=='Spell':
            self.spell_reverse_effect_func(obj)


# effect that triggers on a certain condition.
# Effect is added to a player's effect attribute or character's abil attribute,
# depending on the type of trigger.
class Triggered_Effect(Effect):
    def __init__(self, name:str, trigger, effect_func, condition = lambda obj: True,
        counter = None, eob=False):
        super().__init__(name, effect_func, condition = condition)
        self.trigger = trigger
        self.trigger.source = self
        self.effect_func = effect_func
        self.source = None
        self.condition = condition
        self.counter = counter
        self.eob = eob

    def trigger_effect(self):
        if self.condition(self.source):
            self.effect_func(self.source)

    def __repr__(self):
        return self.name


class Quest(Triggered_Effect):
    def __init__(self, name:str, trigger, counter, effect_func = None):
        super().__init__(name, trigger, effect_func)
        self.counter = counter
        self.source = None

    def finish_effect(self):
        self.source.upgraded = True
        self.source.owner.select_treasure(self.source.lvl)

    def trigger_effect(self):
        self.counter -= 1
        if self.counter==0:
            self.finish_effect()

    def __repr__(self):
        return self.name

class Modifier:
    def __init__(self, name:str, atk_func = None, hlth_func=None, oth_func=None,
        oth_reverse_func=None, eob = False):
        self.name = name
        self.source= None
        self.atk_func = atk_func
        self.hlth_func = hlth_func
        self.oth_func = oth_func
        self.oth_reverse_func = oth_reverse_func
        self.eob = eob

    def __repr__(self):
        return self.name

class Trigger:
    def __init__(self, name:str, type, condition= lambda x: True, battle_trigger = True):
        self.name = name
        assert type in ['buy','start of combat','cast','slay','die','attack',
            'start of turn', 'end of turn', 'survive damage']
        # tentative types: buy, start of combat, cast, slay, die, attack, end of turn
        self.type = type
        self.condition = condition
        self.battle_trigger = battle_trigger
        self.source=None

    def __repr__(self):
        return self.name

class Target:

    def __init__(self, name:str, condition = lambda x: True):
        self.name = name
        self.condition = condition
        self.source= None

    def target_select(self):
        legal_targets = []
        for i in self.source.owner.hand:
            if self.condition(i):
                legal_targets.append(i)
        self.source.selected_target = self.source.owner.input_choose(legal_targets)

    def check_for_legal_targets(self, plyr):
        legal_targets = []
        for i in plyr.hand:
            if self.condition(i):
                legal_targets.append(i)
        return len(legal_targets)>0

    def __repr__(self):
        return self.name
