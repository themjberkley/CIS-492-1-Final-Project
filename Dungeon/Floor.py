import sys
import pygame as pg
import random
import Tile

class Floor:
    #Variables
    size:int #Area of floor (size x size) should be multiple of square display
    floorMap:list[list[Tile.Tile]] #List fo every tile on the map
    startPos = [int,int] #[y,x]
    endPos = [int,int] #[y,x]
    
    
    def __init__(self, s:int):
        self.size = s
        self.floorMap = []
        #Sets starting and ending point of maze
        self.startPos = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
        self.endPos = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
    
    def floorBase(self,screen, yOff):
        #Places random tile on floorMap
        for row in range(0,self.size):
            r = []
            for col in range(0,self.size):
                t = Tile.Tile()
                if [row,col] == self.startPos:
                    t.visible = True
                    t.type = "Start"
                    t.active = True
                    t.color = "Green"
                elif [row,col] == self.endPos:
                    t.visible = False
                    t.type = "End"
                    t.active = True
                    t.color = "White"
                else:
                    randTile = random.randint(0,7)
                    t.visible = False
                    t.active = True    
                    match randTile:
                        #0 = Neutral, 1 = Good, 2 = Bad, 3 = Lucky, 4 = Super Lucky, 5 = Battle, 6 = Hard Battle, 7 = Rest
                        case 0:
                            t.type = "Neutral"
                            t.active = False    
                            t.color = "Dark Gray"
                        case 1:
                            t.type = "Good"
                            t.color = "Blue"
                        case 2:
                            t.type = "Bad"
                            t.color = "Red"
                        case 3:
                            t.type = "Lucky"
                            t.color = "Silver"
                        case 4:
                            t.type = "Super Lucky"
                            t.color = "Gold"
                        case 5:
                            t.type = "Battle"
                            t.color = "Orange"
                        case 6:
                            t.type = "Hard Battle"
                            t.color = "Pink"
                        case 7:
                            t.type = "Rest"
                            t.color = "Cyan"
                t.pos = pg.Vector2((screen.get_width()/self.size) * col, (((screen.get_height() - yOff)/self.size) * row) + yOff)
                r.append(t)
                print(row, col, t.type)
            self.floorMap.append(r)
    
    #Draws floor to screen                         
    def drawFloor(self,screen, yOff):
        for row in self.floorMap:
            for tile in row:
                if tile.visible == True:
                    pg.draw.rect(screen,tile.color,(tile.pos.x, tile.pos.y, screen.get_width()/self.size, ((screen.get_height() - yOff)/self.size)))
                else:
                    pass
 