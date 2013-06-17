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

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.factory import Factory
from kivy.utils import boundary
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from math import sin
from math import cos
from math import radians

from random import randint


from background import Background
from tank import Tank
from bullet import Bullet
from stockbar import Stockbar


'''
####################################
##
##   GLOBAL SETTINGS
##
####################################
'''

VERSION = '1.0'

LEVEL_WIDTH = 16
LEVEL_HEIGHT = 16


'''
####################################
##
##   Setting Dialog Class
##
####################################
'''
class SettingDialog(BoxLayout):
    music_slider = ObjectProperty(None)
    sound_slider = ObjectProperty(None)
    speed_slider = ObjectProperty(None)
    
    root = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(SettingDialog, self).__init__(**kwargs)
        
        self.music_slider.bind(value=self.update_music_volume)
        self.sound_slider.bind(value=self.update_sound_volume)
        self.speed_slider.bind(value=self.update_speed)
    
    def update_music_volume(self, instance, value):
        # write to app configs
        self.root.app.config.set('General', 'Music', str(int(value)))
        self.root.app.config.write()
        self.root.app.music.volume = value / 100.0
    
    def update_sound_volume(self, instance, value):
        # write to app configs
        self.root.app.config.set('General', 'Sound', str(int(value)))
        self.root.app.config.write()
        for item in self.root.app.sound:
            self.root.app.sound[item].volume = value / 100.0
    
    def update_speed(self, instance, value):
        # write to app configs
        self.root.app.config.set('GamePlay', 'BulletSpeed', str(int(value)))
        self.root.app.config.write()
    
    def display_help_screen(self):
        self.root.setting_popup.dismiss()
        self.root.display_help_screen()
    
    def dismiss_parent(self):
        self.root.setting_popup.dismiss()
    

