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

from kivy.uix.image import Image
from kivy.properties import NumericProperty

MIN_DEFLECTOR_LENGTH = 100


'''
####################################
##
##   Stock Bar Image Class
##
####################################
'''
class Stockbar(Image):
    max_stock = NumericProperty(0)
    
    new_deflectors_allowed = True
    
    
    def recalculate_stock(self):
        # this function is called every time a deflector size is changing
        # first sum up all the deflectors on screen
        length_sum = 0
        
        if not len(self.parent.deflector_list) == 0:
            for deflector in self.parent.deflector_list:
                length_sum += deflector.length
        
        self.width = self.max_stock - length_sum
        
        if self.width < MIN_DEFLECTOR_LENGTH:
            # if the stock material doesn't suffice for a new deflector, disable new deflectors
            self.source = 'graphics/deflector_red.png'
            self.new_deflectors_allowed = False
        elif self.width <= 0:
            # if all the stock material was used up, disable new deflectors
            self.new_deflectors_allowed = False
        else:
            self.source = 'graphics/deflector_blue.png'
            self.new_deflectors_allowed = True
    
    def new_deflector(self, length):
        # is called when a new deflector is created.
        self.width -= length
    
    def deflector_deleted(self, length):
        self.width += length


