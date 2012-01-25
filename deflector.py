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

from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image

from kivy.graphics.transformation import Matrix
from kivy.vector import Vector
from math import atan2


MIN_DEFLECTOR_LENGTH = 100


class Deflector(Scatter):
    touch1 = ObjectProperty(None)
    touch2 = ObjectProperty(None)
    
    point1 = ObjectProperty(None)
    point2 = ObjectProperty(None)
    
    deflector_line = ObjectProperty(None)
    
    length = NumericProperty(0)
    length_origin = 0
    
    point_pos_origin = []
    
    '''
    ####################################
    ##
    ##   Class Initialisation
    ##
    ####################################
    '''
    def __init__(self, **kwargs):
        super(Deflector, self).__init__(**kwargs)
        
        # DEFLECTOR LINE:
        # Here I rotate and translate the deflector line so that it lays exactly under the two fingers
        # and can be moved and scaled by scatter from now on. Thus I also have to pass the touches to scatter.
        # First i create the line perfectly horizontal but with the correct length. Then i add the two
        # drag points at the beginning and the end.
        
        #self.deflector_line.size = (self.length, 0)
        #self.deflector_line.pos = self.touch1.pos
        
        self.length_origin = self.length
        
        with self.canvas.before:
            Color(.8, .8, .8)
            self.deflector_line = Line(points=(self.touch1.x, self.touch1.y, self.touch1.x + self.length, self.touch1.y))
        
        '''
        self.deflector_line = Image(source='graphics/beta/deflector_blue_beta2.png',
                                    allow_stretch=True,
                                    keep_ratio=False,
                                    size=(self.length, 20),
                                    center_y=(self.touch1.y),
                                    x=self.touch1.x)
        '''
        
        # set the right position for the two points:
        self.point1.pos = self.touch1.x - 20, self.touch1.y - 20
        self.point2.pos = self.touch1.x - 20 + self.length, self.touch1.y - 20
        self.point_pos_origin = [self.point1.x, self.point1.y, self.point2.x, self.point2.y]
        
        
        # rotation:
        dx = self.touch2.x - self.touch1.x
        dy = self.touch2.y - self.touch1.y
        angle = atan2(dy, dx)
        
        rotation_matrix = Matrix().rotate(angle, 0, 0, 1)
        self.apply_transform(rotation_matrix, post_multiply=True, anchor=self.to_local(self.touch1.x, self.touch1.y))
        
        # We have to adjust the bounding box of ourself to the dimension of all the canvas objects (Do we have to?)
        #self.size = (abs(self.touch2.x - self.touch1.x), abs(self.touch2.y - self.touch1.y))
        #self.pos = (min(self.touch1.x, self.touch2.x), min(self.touch1.y, self.touch2.y))
        
        # Now we finally add both touches we received to the _touches list of the underlying scatter class structure. 
        self.touch1.grab(self)
        self._touches.append(self.touch1)
        self._last_touch_pos[self.touch1] = self.touch1.pos
        
        self.touch2.grab(self)
        self._touches.append(self.touch2)
        self._last_touch_pos[self.touch2] = self.touch2.pos
        
        self.point1.bind(size=self.size_callback)
    
    def size_callback(self, instance, size):        
        # problem: if the points are resized (scatter resized them, kv-rule resized them back),
        # their center isn't on the touch point anymore.
        self.point1.pos = self.point_pos_origin[0] + (40 - size[0])/2, self.point_pos_origin[1] + (40 - size[0])/2
        self.point2.pos = self.point_pos_origin[2] + (40 - size[0])/2, self.point_pos_origin[3] + (40 - size[0])/2
        
        # here comes the calculations of the remaining deflector material stock:
        self.length = Vector(self.touch1.pos).distance(self.touch2.pos)
        
        # get the current stock from the root widget:
        current_stock = self.parent.parent.stockbar.width
        
        # now set the limitation for scaling:
        self.scale_max = (self.length_origin + current_stock) / self.length_origin
        
        # and if i'm allowed to do, decrease the stock bar
        if current_stock > 0:
            self.parent.parent.stockbar.recalculate_stock()
        
        if self.length < MIN_DEFLECTOR_LENGTH:
            self.point1.source = 'graphics/beta/finger_point_red_beta.png'
            self.point2.source = 'graphics/beta/finger_point_red_beta.png'
        else:
            self.point1.source = 'graphics/beta/finger_point_blue_beta.png'
            self.point2.source = 'graphics/beta/finger_point_blue_beta.png'
        
        
    
    def collide_widget(self, wid):
        if max(self.point1.pos[0], self.point2.pos[0]) < wid.x:
            return False
        if min(self.point1.pos[0], self.point2.pos[0]) > wid.right:
            return False
        if max(self.point1.pos[1], self.point2.pos[1]) < wid.y:
            return False
        if min(self.point1.pos[1], self.point2.pos[1]) > wid.top:
            return False
        return True
    
    def collide_point(self, x, y):
        return min(self.point1.pos[0], self.point2.pos[0]) <= x <= max(self.point1.pos[0], self.point2.pos[0]) \
           and min(self.point1.pos[1], self.point2.pos[1]) <= y <= max(self.point1.pos[1], self.point2.pos[1])
    
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    
    def on_touch_down(self, touch):
        '''
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
        print touch
    
    '''
    ####################################
    ##
    ##   On Touch Up
    ##
    ####################################
    '''
    '''
    def on_touch_up(self, touch):
        # remove the two grabbed touches from the list
        if self.touch1 in self._touches and self.touch1.grab_state:
            self.touch1.ungrab(self)
            del self._last_touch_pos[self.touch1]
            self._touches.remove(self.touch1)
        if self.touch2 in self._touches and self.touch2.grab_state:
            self.touch2.ungrab(self)
            del self._last_touch_pos[self.touch2]
            self._touches.remove(self.touch2)
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
