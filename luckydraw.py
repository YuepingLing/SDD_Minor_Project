import random
from kivy.uix.popup import Popup
from kivy.lang.builder import Builder
from kivy.uix.label import Label

Builder.load_file('luckydraw.kv')

items = ['Anti_Gray', 'EnergyBar', 'EnergyDrink', 'FuelBar', 'Monster',
         'Nutrients', 'ProteinShake', 'PureProtein', 'WeightlossShake', 'WheyEnergy']


class LuckyDraw(Popup):

    def __init__(self, **kwargs):
        super(LuckyDraw, self).__init__(**kwargs)
        self.ids.lucky_draw.add_widget(Label(text=random.choice(items)))
