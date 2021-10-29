from c_Treasure import Treasure

class Effect:
    def __init__(self,name, effect_func=None, reverse_effect_func = None, condition = lambda x: True,
        modifier = None, once_per_turn=False, multi_ignore = False):
        self.name = name
        self.effect_func = effect_func
        self.reverse_effect_func = reverse_effect_func
        self.condition = condition
        self.source = None
        self.modifier = modifier
        self.once_per_turn = once_per_turn
        self.activated_this_turn = False
        # how many times each effect will trigger
        self.multiplier = 1
        self.effects = []
        # If a effect has no effect when multiplied, ignore multiplier changes
        self.multi_ignore = multi_ignore

    def add_to_obj(self, obj):
        self.source = obj
        if self.modifier!=None:
            self.modifier.source = obj
            self.modifier.source_abil = self

    def apply_effect(self, char):
        self.effect_func(char)

    def reverse_effect(self, char):
        self.reverse_effect_func(char)

    def __repr__(self):
        return self.name

# Effect that modifiers level of treasures a player gets
# Effect is added to a player object's effect attribute
class Treasure_Level_Mod(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Treasure Level Modifier'

    def apply_effect(self, base_lvl):
        for _ in range(self.multiplier):
            base_lvl = self.effect_func(base_lvl)
        return base_lvl


class Treasure_Effect_Multiplier(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Treasure Effect Multiplier'

    def apply_effect(self, effect):
        if effect.multi_ignore == False:
            effect.multiplier += 1

    def reverse_effect(self, effect):
        if effect.multi_ignore == False:
            effect.multiplier -= 1

# Effect that affects a player
# Effect is added to a player object's effect attribute
class Player_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
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
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Support Effect'

    def apply_effect(self, char):
        for _ in range(self.multiplier):
            self.effect_func(char, self.source)

    def reverse_effect(self, char):
        self.reverse_effect_func(char, self.source)

# Effect that occurs on a character's death
# Effect is added to a character object's abil attribute
class Last_Breath_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
        self.type='Death Effect'

    def apply_effect(self, char):
        for _ in range(self.multiplier):
            self.effect_func(char)

# Effect that affects a character on purchase
# Effect is added to a player's abil attribute
class Purchase_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, once_per_turn = False
        , multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier,
            once_per_turn, multi_ignore= multi_ignore)
        self.type='Purchase Effect'

    def apply_effect(self, eff, char):
        if self.activated_this_turn == False:
            for _ in range(self.multiplier):
                self.effect_func(char, eff)

        if self.once_per_turn:
            self.activated_this_turn = True

# Static effects that will only affect the character itself and are always
# on regardless of zone
# Effect is added to a character object's abil attribute
class Local_Static_Effect(Effect):
    def __init__(self, name:str, effect_func=None, reverse_effect_func = None,
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
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
        condition = lambda x: True, modifier = None, multi_ignore=False):
        super().__init__(name,effect_func, reverse_effect_func, condition, modifier
            , multi_ignore= multi_ignore)
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
            condition = lambda x: True, modifier= None, multi_ignore=False):
        super().__init__(name, condition, modifier, multi_ignore= multi_ignore)

        self.effect_func = lambda x: print('wrong effect passed')
        self.reverse_effect_func = lambda x: print('wrong effect passed')

        self.type='Shop Effect'
        self.source = None
        self.char_effect_func = char_effect_func
        self.char_reverse_effect_func = char_reverse_effect_func
        self.spell_effect_func = spell_effect_func
        self.spell_reverse_effect_func = spell_reverse_effect_func

    def apply_effect(self, obj):
        for _ in range(self.multiplier):
            if self.char_effect_func != None and obj.__class__.__name__=='Character' and self.condition(obj):
                self.char_effect_func(obj)
            if self.spell_effect_func != None and obj.__class__.__name__=='Spell' and self.condition(obj):
                self.spell_effect_func(obj)

    def reverse_effect(self, char):
        for _ in range(self.multiplier):
            if self.char_reverse_effect_func != None and obj.__class__.__name__=='Character':
                self.char_reverse_effect_func(obj)
            if self.spell_reverse_effect_func != None and obj.__class__.__name__=='Spell':
                self.spell_reverse_effect_func(obj)


