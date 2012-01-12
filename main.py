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
from kivy.graphics.transformation import Matrix

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter

from deflector import Deflector

from math import radians
from math import atan2
from math import pi


'''
####################################
##
##   GLOBAL SETTINGS
##
####################################
'''

VERSION = '1.0'

# Graphics
# ---------------------------------------------------------


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
                Deflector(touch1=ud, touch2=search_touch.ud)
                pairing_made = True
                print 'pairing made'
        
        if pairing_made == False:
            # if no second touch was found: tag the current one as 'lonely'
            ud['lonely'] = True
            print 'lonely touch'


'''
####################################
##
##   Tank Class
##
####################################
'''
class Tank(Scatter):
    tank_image = ObjectProperty(None)
    tank_tower_scatter = ObjectProperty(None)
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        print self.bbox
        if not self.collide_point(*touch.pos):
            return False
        else:
            return super(Tank, self).on_touch_down(touch)
        
        
    
    '''
    ####################################
    ##
    ##   On Touch Move
    ##
    ####################################
    '''
    def on_touch_move(self, touch):
        ud = touch.ud
        
        # Here comes the calculation for the tower-rotating
        if 'tank_position' in ud:
            # if the current touch is already in the 'rotate' mode, rotate the tower.
            dx = touch.x - (ud['tank_position'][0] + 46)    # +46 -> the reference point is in the middle of the tank image.
            dy = touch.y - (ud['tank_position'][1] + 75)    # +75 -> the reference point is in the middle of the tank image.
            angle = kivy.utils.boundary(atan2(dy, dx) * 360 / 2 / pi, -60, 60)
            
            angle_change = self.tank_tower_scatter.rotation - angle
            rotation_matrix = Matrix().rotate(-radians(angle_change), 0, 0, 1)
            self.tank_tower_scatter.apply_transform(rotation_matrix, post_multiply=True, anchor=(98, 38))
            
            #self.tank_tower_scatter.rotation = angle
            #self.tank_tower_scatter.apply_transform(trans=Matrix().rotate(transform_angle, 0, 0, 1), post_multiply=True, anchor=(98, 38))
        
        elif touch.x > self.right:
            # if the finger moved too far to the right go into rotation mode, remember where the rotation started and disable translation
            ud['tank_position'] = self.pos + (46, 75)
            self.do_translation_y = False
            
        
        return super(Tank, self).on_touch_move(touch)
      
    
    '''
    ####################################
    ##
    ##   On Touch Up
    ##
    ####################################
    '''
    def on_touch_up(self, touch):
        # set translation_y to the initial state again
        self.do_translation_y = True
        return super(Tank, self).on_touch_up(touch)
            

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
        print 'fire!'
    
    def reset_button_pressed(self):
        print 'reset'
    
    def menu_button_pressed(self):
        print 'menu'
        self.Tank.pos = (0, 0)


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
    