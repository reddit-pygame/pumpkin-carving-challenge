import pygame as pg
import prepare
from state_engine import GameState
from animation import Animation
from pumpkin import Pumpkin


class Carving(GameState):
    def __init__(self):
        super(Carving, self).__init__()
        self.brush_size = 8
        self.drawing = False
        self.pumpkin = Pumpkin()
        self.history = [] #
        self.line_start = None
        self.shade = pg.Surface(prepare.SCREEN_SIZE).convert()
        self.shade.fill(pg.Color(10, 5, 20))
        self.shade_alpha = 255
        self.shade.set_alpha(self.shade_alpha)
        self.animations = pg.sprite.Group()
        
    def save_work_surf(self): #
        self.history.append(self.pumpkin.work_surf.copy())
        
    def undo(self): #
        try:
            previous = self.history.pop()    
            self.pumpkin.work_surf = previous
        except IndexError:
            pass
    
    def startup(self, persistent):
        self.persist = persistent
        self.shade_alpha = 255
        ani = Animation(shade_alpha=0, duration=3000,
                                round_values=True, transition="linear")
        ani.start(self)
        self.animations.add(ani)
        
    def get_event(self, event):        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.drawing = True
                self.save_work_surf() #
                self.line_start = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False
                                
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.brush_size += 1
            elif event.key == pg.K_DOWN:
                self.brush_size = max(2, self.brush_size - 1)
            elif event.key == pg.K_z and pg.key.get_pressed()[pg.K_LCTRL]: #
                self.undo() #
                
    def update(self, dt):        
        if self.drawing:
            mx, my = pg.mouse.get_pos()
            px, py = self.pumpkin.rect.topleft
            line_start = self.line_start[0] - px, self.line_start[1] - py
            pos = mx - px, my - py
            pg.draw.line(self.pumpkin.work_surf, pg.Color(0, 0, 0), line_start,
                               pos, self.brush_size*2 + 3)
            pg.draw.circle(self.pumpkin.work_surf, pg.Color(0, 0, 0), line_start, self.brush_size)
            pg.draw.circle(self.pumpkin.work_surf, pg.Color(0, 0, 0), pos, self.brush_size)
            self.line_start = mx, my
        if self.shade_alpha > 0:
            self.shade.set_alpha(self.shade_alpha)        
        self.pumpkin.update(dt)
        self.animations.update(dt)
        
    def draw(self, surface):
        surface.fill(pg.Color(10, 5, 20))
        self.pumpkin.draw(surface)
        if not self.drawing:
            pg.draw.circle(surface, pg.Color("white"), pg.mouse.get_pos(), self.brush_size, 1)
        if self.shade_alpha > 0:
            surface.blit(self.shade, (0, 0))