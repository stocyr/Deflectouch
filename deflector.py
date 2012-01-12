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

from kivy.properties import ObjectProperty
from kivy.uix.scatter import Scatter


class Deflector(Scatter):
    touch1 = ObjectProperty(None)
    touch2 = ObjectProperty(None)
    
    end_point1 = ObjectProperty(None)
    end_point2 = ObjectProperty(None)
    deflector_line = ObjectProperty(None)
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        ud = touch.ud
        
        # This event handler is only used to ensure that transforming the scatter is exclusively possible on the two end points
        if self.end_point1.collide_point(*touch.pos) or self.end_point2.collide_point(*touch.pos):
            # if the user touched one of the end points (valid touch), dispatch the touch to the scatter
            print 'end point touched - dispatching to scatter'
            return super(Deflector, self).on_touch_down(touch)
        else:
            # if not, keep the touch
            print 'no end point touched'
            return True
    
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
