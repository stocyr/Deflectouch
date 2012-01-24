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

from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.properties import NumericProperty


'''
####################################
##
##   Stock Bar Image Class
##
####################################
'''
class Stockbar(Image):
    max_stock = NumericProperty(0)
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    pass

    def recalculate_stock(self):
        # this function is called every time a deflector size is changing
        # first sum up all the deflectors on screen
        length_sum = 0
        
        if not len(self.parent.deflector_list) == 0:
            for deflector in self.parent.deflector_list:
                length_sum += deflector.length
        
        self.width = self.max_stock - length_sum
    
    def new_deflector(self, length):
        # is called when a new deflector is created.
        animation = Animation(width=self.width - length, t='out_elastic', duration=1)
        animation.start(self)