'''
####################################
##
##   Main Widget Class
##
####################################
'''
class DeflectouchWidget(Widget):
    app = ObjectProperty(None)
    version = StringProperty(VERSION)
    
    level = NumericProperty(1)
    lives = NumericProperty(3)
    
    bullet = None
    setting_popup = None
    stockbar = None
    
    deflector_list = []
    obstacle_list = []
    goal_list = []
    
    max_stock = 0
    
    level_build_index = 0
    
    
    '''
    ####################################
    ##
    ##   GUI Functions
    ##
    ####################################
    '''
    def fire_button_pressed(self):
        if self.bullet:
            # if there is already a bullet existing (which means it's flying around or exploding somewhere)
            # don't fire.
            return
        
        self.app.sound['bullet_start'].play()
        
        # create a bullet, calculate the start position and fire it.
        tower_angle = radians(self.tank.tank_tower_scatter.rotation)
        tower_position = self.tank.pos
        bullet_position = (tower_position[0] + 48 + cos(tower_angle) * 130, tower_position[1] + 70 + sin(tower_angle) * 130)
        self.bullet = Bullet(angle=tower_angle)
        self.bullet.center = bullet_position
        self.add_widget(self.bullet)
        self.bullet.fire()
    
    
    def reset_button_pressed(self):
        self.app.sound['reset'].play()
        
        self.reset_level()
        
    
    def level_button_pressed(self):
        self.app.sound['switch'].play()
        
        # create a popup with all the levels
        grid_layout = GridLayout(cols=8,rows=5,spacing=10, padding=10)
        
        enable_next_row = True
        row_not_complete = False
        for row in range(5):
            for collumn in range(8):
                button = Button(text=str(row*8 + (collumn + 1)),bold=True,font_size=30)
                
                if enable_next_row == True:
                    # if this row is already enabled:
                    button.bind(on_press=self.load_level)
                
                    if self.app.config.get('GamePlay', 'Levels')[row*8 + collumn] == '1':
                        # if level was already done, green button
                        button.background_color = (0, 1, 0, 1)
                    else:
                        # if level not yet done but enabled though, red button
                        button.background_color = (1, 0, 0, 0.5)
                        
                        # and do NOT enable the next row then:
                        row_not_complete = True
                
                else:
                    # if not yet enabled:
                    button.background_color = (0.1, 0.05, 0.05, 1)
                    
                grid_layout.add_widget(button)
            
            if row_not_complete == True:
                enable_next_row = False
        
        popup = Popup(title='Level List (if you finished a row, the next row will get enabled!)',
                      content=grid_layout,
                      size_hint=(0.5, 0.5))
        popup.open()
    
    
    def settings_button_pressed(self):
        self.app.sound['switch'].play()
        
        # the first time the setting dialog is called, initialize its content.
        if self.setting_popup is None:
            
            self.setting_popup = Popup(attach_to=self,
                                       title='DeflecTouch Settings',
                                       size_hint=(0.3, 0.5))
            
            self.setting_dialog = SettingDialog(root=self)
            
            self.setting_popup.content = self.setting_dialog
        
            self.setting_dialog.music_slider.value = boundary(self.app.config.getint('General', 'Music'), 0, 100)
            self.setting_dialog.sound_slider.value = boundary(self.app.config.getint('General', 'Sound'), 0, 100)
            self.setting_dialog.speed_slider.value = boundary(self.app.config.getint('GamePlay', 'BulletSpeed'), 1, 10)
        
        self.setting_popup.open()
        
        
    def display_help_screen(self):
        # display the help screen on a Popup
        image = Image(source='graphics/help_screen.png')
        
        help_screen = Popup(title='Quick Guide through DEFLECTOUCH',
                            attach_to=self,
                            size_hint=(0.98, 0.98),
                            content=image)
        image.bind(on_touch_down=help_screen.dismiss)
        help_screen.open()
    
    
    '''
    ####################################
    ##
    ##   Game Play Functions
    ##
    ####################################
    '''
    
    def bullet_exploding(self):
        self.app.sound['explosion'].play()
        
        # create an animation on the old bullets position:
        # bug: gif isn't transparent
        #old_pos = self.bullet.center
        #self.bullet.anim_delay = 0.1
        #self.bullet.size = 96, 96
        #self.bullet.center = old_pos
        #self.bullet.source = 'graphics/explosion.gif'
        #Clock.schedule_once(self.bullet_exploded, 1)
        
        self.remove_widget(self.bullet)
        self.bullet = None
        # or should i write del self.bullet instead?
        
        self.lives -= 1
        if self.lives == 0:
            self.reset_level()
    
    
    def level_accomplished(self):
        self.app.sound['accomplished'].play()
        
        # store score in config: (i have to convert the string to a list to do specific char writing)
        levels_before = list(self.app.config.get('GamePlay', 'Levels'))
        levels_before[self.level - 1] = '1'
        self.app.config.set('GamePlay', 'Levels', "".join(levels_before))
        self.app.config.write()
        
        # show up a little image with animation: size*2 and out_bounce and the wait 1 sec
        image = Image(source='graphics/accomplished.png', size_hint=(None, None), size=(200, 200))
        image.center=self.center
        animation = Animation(size=(350, 416), duration=1, t='out_bounce')
        animation &= Animation(center=self.center, duration=1, t='out_bounce')
        animation += Animation(size=(350, 416), duration=1) # little hack to sleep for 1 sec
        
        self.add_widget(image)
        animation.start(image)
        animation.bind(on_complete=self.accomplished_animation_complete)
    
    
    def accomplished_animation_complete(self, animation, widget):
        self.remove_widget(widget)
        
        # open the level dialog?
        #self.level_button_pressed()
        
        # no. just open the next level.
        if self.level != 40:
            if self.level % 8 == 0:
                # if it was the last level of one row, another row has been unlocked!
                Popup(title='New levels unlocked!', content=Label(text='Next 8 levels unlocked!', font_size=18), size_hint=(0.3, 0.15)).open()
            
            self.reset_level()
            self.load_level(self.level + 1)
            
        
    def reset_level(self):
        # first kill the bullet
        if self.bullet != None:
            self.bullet.unbind(pos=self.bullet.callback_pos)
            self.bullet.animation.unbind(on_complete=self.bullet.on_collision_with_edge)
            self.bullet.animation.stop(self.bullet)
            self.remove_widget(self.bullet)
            self.bullet = None
        
        # then delete all the deflectors.
        self.background.delete_all_deflectors()
        
        # now the user can begin once again with 3 lives:
        self.lives = 3
    
    
    def load_level(self, level):
        BRICK_WIDTH = self.height / 17.73
        LEVEL_OFFSET = [self.center_x - (LEVEL_WIDTH/2) * BRICK_WIDTH, self.height / 12.5]
        
        # i have to check if the function is called by a level button in the level popup OR with an int as argument:
        if not isinstance(level, int):
            level = int(level.text)
            # and if the function was called by a button, play a sound
            self.app.sound['select'].play()
        
        # try to load the level image
        try:
            level_image = kivy.core.image.Image.load(self.app.directory + '/levels/level%02d.png' % level, keep_data=True)
        except Exception, e:
            error_text = 'Unable to load Level %d!\n\nReason: %s' % (level, e)
            Popup(title='Level loading error:', content=Label(text=error_text, font_size=18), size_hint=(0.3, 0.2)).open()
            return
        
        # First of all, delete the old level:
        self.reset_level()
        
        for obstacle in self.obstacle_list:
            self.background.remove_widget(obstacle)
        self.obstacle_list = []
        
        for goal in self.goal_list:
            self.background.remove_widget(goal)
        self.goal_list = []
        
        if self.stockbar != None:
            self.remove_widget(self.stockbar)
        self.max_stock = 0
        
        # set level inital state
        self.lives = 3
        self.level = level
        
        for y in range(LEVEL_HEIGHT, 0, -1):
            for x in range(LEVEL_WIDTH):
                color = level_image.read_pixel(x, y)
                if len(color) > 3:
                    # if there was transparency stored in the image, cut it.
                    color.pop()
                
                if color == [0, 0, 0]:
                    # create obstacle brick on white pixels
                    image = Image(source=('graphics/brick%d.png' % randint(1, 4)),
                                  x = LEVEL_OFFSET[0] + x * BRICK_WIDTH,
                                  y = LEVEL_OFFSET[1] + (y-1) * BRICK_WIDTH,
                                  size = (BRICK_WIDTH, BRICK_WIDTH),
                                  allow_stretch = True)
                    self.obstacle_list.append(image)
                    # the actual widget adding is done in build_level()
                    #self.background.add_widget(image)
                
                elif color == [0, 0, 1]:
                    # create a goal brick on blue pixels
                    image = Image(source=('graphics/goal%d.png' % randint(1, 4)),
                                  x = LEVEL_OFFSET[0] + x * BRICK_WIDTH,
                                  y = LEVEL_OFFSET[1] + (y-1) * BRICK_WIDTH,
                                  size = (BRICK_WIDTH, BRICK_WIDTH),
                                  allow_stretch = True)
                    self.goal_list.append(image)
                    # the actual widget adding is done in build_level()
                    #self.background.add_widget(image)
                    
        
        # but in the lowermost row there is also stored the value for the maximum stock 
        for x in range(LEVEL_WIDTH):
            color = level_image.read_pixel(x, 0)
            if len(color) > 3:
                # if there was transparency stored in the image, cut it.
                color.pop()
                    
            if color == [1, 0, 0]:
                self.max_stock += 1
        
        # now i set up the stockbar widget:
        self.max_stock = self.max_stock * self.width/1.4/LEVEL_WIDTH
        self.stockbar = Stockbar(max_stock=self.max_stock,
                                 x=self.center_x-self.max_stock/2,
                                 center_y=self.height/16 + 20)
        self.add_widget(self.stockbar)
        
        # now start to build up the level:
        self.level_build_index = 0
        if len(self.obstacle_list) != 0:
            Clock.schedule_interval(self.build_level, 0.01)
        
        
    def build_level(self, instance):
        #if self.level_build_index % int(0.02 / (0.5 / (len(self.obstacle_list) + len(self.goal_list)))) == 0:
            # play a sound every now and then:
        self.app.sound['beep'].play()
        
        if self.level_build_index < len(self.obstacle_list):
            self.background.add_widget(self.obstacle_list[self.level_build_index])
        else:
            if self.level_build_index - len(self.obstacle_list) != len(self.goal_list):
                self.background.add_widget(self.goal_list[self.level_build_index - len(self.obstacle_list)])
            else:
                # we're done. Disable the schedule
                return False
        self.level_build_index += 1

