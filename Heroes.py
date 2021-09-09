

class Hero:
    def __init__(self, name, abils=None, life=40):
        self.life=life
        self.abils=abils

    def __repr__(self):
        return self.name

Celestial_Tiger = Hero(name='Celestial Tiger')
Charon = Hero(name='Charon')
Evella = Hero(name='Evella')
Fallen_Angel = Hero(name='Fallen Angel')
Gepetto = Hero(name='Gepetto')
Grandmother = Hero(name='Grandmother')
Gwen = Hero(name='Gwen')
Hoard_Dragon = Hero(name='Hoard Dragon')
Jacks_Giant = Hero(name='Jack's Giant')
Krampus = Hero(name='Krampus')
Loki = Hero(name='Loki')
Mad_Catter = Hero(name='Mad Catter')
Mask = Hero(name='Mask')
Merlin = Hero(name='Merlin')
Mihri_King_Lion = Hero(name='Mihri, King Lion')
Mordred = Hero(name='Mordred')
Morgan_le_Fay = Hero(name='Morgan le Fay')
Mrs_Claus = Hero(name='Mrs. Claus')
Muerte = Hero(name='Muerte')
Pans_Shadow = Hero(name='Pan's Shadow')
Peter_Pants = Hero(name='Peter Pants')
Pied_Piper = Hero(name='Pied Piper')
Potion_Master = Hero(name='Potion Master')
Beauty = Hero(name='Beauty')
Pup_the_Magic_Dragon = Hero(name='Pup the Magic Dragon')
Sad_Dracula = Hero(name='Sad Dracula')
Sir_Galahad = Hero(name='Sir Galahad')
Skip_the_Time_Skipper = Hero(name='Skip, the Time Skipper')
Snow_Angel = Hero(name='Snow Angel')
The_Cursed_King = Hero(name='The Cursed King')
The_Fates = Hero(name='The Fates')
Trophy_Hunter = Hero(name='Trophy Hunter')
Wonder_Waddle = Hero(name='Wonder Waddle')
Xelhua = Hero(name='Xelhua')

objs=deepcopy(list(locals().keys()))
master_char_list=[]
for i in objs:
    obj=locals()[i]
    if isinstance(obj, Hero):
        master_char_list.append(obj)
