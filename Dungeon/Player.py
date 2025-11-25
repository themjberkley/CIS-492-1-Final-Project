#Player Class and Methods
import pygame as pg
import Floor

class Player:
    HP:int
    COLOR = "Black"
    pos:pg.Vector2
    posGrid = [] #[y,x]
    
    def __init__(self):
        self.HP = 10
    
    def drawPlayer(self, screen, f:Floor):
        pg.draw.circle(screen, "black", (self.pos[0] + ((screen.get_width()/f.size)/2),self.pos[1] + ((screen.get_height()/f.size)/2)), ((screen.width/f.size)/4))
        
    #def printStats(self):
    #    return "HP: " + str(self.HP) + " ATK: " + str(self.ATK) + " DEF: " + str(self.DEF)
    
    #def getPos(self):
     #   return self.posGrid
    

    
