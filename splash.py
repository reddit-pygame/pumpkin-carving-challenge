from math import radians, cos, sin
from random import randint, shuffle, choice
from itertools import cycle
import json
import pygame as pg

import prepare
import tools
from state_engine import GameState
from animation import Task, Animation


def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
        adjusted for pygame's y-axis"""
    return (pos[0] + (cos(angle) * distance),
                pos[1] - (sin(angle) * distance))
                

class Bat(object):
    def __init__(self, pos, angle):
        self.idle_image = prepare.GFX["bat-idle"]
        imgs = prepare.GFX["bat1"], prepare.GFX["bat2"]
        if 90 <= angle <= 270:
            rot_angle = angle - 180 
            imgs = [pg.transform.flip(img, True, False) for img in imgs]        
        else:
            rot_angle = angle
        self.angle = radians(angle)
        images = [pg.transform.rotate(image, rot_angle) for image in imgs]
        self.images = cycle(images)
        self.image = self.idle_image
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0
        self.flap_time = randint(60, 100)
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flap_time:
            self.timer -= self.flap_time
            self.image = next(self.images)
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
        
class Splash(GameState):
    def __init__(self):
        super(Splash, self).__init__()
        self.animations = pg.sprite.Group()
        self.animations.add(Task(self.wake_bats, 6000))
        self.timer  = 0
        with open("bat_spots.json", "r") as f:
            points = json.load(f)
            shuffle(points)
        self.bats = [Bat(point, randint(0, 360)) for point in points]
        self.web = prepare.GFX["web"]
        self.web_rect = self.web.get_rect(center=prepare.SCREEN_RECT.center)
        
        self.shade = pg.Surface(prepare.SCREEN_SIZE).convert()
        self.shade.fill(pg.Color("gray1"))
        self.shade_alpha = 255
        
        self.flash_timer = 0
        self.flash_time = 120
        self.thunder_sounds = [prepare.SFX["thunder{}".format(x)] for x in range(1, 5)]
        pg.mixer.music.load(prepare.MUSIC["CrEEP"])
        pg.mixer.music.play()
        
    def flash(self):
        dur = randint(60, 100)
        ani = Animation(shade_alpha=0, duration=dur, transition="linear",
                                round_values=True)
        ani2 = Animation(shade_alpha=240, duration=dur, delay=dur, 
                                  transition="linear", round_values=True)
        ani.start(self)
        ani2.start(self)
        self.animations.add(ani, ani2)
        self.flash_time = randint(150, 350)
        choice(self.thunder_sounds).play()
        
    def wake_bats(self):
        transitions = ("in_expo", "in_quad", "in_quint", "in_cubic")
        fly_time = 4500
        for bat in self.bats:        
            bat.image = next(bat.images)
            bat.rect = bat.image.get_rect(center=bat.rect.center)            
            dest = project(bat.rect.center, bat.angle, 1200)
            ani = Animation(centerx=dest[0], centery=dest[1], duration=fly_time, round_values=True, transition=choice(transitions))
            self.animations.add(ani)
            ani.start(bat.rect)
            
    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.bats.append(Bat(event.pos, 0))
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                with open("bat_spots.json", "w") as f:
                    json.dump([bat.rect.center for bat in self.bats], f)
                
       
    def update(self, dt):
        self.timer += dt
        self.flash_timer += dt
        if self.timer >= 6000:
            for bat in self.bats:
                bat.update(dt)
        if self.timer > 11000:
            self.done = True
            self.next_state = "CARVING"
        if self.flash_timer >= self.flash_time:
            self.flash()
            self.flash_timer -= self.flash_time
         
        self.animations.update(dt)
        self.shade.set_alpha(self.shade_alpha)   
                
    def draw(self, surface):
        surface.fill(pg.Color(5, 5, 15))
        surface.blit(self.web, self.web_rect)
        for bat in self.bats:
            bat.draw(surface)
        surface.blit(self.shade, (0, 0))    
        