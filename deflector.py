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

from kivy.properties import ObjectProperty, NumericProperty
from kivy.graphics import Color, Ellipse, Line
from kivy.graphics.texture import Texture
from kivy.graphics.instructions import Canvas
from kivy.graphics.transformation import Matrix
from kivy.vector import Vector

from kivy.uix.scatter import Scatter
from kivy.core.image import Image

from math import atan2


class Deflector(Scatter):
    touch1 = ObjectProperty(None)
    touch2 = ObjectProperty(None)
    
    point1 = ObjectProperty(None)
    point2 = ObjectProperty(None)
    
    deflector_line = ObjectProperty(None)
    
    lenght = NumericProperty(0)
    
    '''
    ####################################
    ##
    ##   Class Initialisation
    ##
    ####################################
    '''
    def __init__(self, **kwargs):
        super(Deflector, self).__init__(**kwargs)
        
        # I create the two points and the line exactly under the two fingers.
        # They can be moved and scaled from within this class now.
        
        # We have to adjust the bounding box of ourself to the dimension of all the canvas objects (Do we have to?)
        self.size = (abs(self.touch2.x - self.touch1.x), abs(self.touch2.y - self.touch1.y))
        #self.pos = (min(self.touch1.x, self.touch2.x), min(self.touch1.y, self.touch2.y))
                
        #texture = Texture.create(size=(10, 10))
        self.texture = Image('graphics/beta/5x5.png').texture
        
        with self.canvas:
            self.point1 = Ellipse(
                                  size=(40,40),
                                  pos=(self.touch1.x - 20, self.touch1.y - 20),
                                  source='graphics/beta/finger_point_blue_beta.png'
                                  #source='graphics/beta/finger_point_blue_beta.png'
                                  )
            
            self.point2 = Ellipse(
                                  size=(40,40),
                                  pos=(self.touch2.x - 20, self.touch2.y - 20),
                                  source='graphics/beta/finger_point_blue_beta.png'
                                  )
            
            self.deflector_line = Line(
                                       points=(self.touch1.x, self.touch1.y, self.touch2.x, self.touch2.y),
                                       texture=self.texture
                                       )
        
        # We have to adjust the bounding box of ourself to the dimension of all the canvas objects (Do we have to?)
        #self.size = (abs(self.touch2.x - self.touch1.x), abs(self.touch2.y - self.touch1.y))
        
        # Now we finally grab both touches we received
        self.touch1.grab(self)
        self.touch2.grab(self)
    
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
        if self.point1.collide_point(*touch.pos) or self.point2.collide_point(*touch.pos):
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
