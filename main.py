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
from kivy.properties import ObjectProperty, StringProperty
from kivy.factory import Factory

from kivy.uix.image import Image
from kivy.uix.widget import Widget

from math import sin
from math import cos
from math import radians

from random import randint


from background import Background
from tank import Tank
from bullet import Bullet


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
##   Main Widget Class
##
####################################
'''
class DeflectouchWidget(Widget):
    app = ObjectProperty(None)
    version = StringProperty(VERSION)
    
    fire_button = ObjectProperty(None)
    reset_button = ObjectProperty(None)
    menu_button = ObjectProperty(None)
    
    bullet = None
    
    deflector_list = []
    obstacle_list = []
        
    
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
        print 'reset'
    
    def menu_button_pressed(self):
        print 'menu'
        self.load_level()
    
    
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
        # or should i write del self.bullet ?
    
    def load_level(self):
        # First of all, delete the old level:
        for obstacle in self.obstacle_list:
            self.remove_widget(obstacle)
        self.obstacle_list = []
        
        # Then load the text file in where the level is stored
        level_image = kivy.core.image.Image.load('levels/level01.png', keep_data=True)
        
        for x in range(LEVEL_WIDTH):
            for y in range(LEVEL_HEIGHT):
                color = level_image.read_pixel(x, y)
                
                if color == [0, 0, 0, 1]:
                    # create obstacle brick on white pixels
                    image = Image(source=('graphics/beta/brick' + str(randint(1, 4)) + '.png'),
                                  x = LEVEL_OFFSET[0] + x * BRICK_WIDTH,
                                  y = LEVEL_OFFSET[1] + (16-y) * BRICK_WIDTH,
                                  size = (BRICK_WIDTH, BRICK_WIDTH),
                                  allow_stretch = True)
                    self.obstacle_list.append(image)
                    self.add_widget(image)
                
                elif color == [0, 0, 1, 1]:
                    # create a goal brick on blue pixels
                    pass


Factory.register("Tank", Tank)
Factory.register("Background", Background)


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
        return self.deflectouchwidget
    
   
    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'Sound', 'On')
        config.setdefault('General', 'Music', 'On')
        
        config.adddefaultsection('GamePlay')
        config.setdefault('GamePlay', 'BulletSpeed', '10')
    


if __name__ in ('__main__', '__android__'):
    Deflectouch().run()
    