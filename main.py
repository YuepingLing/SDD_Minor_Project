from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.relativelayout import RelativeLayout
import hashlib
import random

# Set Window size
Window.size = (850, 850)
# Add fonts
LabelBase.register(name='glacial',
                   fn_regular='font/GlacialIndifference-Regular.ttf')
LabelBase.register(name='trocchi',
                   fn_regular='font/Trocchi.ttf')

Builder.load_file('main.kv')
Builder.load_file('shopwindow.kv')
Builder.load_file('cartwindow.kv')

items = (['Anti_Gray', 20, 0],
         ['EnergyBar', 2.5, 0],
         ['EnergyDrink', 5, 0],
         ['FuelBar', 2, 0],
         ['Monster', 5, 0],
         ['Nutrients', 15, 0],
         ['ProteinShake', 20, 0],
         ['PureProtein', 20, 0],
         ['WeightlossShake', 20, 0],
         ['WheyEnergy', 20, 0])


class CustomPopup(Popup):

    def __init__(self, title, button_name):
        self.title = title
        self.button_name = button_name
        super(CustomPopup, self).__init__()

    def get_title(self):
        return self.title

    def get_button_name(self):
        return self.button_name

    def verify(self):
        if self.get_title() == 'Sign In':
            User.sign_in()
            self.dismiss()
        if self.get_title() == 'Sign Up':
            User.sign_up()
            self.dismiss()


sign_in_pop = CustomPopup('Sign In', 'Sign In')
sign_up_pop = CustomPopup('Sign Up', 'Sign Up')


# Class the root window
class RootWindow(Screen):

    @staticmethod
    def open_popup1():
        sign_in_pop.open()

    @staticmethod
    def open_popup2():
        sign_up_pop.open()


class MyScreens(ScreenManager):
    pass


class ShopWindow(Screen):

    def logout(self):
        self.manager.current = 'root_window'

    @staticmethod
    def lucky_draw():
        LuckyDraw().draw()

    @staticmethod
    def add_item():
        for each in items:
            if each[2] > 0:
                cart_window.ids.item_field.add_widget(Label(text=each[0],
                                                            pos_hint={'center_x': .5, 'center_y': .5}))


class CartWindow(Screen):

    def __init__(self, **kwargs):
        super(CartWindow, self).__init__(**kwargs)


class ItemLayout(RelativeLayout):

    def minus_one(self):
        amount = self.ids['amount'].text
        if int(amount) > 0:
            amount = str(int(amount) - 1)
            self.ids['amount'].text = amount
            for each in items:
                if self.name == each[0]:
                    each[2] -= 1

    def plus_one(self):
        amount = self.ids['amount'].text
        amount = str(int(amount) + 1)
        self.ids['amount'].text = amount
        for each in items:
            if self.name == each[0]:
                each[2] += 1


my_screens = MyScreens()
root_window = RootWindow(name='root_window')
my_screens.add_widget(root_window)
shop_window = ShopWindow(name='shop_window')
my_screens.add_widget(shop_window)
cart_window = CartWindow(name='cart_window')
my_screens.add_widget(cart_window)
my_screens.current = 'shop_window'


class User:
    @staticmethod
    def sign_up():
        uname = sign_up_pop.ids['login'].text
        pwd = hashlib.sha256(sign_up_pop.ids['pwd'].text.encode('utf-8'))
        file = open('users.txt', 'a')
        file.write(uname + ' ' + pwd.hexdigest() + '\n')
        file.close()

    @staticmethod
    def sign_in():
        with open('users.txt') as file:
            no_user = True
            check_stat = False
            for lines in file:
                if lines.split(' ')[0] == sign_in_pop.ids['login'].text:
                    if lines.split(' ')[1].rstrip() == \
                            hashlib.sha256(sign_in_pop.ids['pwd'].text.encode('utf-8')).hexdigest():
                        check_stat = True
                    else:
                        Popup(title='Prompt',
                              content=Label(text='Password Incorrect.',
                                            font_size=28),
                              size_hint=(.5, .5)).open()
                    no_user = False
            if no_user:
                Popup(title='Prompt',
                      content=Label(text='User does not exist.',
                                    font_size=28),
                      size_hint=(.5, .5)).open()
        file.close()
        if check_stat:
            my_screens.current = 'shop_window'


class LuckyDraw(Popup):

    def __init__(self, **kwargs):
        super(LuckyDraw, self).__init__(**kwargs)

    def draw(self):
        lucky_item = random.choice(items)[0]
        self.ids.lucky_draw.add_widget(Label(text=lucky_item))
        self.open()


# Build the App
class EnergyMaxApp(App):

    def build(self):
        return my_screens


if __name__ == '__main__':
    EnergyMaxApp().run()