Factory.register("Tank", Tank)
Factory.register("Background", Background)
Factory.register("Stockbar", Stockbar)


'''
####################################
##
##   Main Application Class
##
####################################
'''
class Deflectouch(App):
    title = 'Deflectouch'
    icon = 'icon.png'
    
    sound = {}
    music = None
    
    
    def build(self):
        # print the application informations
        print '\nDeflectouch v%s  Copyright (C) 2012  Cyril Stoller' % VERSION
        print 'This program comes with ABSOLUTELY NO WARRANTY'
        print 'This is free software, and you are welcome to redistribute it'
        print 'under certain conditions; see the source code for details.\n'

        from kivy.base import EventLoop
        EventLoop.ensure_window()
        self.window = EventLoop.window
        
        # create the root widget and give it a reference of the application instance (so it can access the application settings)
        self.deflectouchwidget = DeflectouchWidget(app=self)
        self.root = self.deflectouchwidget
        
        
        # start the background music:
        self.music = SoundLoader.load('sound/deflectouch.ogg')
        self.music.volume = self.config.getint('General', 'Music') / 100.0
        self.music.bind(on_stop=self.sound_replay)
        self.music.play()
        
        # load all other sounds:
        self.sound['switch'] = SoundLoader.load('sound/switch.ogg')
        self.sound['select'] = SoundLoader.load('sound/select.ogg')
        self.sound['reset'] = SoundLoader.load('sound/reset.ogg')
        self.sound['beep'] = SoundLoader.load('sound/beep.ogg')
        
        self.sound['bullet_start'] = SoundLoader.load('sound/bullet_start.ogg')
        self.sound['explosion'] = SoundLoader.load('sound/explosion.ogg')
        self.sound['accomplished'] = SoundLoader.load('sound/accomplished.ogg')
        
        self.sound['no_deflector'] = SoundLoader.load('sound/no_deflector.ogg')
        self.sound['deflector_new'] = SoundLoader.load('sound/deflector_new.ogg')
        self.sound['deflector_down'] = SoundLoader.load('sound/deflector_down.ogg')
        self.sound['deflector_up'] = SoundLoader.load('sound/deflector_up.ogg')
        self.sound['deflector_delete'] = SoundLoader.load('sound/deflector_delete.ogg')
        self.sound['deflection'] = SoundLoader.load('sound/deflection.ogg')
        
        sound_volume = self.config.getint('General', 'Sound') / 100.0
        for item in self.sound:
            self.sound[item].volume = sound_volume
        
        # continue on the last level which wasn't finished
        level_opened = False
        for counter, char  in enumerate(self.config.get('GamePlay', 'Levels')):
            # if I found a level not yet done, continue with that
            if char == '0':
                self.deflectouchwidget.load_level(counter + 1)
                level_opened = True
                break
        
        # if all levels were completed, just open the last one.
        if level_opened == False:
            self.deflectouchwidget.load_level(40)
        
        # if the user started the game the first time, display quick start guide
        if self.config.get('General', 'FirstStartup') == 'Yes':
            
            Clock.schedule_once(self.welcome_screen, 2)
            
            self.config.set('General', 'FirstStartup', 'No')
            self.config.write()
    
   
    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'Music', '40')
        config.setdefault('General', 'Sound', '100')
        config.setdefault('General', 'FirstStartup', 'Yes')
        
        config.adddefaultsection('GamePlay')
        config.setdefault('GamePlay', 'BulletSpeed', '10')
        config.setdefault('GamePlay', 'Levels', '0000000000000000000000000000000000000000')
    
    def welcome_screen(self, instance):
        self.root.display_help_screen()
    
    def sound_replay(self, instance):
        if self.music.status != 'play':
            self.music.play()


if __name__ in ('__main__', '__android__'):
    Deflectouch().run()
    
