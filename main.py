'''
IcarusTouch

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
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty, StringProperty

from kivy.uix.image import Image
from kivy.uix.widget import Widget


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
##   Main Widget Class
##
####################################
'''
class DeflectouchWidget(Widget):
    app = ObjectProperty(None)
    version = StringProperty(VERSION)
    
    
    '''
    ####################################
    ##
    ##   Class Initialisation
    ##
    ####################################
    '''
    def __init__(self, **kwargs):
        super(DeflectouchWidget, self).__init__(**kwargs) # don't know if this is necessary?
        
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        ud = touch.ud
        
    
    
    '''
    ####################################
    ##
    ##   On Touch Move
    ##
    ####################################
    '''
    def on_touch_move(self, touch):
        ud = touch.ud
        
    
    
    '''
    ####################################
    ##
    ##   On Touch Up
    ##
    ####################################
    '''
    def on_touch_up(self, touch):
        ud = touch.ud
        
    
    
    '''
    ####################################
    ##
    ##   Other GUI Events
    ##
    ####################################
    '''
    
    
    '''
    ####################################
    ##
    ##   Graphical Functions
    ##
    ####################################
    '''
    def create_circle(self, touch):
        # create the circle image
        circle = Image(
            source=self.app.config.get('Advanced', 'CircleImage'),
            color=(.7, .85, 1, 1),
            allow_stretch=True,
            size=(self.app.config.getint('Advanced', 'CircleSize'), self.app.config.getint('Advanced', 'CircleSize')))
        
        # center the circle on the finger position
        circle.x = touch.x - circle.size[0] / 2
        circle.y = touch.y - circle.size[1] / 2
        
        self.add_widget(circle)
        
        # and just right fade it out after having displayed it
        animation = Animation(
            color=(.7, .85, 1, 0),
            size=(self.app.config.getint('Advanced', 'CircleSize') * 2, self.app.config.getint('Advanced', 'CircleSize') * 2),
            x=circle.pos[0] - (self.app.config.getint('Advanced', 'CircleSize')/2), # workaround for centering the image during resizing
            y=circle.pos[1] - (self.app.config.getint('Advanced', 'CircleSize')/2), # workaround for centering the image during resizing
            t='out_expo', duration=2)
        
        animation.start(circle)
        animation.bind(on_complete=self.circle_fadeout_complete)
    
    def circle_fadeout_complete(self, animation, widget):
        self.remove_widget(widget)
        


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
        # create the various section for the .ini settings file:
        
        config.adddefaultsection('General')
        config.setdefault('General', 'Sound', 'On')
        config.setdefault('General', 'Music', 'On')
    


if __name__ in ('__main__', '__android__'):
    Deflectouch().run()
    