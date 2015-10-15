import pygame as pg
import prepare
from state_engine import GameState
from pumpkin import Pumpkin


class Carving(GameState):
    def __init__(self):
        super(Carving, self).__init__()
        self.brush_size = 8
        self.drawing = False
        self.pumpkin = Pumpkin()
        self.history = []
        
    def save_work_surf(self):
        self.history.append(self.pumpkin.work_surf.copy())
        
    def undo(self):
        try:
            previous = self.history.pop()    
            self.pumpkin.work_surf = previous
        except IndexError:
            pass
    
    def startup(self, persistent):
        self.persist = persistent
        
    def get_event(self, event):        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.drawing = True
                self.save_work_surf()
            elif event.button == 3:
                self.pumpkin.reset()
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.drawing = False            
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.brush_size += 1
            elif event.key == pg.K_DOWN:
                self.brush_size = max(2, self.brush_size - 1)
            elif event.key == pg.K_z and pg.key.get_pressed()[pg.K_LCTRL]:
                self.undo()
                
    def update(self, dt):        
        if self.drawing:
            mx, my = pg.mouse.get_pos()
            px, py = self.pumpkin.rect.topleft
            pos = mx - px, my - py
            pg.draw.circle(self.pumpkin.work_surf, pg.Color(0, 0, 0), pos, self.brush_size)
        self.pumpkin.update(dt)
        
    def draw(self, surface):
        surface.fill(pg.Color(5, 5, 20))
        self.pumpkin.draw(surface)
        if not self.drawing:
            pg.draw.circle(surface, pg.Color("white"), pg.mouse.get_pos(), self.brush_size, 1)