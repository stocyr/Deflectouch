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
from kivy.base import EventLoop
from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout

from math import sin
from math import cos
from math import radians

from deflector import Deflector
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


'''
####################################
##
##   Background Image Class
##
####################################
'''
class Background(Image):
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        ud = touch.ud
        
        # the first time a touch occures, nothing happens. If a second finger is touching,
        # create a deflector.
        
        # search for a lonely touch
        
        pairing_made = False        
        for search_touch in EventLoop.touches[:]:
            if 'lonely' in search_touch.ud:
                # so here we have a second touch: make a pairing.
                del search_touch.ud['lonely']
                print 'pairing made'
                self.add_widget(Deflector(touch1=search_touch, touch2=touch))
                pairing_made = True
        
        if pairing_made == False:
            # if no second touch was found: tag the current one as 'lonely'
            ud['lonely'] = True
            #print 'lonely touch'



            

'''
####################################
##
##   Main Widget Class
##
####################################
'''
class DeflectouchWidget(FloatLayout):
    app = ObjectProperty(None)
    version = StringProperty(VERSION)
    
    fire_button = ObjectProperty(None)
    reset_button = ObjectProperty(None)
    menu_button = ObjectProperty(None)
    
    
    '''
    ####################################
    ##
    ##   Class Initialisation
    ##
    ####################################
    '''
    def __init__(self, **kwargs):
        super(DeflectouchWidget, self).__init__(**kwargs)
        
        self.background = Background()
        self.add_widget(self.background)
        
        # after we added the background, we have to put the buttons on the top again:
        self.remove_widget(self.fire_button)
        self.add_widget(self.fire_button)
        self.remove_widget(self.reset_button)
        self.add_widget(self.reset_button)
        self.remove_widget(self.menu_button)
        self.add_widget(self.menu_button)
        
        self.rail_image = Image(
            source='graphics/beta/rails_beta.png')
        self.add_widget(self.rail_image)
        
        self.Tank = Tank(pos=(10, 600))
        self.add_widget(self.Tank)
        
    
    '''
    ####################################
    ##
    ##   GUI Functions
    ##
    ####################################
    '''
    def fire_button_pressed(self):
        # create a bullet, calculate the start position and fire it.
        tower_angle = radians(self.Tank.tank_tower_scatter.rotation)
        tower_position = self.Tank.pos
        bullet_position = (tower_position[0] + 46 + cos(tower_angle) * 130, tower_position[1] + 75 + sin(tower_angle) * 130)
        self.bullet = Bullet(angle=tower_angle)
        self.bullet.center = bullet_position
        self.add_widget(self.bullet)
        self.bullet.fire()
    
    def reset_button_pressed(self):
        print 'reset'
    
    def menu_button_pressed(self):
        print 'menu'


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
    


if __name__ in ('__main__', '__android__'):
    Deflectouch().run()
    