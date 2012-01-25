'''
Deflectouch

Copyright (C) 2012  Cyril Stoller

For comments, suggestions or other messages, contact me at:
<cyril.stoller@gmail.com>

This file is part of Deflectouch.

Deflectouch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Deflectouch is distributed in the hope that it will be fun,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Deflectouch.  If not, see <http://www.gnu.org/licenses/>.
'''


import kivy
kivy.require('1.0.9')

from kivy.app import App
from kivy.config import Config
# for making screenshots with F12:
Config.set('modules', 'keybinding', '')
#Config.set('modules', 'inspector', '')
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.utils import boundary
from kivy.clock import Clock

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from math import sin
from math import cos
from math import radians

from random import randint


from background import Background
from tank import Tank
from bullet import Bullet
from stockbar import Stockbar


'''
####################################
##
##   GLOBAL SETTINGS
##
####################################
'''

VERSION = '1.0'

LEVEL_WIDTH = 17
LEVEL_HEIGHT = 16

LEVEL_OFFSET = [400, 50]
BRICK_WIDTH = 65


'''
####################################
##
##   Setting Dialog Class
##
####################################
'''
class SettingDialog(BoxLayout):
    music_slider = ObjectProperty(None)
    sound_slider = ObjectProperty(None)
    speed_slider = ObjectProperty(None)
    
    root = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(SettingDialog, self).__init__(**kwargs)
        
        self.music_slider.bind(value=self.update_music_volume)
        self.sound_slider.bind(value=self.update_sound_volume)
        self.speed_slider.bind(value=self.update_speed)
    
    def update_music_volume(self, instance, value):
        # write to app configs
        self.root.app.config.set('General', 'Music', int(value))
        self.root.app.config.write()
    
    def update_sound_volume(self, instance, value):
        # write to app configs
        self.root.app.config.set('General', 'Sound', int(value))
        self.root.app.config.write()
    
    def update_speed(self, instance, value):
        # write to app configs
        self.root.app.config.set('GamePlay', 'BulletSpeed', int(value))
        self.root.app.config.write()
    
    def display_help_screen(self):
        self.root.setting_popup.dismiss()
        self.root.display_help_screen()
    
    def dismiss_parent(self):
        self.root.setting_popup.dismiss()
    

