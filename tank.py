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
from kivy.uix.image import Image

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
class Tank(Image):
    tank_tower_scatter = ObjectProperty(None)
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        #if not self.collide_point(*touch.pos):
        #    touch.ungrab(self)
        #    return False
        #else:
        print 'tank'
        touch.ud['tank_touch'] = True
        #return super(Tank, self).on_touch_down(touch)
        
    
    '''
    ####################################
    ##
    ##   On Touch Move
    ##
    ####################################
    '''
    def on_touch_move(self, touch):
        ud = touch.ud
        
        if 'tank_touch' in ud:
            # Here comes the calculation for the tower-rotating
            if 'tank_position' in ud:
                # if the current touch is already in the 'rotate' mode, rotate the tower.
                dx = touch.x - (ud['tank_position'][0] + 46)    # +46 -> the reference point is in the middle of the tank image.
                dy = touch.y - (ud['tank_position'][1] + 75)    # +75 -> the reference point is in the middle of the tank image.
                angle = boundary(atan2(dy, dx) * 360 / 2 / pi, -60, 60)
                
                angle_change = self.tank_tower_scatter.rotation - angle
                rotation_matrix = Matrix().rotate(-radians(angle_change), 0, 0, 1)
                self.tank_tower_scatter.apply_transform(rotation_matrix, post_multiply=True, anchor=(98, 38))
                
                #self.tank_tower_scatter.rotation = angle
                #self.tank_tower_scatter.apply_transform(trans=Matrix().rotate(transform_angle, 0, 0, 1), post_multiply=True, anchor=(98, 38))
            
            elif touch.x > self.right:
                # if the finger moved too far to the right go into rotation mode, remember where the rotation started and disable translation
                ud['tank_position'] = self.pos
                self.do_translation_y = False
            
            else:
                print 'move'
                # if 'normal' dragging (up and down) is performed, do it: 
                self.y += touch.dy
                print touch.dy
      
    
    '''
    ####################################
    ##
    ##   On Touch Up
    ##
    ####################################
    '''
    def on_touch_up(self, touch):
        pass

