#Tile Class and Methods

import pygame as pg
#__TILES__ = ["Neutral", "Good","Lucky","Rest", "Bad", "Start", "End"] 

class Tile:
    visible:bool
    active:bool
    type:str
    color:str
    pos = pg.Vector2
    size = pg.rect
        
    def __init__(self):
        self.visible = False
        self.type = "Neutral"
        self.active = True
        
    def setVisible(self):
        self.visible = True
        
        
        