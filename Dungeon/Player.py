#Player Class and Methods
import pygame as pg
import random
import Floor

class Player:
    HP:int
    COLOR = "Black"
    pos:pg.Vector2
    posGrid = [] #[y,x]
    
    def __init__(self):
        self.HP = 3
    
    def drawPlayer(self, screen, f:Floor):
        pg.draw.circle(screen, "black", (self.pos[0] + ((screen.get_width()/f.size)/2),self.pos[1] + ((screen.get_height()/f.size)/2)), ((screen.width/f.size)/4))
        
    def surroundingTiles (self, f:Floor):
        surrTiles = []
        #North
        if self.posGrid[0] == 0:
            nTile = "Edge"
        else:
            nTile = f.floorMap[self.posGrid[0] - 1][self.posGrid[1]].type
        #South
        try:
            sTile = f.floorMap[self.posGrid[0] + 1][self.posGrid[1]].type
        except IndexError:
            sTile = "Edge"
        #West
        if self.posGrid[1] == 0:
            wTile = "Edge"
        else:
            wTile = f.floorMap[self.posGrid[0]][self.posGrid[1] - 1].type
        #East
        try:
            eTile = f.floorMap[self.posGrid[0]][self.posGrid[1] + 1].type
        except IndexError:
            eTile = "Edge"
            
        surrTiles = [nTile,sTile,eTile,wTile]
        #random.shuffle(surrTiles)
        return str(surrTiles)
    
    def checkPos(f:Floor):
        
        pass
        
    #def printStats(self):
    #    return "HP: " + str(self.HP) + " ATK: " + str(self.ATK) + " DEF: " + str(self.DEF)
    
    #def getPos(self):
     #   return self.posGrid
    

    
