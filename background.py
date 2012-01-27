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
from kivy.base import EventLoop
from kivy.vector import Vector

from deflector import Deflector


'''
####################################
##
##   Background Image Class
##
####################################
'''
class Background(Image):
    
    '''
    ####################################
    ##
    ##   On Touch Down
    ##
    ####################################
    '''
    def on_touch_down(self, touch):
        ud = touch.ud
        
        for deflector in self.parent.deflector_list:
            if deflector.collide_point(*touch.pos):
                print 'touch on deflector'
                
                # here comes the selection: do i want to pass the touches to the scatter?
                # if i really pass it to a deflector:
                return True
        
        # if i didn't wanted to move / scale a deflector and but rather create a new one:
        # search for other 'lonely' touches
              
        for search_touch in EventLoop.touches[:]:
            if 'lonely' in search_touch.ud:
                # so here we have a second touch: make a pairing.
                del search_touch.ud['lonely']
                self.create_deflector(search_touch, touch)
                return True
        
        # if no second touch was found: tag the current one as a 'lonely' touch
        ud['lonely'] = True
        
    
    def create_deflector(self, touch_1, touch_2):
        length = Vector(touch_1.pos).distance(touch_2.pos)
        deflector = Deflector(touch1=touch_1, touch2=touch_2, length=length)
        self.parent.deflector_list.append(deflector)
        self.add_widget(deflector)
        
        self.parent.stockbar.new_deflector(length)
        
    
    def delete_deflector(self, deflector):
        self.parent.stockbar.deflector_deleted(deflector.length)
        
        self.remove_widget(deflector)
        self.parent.deflector_list.remove(deflector)
    
    def delete_all_deflectors(self):
        for deflector in self.parent.deflector_list:
            self.remove_widget(deflector)
        self.parent.deflector_list = []
        
        self.parent.stockbar.recalculate_stock()
