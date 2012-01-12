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

from kivy.graphics.transformation import Matrix
from kivy.vector import Vector
from math import radians
from math import atan2


class Deflector(Scatter):
    touch1 = ObjectProperty(None)
    touch2 = ObjectProperty(None)
    
    end_point1 = ObjectProperty(None) # refers to the end point IMAGES.
    end_point2 = ObjectProperty(None)
    
    deflector_line = ObjectProperty(None)
    
    '''
    ####################################
    ##
    ##   Class Initialisation
    ##
    ####################################
    '''
    def __init__(self, **kwargs):
        super(Deflector, self).__init__(**kwargs)
        
        # Here I rotate and translate the deflector line so that it lays exactly under the two fingers
        # and can be moved and scaled by scatter from now on. Thus I also have to pass the touches to scatter.
        
        # size:
        finger_distance = Vector(self.touch1.pos).distance(self.touch2.pos)
        self.deflector_line.size = (finger_distance, 0) # -> does that work?
        
        # position:
        # First I set the one end point to the first touch, then
        # I'm gonna rotate it arround the position of the first touch, so that it will arrive at the other touch.
        # possible problem: the above scatter won't then adjust its bounding box and so on... --> same prob as with the tank scatter.
        self.deflector_line.pos = self.touch1.pos
        
        # adjusting the position of the two end-points
        self.end_point1.center = self.touch1.pos
        self.end_point2.center = (self.touch1.x + finger_distance, self.touch1.y)
        
        # rotation:
        dx = self.touch2.x - self.touch1.x
        dy = self.touch2.y - self.touch1.y
        angle = atan2(dy, dx)
        
        rotation_matrix = Matrix().rotate(angle, 0, 0, 1)
        self.apply_transform(rotation_matrix, post_multiply=True, anchor=self.to_local(self.touch1.x, self.touch1.y))
        
        
        # Now we finally add both touches we received to the _touches list of the underlying scatter class structure. 
        self.touch1.grab(self)
        self._touches.append(self.touch1)
        self._last_touch_pos[self.touch1] = self.touch1.pos
        
        self.touch2.grab(self)
        self._touches.append(self.touch2)
        self._last_touch_pos[self.touch2] = self.touch2.pos
    
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    '''
    def on_touch_down(self, touch):
        
        if not self.collide_point(*touch.pos):
            return False
        
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
