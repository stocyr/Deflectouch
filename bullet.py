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

from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.animation import Animation

from kivy.utils import boundary
from math import tan
from math import pi
from kivy.vector import Vector


class Bullet(Image):
    angle = NumericProperty(0)
    animation = ObjectProperty(None)
        
    '''
    ####################################
    ##
    ##   Bullet Behavioral
    ##
    ####################################
    '''
    
    def __init__(self, **kwargs):
        super(Bullet, self).__init__(**kwargs)
        
    def fire(self):
        destination = self.calc_destination(self.angle)
        speed = boundary(self.parent.app.config.getint('GamePlay', 'BulletSpeed'), 1, 10)
        self.animation = self.create_animation(speed, destination)
        
        # start the animation
        self.animation.start(self)
        self.animation.bind(on_complete=self.on_collision_with_edge)
        
        # schedule the position change
        self.bind(pos=self.callback_pos)
    
    def create_animation(self, speed, destination):
        # create the animation
        # t = s/v -> v from 1 to 10 / unit-less
        time = Vector(self.center).distance(destination) / (speed * 70)
        return Animation(pos=destination, duration=time)
        
    def calc_destination(self, angle):
                # calculate the path until the bullet hits the edge of the screen
        win = self.get_parent_window()
        left = 102
        right = win.width - 20
        top = win.height - 20
        bottom = 20
        
        bullet_x_to_right = right - self.center_x
        bullet_x_to_left = left - self.center_x
        bullet_y_to_top = top - self.center_y
        bullet_y_to_bottom = bottom - self.center_y
        
        destination_x = 0
        destination_y = 0
        
            
        # this is a little bit ugly, but i couldn't find a nicer way in the hurry
        if self.angle >= 0 and self.angle < pi/2:
            # 1st quadrant
            if self.angle == 0:
                destination_x = bullet_x_to_right
                destination_y = 0
            else:
                destination_x = boundary(bullet_y_to_top / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_right, bullet_y_to_bottom, bullet_y_to_top)
                
        elif self.angle >= pi/2 and self.angle < pi:
            # 2nd quadrant
            if self.angle == pi/2:
                destination_x = 0
                destination_y = bullet_y_to_top
            else:
                destination_x = boundary(bullet_y_to_top / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_left, bullet_y_to_bottom, bullet_y_to_top)
                
        elif self.angle >= pi and self.angle < 3*pi/2:
            # 3rd quadrant
            if self.angle == pi:
                destination_x = bullet_x_to_left
                destination_y = 0
            else:
                destination_x = boundary(bullet_y_to_bottom / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_left, bullet_y_to_bottom, bullet_y_to_top) 
                       
        elif self.angle >= 3*pi/2:
            # 4th quadrant
            if self.angle == 3*pi/2:
                destination_x = 0
                destination_y = bullet_y_to_bottom
            else:
                destination_x = boundary(bullet_y_to_bottom / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_right, bullet_y_to_bottom, bullet_y_to_top)
            
        
        
        destination_x += self.center_x
        destination_y += self.center_y
        
        return (destination_x, destination_y)
    
    def callback_pos(self, value, pos):
        # check here if the bullet collides with a deflector or an obstacle
        
        # first check if there's a collision with deflectors:
        if not len(self.parent.deflector_list) == 0:
            for deflector in self.parent.deflector_list:
                print 'line pos: ', deflector.deflector_line.pos, 'line size: ', deflector.deflector_line.size
                if self.collide_widget(deflector.deflector_line):
                    # if the bullet collides with the deflector line of one of the deflectors,
                    # call on_collision_with_deflector and pass it the colliding instance
                    self.on_collision_with_deflector(deflector)
        
        # then check if there's a collision with the goal:
        
        
        # then check if there's a collision with obstacles:
        
    
    def fade_out(self):
        # create fade-out animation
        #bind(animation, self.parent.bullet_died
        self.parent.bullet_died()
        
    def on_collision_with_edge(self, animation, widget):
        print 'edge'
        self.fade_out()
    
    def on_collision_with_obstacle(self):
        print 'obstacle'
        self.fade_out()
    
    def on_collision_with_deflector(self, deflector):
        print 'deflector'
        # calculate deflection_angle
        # calculate new animation
        # start animation
    
    def on_collision_with_goal(self):
        print 'goal'
        self.fade_out()
        
        
        
        
        
        
        
        
        
        
        
        