#Player Class and Methods
import pygame as pg
import Floor
import Tile

class Player:
    HP:int
    COLOR = "Black"
    pos:pg.Vector2
    posGrid = [] #[y,x]

    def __init__(self):
        self.max_hp = 5
        self.HP = self.max_hp

    def drawPlayer(self, screen, f:Floor):
        # Fixed screen.width to screen.get_width() to ensure compatibility
        pg.draw.circle(screen, "black", (self.pos[0] + ((screen.get_width()/f.size)/2),self.pos[1] + ((screen.get_height()/f.size)/2)), ((screen.get_width()/f.size)/4))

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

        surrTiles = {'Up': nTile, 'Down': sTile, 'Left': wTile, 'Right': eTile}
        return surrTiles

    def apply_tile_effect(self, tile:Tile.Tile):
        """Adjust HP based on the tile type and return the delta and a short label."""
        hp_delta = 0
        event = ""
        
        if tile.type == "Trap":
            hp_delta = -1
            event = "Red tile dealt 1 HP of damage."
        elif tile.type == "Heal":
            if self.HP < self.max_hp:
                hp_delta = 1
                event = "Light blue tile restored 1 HP."
            else:
                event = "Already at full HP."
        
        # Apply HP change and clamp between 0 and max
        if hp_delta != 0:
            self.HP = max(0, min(self.max_hp, self.HP + hp_delta))
            
        return hp_delta, event

    def is_alive(self):
        return self.HP > 0
