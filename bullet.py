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
from math import sin
from math import pi
from math import radians
from kivy.vector import Vector


class Bullet(Image):
    angle = NumericProperty(0) # in radians!
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
        animation = self.create_animation(speed, destination)
        
        # start the animation
        animation.start(self)
        animation.bind(on_complete=self.on_collision_with_edge)
        
        # start to track the position changes
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
        if 0 <= self.angle < pi/2:
            # 1st quadrant
            if self.angle == 0:
                destination_x = bullet_x_to_right
                destination_y = 0
            else:
                destination_x = boundary(bullet_y_to_top / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_right, bullet_y_to_bottom, bullet_y_to_top)
                
        elif pi/2 <= self.angle < pi:
            # 2nd quadrant
            if self.angle == pi/2:
                destination_x = 0
                destination_y = bullet_y_to_top
            else:
                destination_x = boundary(bullet_y_to_top / tan(self.angle), bullet_x_to_left, bullet_x_to_right)
                destination_y = boundary(tan(self.angle) * bullet_x_to_left, bullet_y_to_bottom, bullet_y_to_top)
                
        elif pi <= self.angle < 3*pi/2:
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
    
    def check_deflector_collision(self, deflector):
        # Here we have a collision Bullet <--> Deflector-bounding-box. But that doesn't mean
        # that there's a collision with the deflector LINE yet. So here's some math stuff
        # for the freaks :) It includes vector calculations, distance problems and trigonometry
        
        # first thing to do is: we need a vector describing the bullet. Length isn't important.
        bullet_position = Vector(self.center)
        bullet_direction = Vector(1, 0).rotate(self.angle * 360 / (2*pi))
        
        # then we need a vector describing the deflector line.
        deflector_vector = Vector(deflector.touch2.pos) - Vector(deflector.touch1.pos)
        
        # now we do a line intersection with the deflector line:
        intersection = Vector.line_intersection(bullet_position, bullet_position + bullet_direction, Vector(deflector.touch1.pos), Vector(deflector.touch2.pos))
        
        # now we want to proof if the bullet comes from the 'right' side.
        # Because it's possible that the bullet is colliding with the deflectors bounding box but
        # would miss / has already missed the deflector line.
        # We do that by checking if the intersection point is BEHIND the bullet position.
        # ('behind' means the bullet direction points AWAY from the intersection point)
        if bullet_direction.angle(intersection - bullet_position) == pi:
            # if the bullet missed the line already - NO COLLISION
            return False
        
        # now we finally check if the bullet is close enough to the deflector line:
        distance = sin(radians(bullet_direction.angle(deflector_vector) % (pi/4))) * Vector(bullet_position - intersection).length()
        if distance < (self.width / 2):
            # there is a collision!
            self.on_collision_with_deflector(deflector, deflector_vector)
            
        
    
    def callback_pos(self, value, pos):
        # check here if the bullet collides with a deflector or an obstacle
        
        # first check if there's a collision with deflectors:
        if not len(self.parent.deflector_list) == 0:
            for deflector in self.parent.deflector_list:
                if self.collide_widget(deflector):
                    # if the bullet collides with the bounding box of a deflector
                    # call check_deflector_collision and pass it the colliding instance
                    self.check_deflector_collision(deflector)
        
        # then check if there's a collision with the goal:
        
        
        # then check if there's a collision with obstacles:
        
    
    def bullet_fade_out(self):
        # create fade-out animation
        #bind(animation, self.parent.bullet_died
        self.parent.bullet_died()
        
    def on_collision_with_edge(self, animation, widget):
        print 'edge'
        self.bullet_fade_out()
    
    def on_collision_with_obstacle(self):
        print 'obstacle'
        self.bullet_fade_out()
    
    def on_collision_with_deflector(self, deflector, deflector_vector):
        print 'deflector'
        # flash up the deflector
        deflector.color = (1, 1, 1)
        Animation(color=(0, 0, 1), duration=1, t='out_expo').start(deflector)
        
        # calculate deflection angle
        impact_angle = (radians(deflector_vector.angle(Vector(1, 0))) % pi) - (self.angle % pi)
        self.angle = (self.angle + 2*impact_angle) % (2*pi)
        
        destination = self.calc_destination(self.angle)
        speed = boundary(self.parent.app.config.getint('GamePlay', 'BulletSpeed'), 1, 10)
        animation = self.create_animation(speed, destination)
        
        # start the animation
        animation.start(self)
        animation.bind(on_complete=self.on_collision_with_edge)
    
    def on_collision_with_goal(self):
        print 'goal'
        self.bullet_fade_out()
        
        
        
        
        
        
        
        
        
        
        
        