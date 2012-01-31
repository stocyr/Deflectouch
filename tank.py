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
from kivy.graphics.transformation import Matrix
from kivy.uix.widget import Widget

from kivy.utils import boundary
from math import radians
from math import atan2
from math import pi

'''
####################################
##
##   Tank Class
##
####################################
'''
class Tank(Widget):
    tank_tower_scatter = ObjectProperty(None)
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        else:
            touch.ud['tank_touch'] = True
            return True
            
        
    
    '''
    ####################################
    ##
    ##   On Touch Move
    ##
    ####################################
    '''
    def on_touch_move(self, touch):
        ud = touch.ud
        
        if not 'tank_touch' in ud:
            return False
        
        if 'rotation_mode' in ud:
            # if the current touch is already in the 'rotate' mode, rotate the tower.
            dx = touch.x - self.center_x
            dy = touch.y - self.center_y
            angle = boundary(atan2(dy, dx) * 360 / 2 / pi, -60, 60)
            
            angle_change = self.tank_tower_scatter.rotation - angle
            rotation_matrix = Matrix().rotate(-radians(angle_change), 0, 0, 1)
            self.tank_tower_scatter.apply_transform(rotation_matrix, post_multiply=True, anchor=(105, 15))
        
        elif touch.x > self.right:
            # if the finger moved too far to the right go into rotation mode
            ud['rotation_mode'] = True
        
        else:
            # if the user wants only to drag the tank up and down, let him do it!
            self.y += touch.dy
            pass

