'''
Deflectouch

Copyright (C) 2012-2024 Cyril Stoller

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

from kivy.graphics.transformation import Matrix
from math import atan2


MIN_DEFLECTOR_LENGTH = 100
GRAB_RADIUS = 30



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
        
        self.length_origin = self.length
        
        with self.canvas.before:
            Color(.8, .8, .8)
            self.deflector_line = Line(points=(self.touch1.x, self.touch1.y - 1, self.touch1.x + self.length, self.touch1.y - 1))
            self.deflector_line2 = Line(points=(self.touch1.x, self.touch1.y + 1, self.touch1.x + self.length, self.touch1.y + 1))
        
        '''
        self.deflector_line = Image(source='graphics/beta/deflector_blue_beta2.png',
                                    allow_stretch=True,
                                    keep_ratio=False,
                                    size=(self.length, 20),
                                    center_y=(self.touch1.y),
                                    x=self.touch1.x)
        '''
        
        # set the right position for the two points:
        self.point1.center = self.touch1.pos
        self.point2.center = self.touch1.x + self.length, self.touch1.y
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
        
        # feedback to the stockbar: reducing of the deflector material stock:
        #self.length = Vector(self.touch1.pos).distance(self.touch2.pos)
        self.length = self.length_origin * self.scale
        try:
            self.parent.parent.stockbar.recalculate_stock()
        except Exception as e:
            return
        # get the current stock from the root widget:
        current_stock = self.parent.parent.stockbar.width
        stock_for_me = current_stock + self.length
        
        # now set the limitation for scaling:
        self.scale_max = stock_for_me / self.length_origin
        
        if self.length < MIN_DEFLECTOR_LENGTH:
            self.point1.color = (1, 0, 0, 1)
            self.point2.color = (1, 0, 0, 1)
        else:
            self.point1.color = (0, 0, 1, 1)
            self.point2.color = (0, 0, 1, 1)
        
        
    
    def collide_widget(self, wid):
        point1_parent = self.to_parent(self.point1.center[0], self.point1.center[1])
        point2_parent = self.to_parent(self.point2.center[0], self.point2.center[1])
        
        if max(point1_parent[0], point2_parent[0]) < wid.x:
            return False
        if min(point1_parent[0], point2_parent[0]) > wid.right:
            return False
        if max(point1_parent[1], point2_parent[1]) < wid.y:
            return False
        if min(point1_parent[1], point2_parent[1]) > wid.top:
            return False
        return True
    
    def collide_point(self, x, y):
        # this function is used exclusively by the underlying scatter functionality.
        # therefor i can control when a touch will be dispatched from here.
        point1_parent = self.to_parent(self.point1.center[0], self.point1.center[1])
        point2_parent = self.to_parent(self.point2.center[0], self.point2.center[1])
        
        return min(point1_parent[0], point2_parent[0]) - GRAB_RADIUS <= x <= max(point1_parent[0], point2_parent[0]) + GRAB_RADIUS \
           and min(point1_parent[1], point2_parent[1]) - GRAB_RADIUS <= y <= max(point1_parent[1], point2_parent[1]) + GRAB_RADIUS
    
    def collide_grab_point(self, x, y):
        point1_parent = self.to_parent(self.point1.center[0], self.point1.center[1])
        point2_parent = self.to_parent(self.point2.center[0], self.point2.center[1])
        
        return point1_parent[0] - GRAB_RADIUS <= x <= point1_parent[0] + GRAB_RADIUS and point1_parent[1] - GRAB_RADIUS <= y <= point1_parent[1] + GRAB_RADIUS \
            or point2_parent[0] - GRAB_RADIUS <= x <= point2_parent[0] + GRAB_RADIUS and point2_parent[1] - GRAB_RADIUS <= y <= point2_parent[1] + GRAB_RADIUS
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        if self.parent.parent.app.sound['deflector_down'].state != 'play':
            self.parent.parent.app.sound['deflector_down'].play()
        
        return super(Deflector, self).on_touch_down(touch)
    
    '''
    ####################################
    ##
    ##   On Touch Up
    ##
    ####################################
    '''
    def on_touch_up(self, touch):
        # if the deflector want's to be removed (touches too close to each other):
        if self.length < MIN_DEFLECTOR_LENGTH and self.parent != None:
            self.parent.delete_deflector(self)
            return True
        
        if self.parent != None and self.collide_grab_point(*touch.pos):
            if self.parent.parent.app.sound['deflector_up'].state != 'play':
                self.parent.parent.app.sound['deflector_up'].play()
        
        return super(Deflector, self).on_touch_up(touch)