'''
####################################
##
##   Main Widget Class
##
####################################
'''
class DeflectouchWidget(Widget):
    app = ObjectProperty(None)
    version = StringProperty(VERSION)
    
    level = NumericProperty(1)
    lives = NumericProperty(3)
    
    bullet = None
    setting_popup = None
    stockbar = None
    
    deflector_list = []
    obstacle_list = []
    goal_list = []
    
    max_stock = 0
    
    
    '''
    ####################################
    ##
    ##   GUI Functions
    ##
    ####################################
    '''
    def fire_button_pressed(self):
        if self.bullet:
            # if there is already a bullet existing (which means it's flying around or exploding somewhere)
            # don't fire.
            return
        
        # create a bullet, calculate the start position and fire it.
        tower_angle = radians(self.tank.tank_tower_scatter.rotation)
        tower_position = self.tank.pos
        bullet_position = (tower_position[0] + 46 + cos(tower_angle) * 130, tower_position[1] + 75 + sin(tower_angle) * 130)
        self.bullet = Bullet(angle=tower_angle)
        self.bullet.center = bullet_position
        self.add_widget(self.bullet)
        self.bullet.fire()
    
    def reset_button_pressed(self):
        # first kill the bullet
        if self.bullet != None:
            self.remove_widget(self.bullet)
            self.bullet = None
        
        # then delete all the deflectors.
        for deflector in self.deflector_list:
            self.background.delete_deflector(deflector)
        
        # now the user can begin once again with 3 lives:
        self.lives = 3
        
        
    
    def level_button_pressed(self):
        # create a popup with all the levels
        grid_layout = GridLayout(cols=8,rows=5,spacing=10, padding=10)
        
        for counter, char in enumerate(self.app.config.get('GamePlay', 'Levels')):
            button = Button(text=str(counter+1),bold=True,font_size=20)
            button.bind(on_press=self.load_level)
            
            if char == '0':
                button.background_color = (1, 0, 0, 0.5)
            else:
                button.background_color = (0, 1, 0, 0.5)
            
            grid_layout.add_widget(button)
        
        popup = Popup(title='Levels',
                      content=grid_layout,
                      size_hint=(0.5, 0.5))
        popup.open()
    
    def settings_button_pressed(self):
        # the first time the setting dialog is called, initialize its content.
        if self.setting_popup == None:
            
            self.setting_popup = Popup(attach_to=self,
                                       title='DeflecTouch Settings',
                                       size=(400, 400),
                                       size_hint=(None, None))
            
            self.setting_dialog = SettingDialog(root=self)
            
            self.setting_popup.content = self.setting_dialog
        
            self.setting_dialog.music_slider.value = boundary(self.app.config.getint('General', 'Music'), 0, 100)
            self.setting_dialog.sound_slider.value = boundary(self.app.config.getint('General', 'Sound'), 0, 100)
            self.setting_dialog.speed_slider.value = boundary(self.app.config.getint('GamePlay', 'BulletSpeed'), 1, 10)
        
        self.setting_popup.open()
        
    def display_help_screen(self):
        # display the help screen on a Popup
        image = Image(source='graphics/beta/help_screen_beta.png')
        
        help_screen = Popup(title='Quick Guide through DEFLECTOUCH',
                            attach_to=self,
                            size_hint=(0.95, 0.95),
                            content=image)
        image.bind(on_touch_down=help_screen.dismiss)
        help_screen.open()
    
    
    '''
    ####################################
    ##
    ##   Game Play Functions
    ##
    ####################################
    '''
    
    def bullet_died(self):
        self.remove_widget(self.bullet)
        self.bullet = None
        # or should i write del self.bullet instead?
        
        self.lives -= 1
        if self.lives == 0:
            self.reset_button_pressed()
    
    def level_accomplished(self):
        # show up a little image with animation: size*2 and out_bounce and the wait 1 sec
        
        # store score in config:
        levels_before = self.app.config.get('GamePlay', 'Levels')
        levels_before[self.level - 1] = '1'
        self.app.config.set('GamePlay', 'Levels', levels_before)
        self.app.config.write()
        
        # open the level dialog
        self.level_button_pressed()
    
    def load_level(self, level):
        print 'level'
        # First of all, delete the old level:
        for obstacle in self.obstacle_list:
            self.remove_widget(obstacle)
        self.obstacle_list = []
        
        for goal in self.goal_list:
            self.remove_widget(goal)
        self.goal_list = []
        
        if self.stockbar != None:
            self.remove_widget(self.stockbar)
        self.max_stock = 0
        
        
        # i have to check if the function is called by a level button in the level popup OR with an int as argument:
        if not isinstance(level, int):
            level = int(level.text)
        
        self.lives = 3
        self.level = level
        
        # Then load the text file in where the level is stored
        level_image = kivy.core.image.Image.load('levels/level%02d.png' % level, keep_data=True)
        
        for x in range(LEVEL_WIDTH):
            for y in range(1, LEVEL_HEIGHT + 1):
                color = level_image.read_pixel(x, y)
                if len(color) > 3:
                    # if there was transparency stored in the image, cut it.
                    color.pop()
                
                if color == [0, 0, 0]:
                    # create obstacle brick on white pixels
                    image = Image(source=('graphics/beta/brick%d.png' % randint(1, 4)),
                                  x = LEVEL_OFFSET[0] + x * BRICK_WIDTH,
                                  y = LEVEL_OFFSET[1] + y * BRICK_WIDTH,
                                  size = (BRICK_WIDTH, BRICK_WIDTH),
                                  allow_stretch = True)
                    self.obstacle_list.append(image)
                    self.add_widget(image)
                
                elif color == [0, 0, 1]:
                    # create a goal brick on blue pixels
                    image = Image(source=('graphics/beta/goal%d.png' % randint(1, 1)),
                                  x = LEVEL_OFFSET[0] + x * BRICK_WIDTH,
                                  y = LEVEL_OFFSET[1] + y * BRICK_WIDTH,
                                  size = (BRICK_WIDTH, BRICK_WIDTH),
                                  allow_stretch = True)
                    self.goal_list.append(image)
                    self.add_widget(image)
                    
        
        # but in the lowermost row there is also stored the value for the maximum stock 
        for x in range(LEVEL_WIDTH):
            color = level_image.read_pixel(x, 0)
            if len(color) > 3:
                    # if there was transparency stored in the image, cut it.
                    color.pop()
                    
            if color == [1, 0, 0]:
                self.max_stock += 1
        
        # now i set up the stockbar widget:
        self.max_stock = self.max_stock * 1527.0/LEVEL_WIDTH
        self.stockbar = Stockbar(max_stock=self.max_stock,
                                 x=960-self.max_stock/2,
                                 center_y=85)
        self.add_widget(self.stockbar)


Factory.register("Tank", Tank)
Factory.register("Background", Background)
Factory.register("Stockbar", Stockbar)


'''
####################################
##
##   Main Application Class
##
####################################
'''
class Deflectouch(App):
    title = 'Deflectouch'
    icon = 'icon.png'
    
    
    def build(self):
        # print the application informations
        print '\nDeflectouch v%s  Copyright (C) 2012  Cyril Stoller' % VERSION
        print 'This program comes with ABSOLUTELY NO WARRANTY'
        print 'This is free software, and you are welcome to redistribute it'
        print 'under certain conditions; see the source code for details.\n'
        
        # create the root widget and give it a reference of the application instance (so it can access the application settings)
        self.deflectouchwidget = DeflectouchWidget(app=self)
        self.root = self.deflectouchwidget
        
        # continue on the last level who wasn't finished
        for counter, char  in enumerate(self.config.get('GamePlay', 'Levels')):
            # if i found a level not yet done, continue with that
            if char == '0':
                self.deflectouchwidget.load_level(counter + 1)
                break;
        
        # if the user started the game the first time, display quick start guide
        if self.config.get('General', 'FirstStartup') == 'Yes':
            
            Clock.schedule_once(self.welcome_screen, 2)
            
            self.config.set('General', 'FirstStartup', 'No')
            self.config.write()
    
   
    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'Music', '50')
        config.setdefault('General', 'Sound', '80')
        config.setdefault('General', 'FirstStartup', 'Yes')
        
        config.adddefaultsection('GamePlay')
        config.setdefault('GamePlay', 'BulletSpeed', '10')
        config.setdefault('GamePlay', 'Levels', '0000000000000000000000000000000000000000')
    
    def welcome_screen(self, instance):
        self.root.display_help_screen()


if __name__ in ('__main__', '__android__'):
    Deflectouch().run()
    