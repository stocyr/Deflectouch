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

from kivy.properties import NumericProperty
from kivy.uix.image import Image


class Bullet(Image):
    angle = NumericProperty(0)
        
    '''
    ####################################
    ##
    ##   Bullet Behavioral
    ##
    ####################################
    '''
    def fire(self):
        # calculate the path
        # start the animation
        # schedule the collision check if necessary
        pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        