# effect that triggers on a certain condition.
# Effect is added to a player's effect attribute or character's abil attribute,
# depending on the type of trigger.
class Triggered_Effect(Effect):
    def __init__(self, name:str, trigger, effect_func, condition = lambda obj: True,
        counter = None, eob=False, multi_ignore=False):
        super().__init__(name, effect_func, condition = condition , multi_ignore=multi_ignore)
        self.trigger = trigger
        self.trigger.source = self
        self.effect_func = effect_func
        self.source = None
        self.condition = condition
        self.counter = counter
        self.eob = eob
        self.activated_this_turn = False

    def trigger_effect(self, effect_kwargs= None):
        if self.counter == None or self.counter <= 0:
            if self.condition(self.source):
                for _ in range(self.multiplier):
                    if effect_kwargs == None:
                        self.effect_func(self.source)
                    else:
                        self.effect_func(self.source, **effect_kwargs)

            # for treasures with counters, remove them when they hit zero
            if self.counter != None and isinstance(self.source, Treasure) \
                and self.source.owner != None:
                self.source.owner.discard_treasure(self.source)

        else:
            self.counter -= 1

    def apply_effect(self, obj):
        self.source = obj
        obj.effects.append(self)
        obj.triggers.append(self.trigger)

    def remove_effect(self, obj):
        self.source = None
        obj.effects.remove(self)
        obj.triggers.remove(self.trigger)

    def __repr__(self):
        return self.name


class Quest(Triggered_Effect):
    def __init__(self, name:str, trigger, counter, effect_func = None, increment = 1
        , multi_ignore=False):
        super().__init__(name, trigger, effect_func , multi_ignore = multi_ignore)
        self.counter = counter
        self.counter_start_val = counter
        self.source = None
        self.increment = increment

    def finish_effect(self):
        self.source.upgraded = True
        self.source.owner.select_treasure(self.source.lvl)

    # args added so the function can handle triggers with effect kwargs
    def trigger_effect(self, *args, **kwargs):
        self.counter -= self.increment
        if self.counter==0:
            self.finish_effect()

    def __repr__(self):
        return self.name

class Modifier:
    def __init__(self, name:str, atk_func = None, hlth_func=None, oth_func=None,
        oth_reverse_func=None, eob = False):
        self.name = name
        self.source= None
        self.source_abil = None
        self.atk_func = atk_func
        self.hlth_func = hlth_func
        self.oth_func = oth_func
        self.oth_reverse_func = oth_reverse_func
        self.eob = eob

    def __repr__(self):
        return self.name

class Trigger:
    def __init__(self, name:str, type, condition= lambda self, condition_obj,
        triggered_obj = None: True, battle_trigger = True):

        '''
        object representing a trigger that needs to be checked for
        params:
        name - name of trigger
        type - type of trigger. influences when this particular trigger is checked for
        condition - a function with three arguments:
            self - this should be the trigger object itself
            condition_obj - the object that caused the trigger to activate. For
            example, for slay triggers, this is the character that slew.
            For many triggers this is just the source of the trigger and often not used.
            triggered_obj - only used by slay triggers triggered. This is the character
            that was slew in that case.
        battle_trigger - boolean for whether a trigger is checked during the battle.
        I think this was never really implemented to do anything.
        '''

        self.name = name
        assert type in ['buy','start of combat','end of combat','cast','purchase'
            ,'slay','die','attack', 'target', 'global slay', # if any char slays
            'start of turn', 'end of turn', 'survive damage','clear front row']
        # make sure type is one of the ones that have been programmed
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
        self.source.owner.check_for_triggers('target', triggering_obj = self.source.selected_target)
        # hard coded hack to get sleeping princess' transform to transfer the
        # target of the spell to the transformed Awakened Princess.
        if self.source.selected_target.name == 'Sleeping Princess':
            # the last object in the owner's hand should be the transformed princess
            assert self.source.owner.hand[-1].name == 'Awakened Princess'
            self.source.selected_target = self.source.owner.hand[-1]


    def check_for_legal_targets(self, plyr):
        legal_targets = []
        for i in plyr.hand:
            if self.condition(i):
                legal_targets.append(i)
        return len(legal_targets)>0

    def __repr__(self):
        return self.name
