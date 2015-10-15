from random import randint
import pygame as pg
import prepare
#http://www.clipartlord.com/wp-content/uploads/2013/12/pumpkin6.png


class Pumpkin(object):
    def __init__(self):
        self.flicker_time = 55
        self.image = prepare.GFX["pumpkin"]
        self.rect = self.image.get_rect(center=prepare.SCREEN_RECT.center)
        self.work_surf = pg.Surface(self.rect.size).convert()
        self.work_surf.fill((255, 255, 255))
        self.work_surf.set_colorkey((255, 255, 255))
        self.final = pg.Surface(self.image.get_size()).convert()
        self.final.set_colorkey(pg.Color(0, 0, 0))
        self.cover = prepare.GFX["pumpkin-cover"]
        self.timer = 0
        self.background = pg.Surface(self.image.get_size()).convert()
        self.background.set_colorkey((0, 0, 0))
        self.flicker()
        
    def reset(self):
        self.working_image = self.image.copy()

    def flicker(self):
        red = randint(210, 230)
        green = randint(150, 200)
        self.background.fill(pg.Color(red, green, 20))
        self.background.blit(self.cover, (0, 0))
    
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flicker_time:
            self.timer -= self.flicker_time
            self.flicker_time = randint(40, 100)
            self.flicker()
            
    def draw(self, surface):     
        self.final.blit(self.image, (0, 0))
        self.final.blit(self.work_surf, (0, 0))
        surface.blit(self.background, self.rect)
        surface.blit(self.final, self.rect)

        
