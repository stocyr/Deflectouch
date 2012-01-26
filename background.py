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
        
        # the first time a touch occures, nothing happens. If a second finger is touching,
        # create a deflector.
        
        # search for a lonely touch
        
        pairing_made = False        
        for search_touch in EventLoop.touches[:]:
            if 'lonely' in search_touch.ud:
                # so here we have a second touch: make a pairing.
                del search_touch.ud['lonely']
                print 'pairing made'
                self.create_deflector(search_touch, touch)
                pairing_made = True
        
        if pairing_made == False:
            # if no second touch was found: tag the current one as 'lonely'
            ud['lonely'] = True
            #print 'lonely touch'
    
    def create_deflector(self, touch_1, touch_2):
        length = self.length_origin = Vector(touch_1.pos).distance(touch_2.pos)
        deflector = Deflector(touch1=touch_1, touch2=touch_2, length=length)
        self.parent.deflector_list.append(deflector)
        self.add_widget(deflector)
        
        self.parent.stockbar.new_deflector(length)
        
    
    def delete_deflector(self, deflector):
        self.parent.stockbar.deflector_deleted(deflector.length)
        
        self.remove_widget(deflector)
        self.parent.deflector_list.remove(deflector)
        del deflector
