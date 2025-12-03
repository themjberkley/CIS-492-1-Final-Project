import sys
import pygame as pg
import random
import Tile

START_COLOR = (46, 204, 113)
GOAL_COLOR = (255, 140, 0)
NOTHING_COLOR = (85, 85, 85)
TREASURE_COLOR = (30, 136, 229)
TRAP_COLOR = (204, 32, 32)
SILVER_COLOR = (198, 198, 198)
GOLD_COLOR = (255, 201, 14)
CURSED_COLOR = (146, 43, 226)
HEAL_COLOR = (173, 235, 255)

class Floor:
    #Variables
    size:int #Area of floor (size x size) should be multiple of square display
    floorMap:list[list[Tile.Tile]] #List of every tile on the map
    startPos = [int,int] #[y,x]
    endPos = [int,int] #[y,x]
    
    BASE_TILE_POOL = [
        {"type": "Nothing", "color": NOTHING_COLOR, "active": False, "base_weight": 24},
        {"type": "Treasure", "color": TREASURE_COLOR, "active": True, "base_weight": 14},
        {"type": "Trap", "color": TRAP_COLOR, "active": True, "base_weight": 14},
        {"type": "SilverBonus", "color": SILVER_COLOR, "active": True, "base_weight": 9},
        {"type": "GoldBonus", "color": GOLD_COLOR, "active": True, "base_weight": 6},
        {"type": "Cursed", "color": CURSED_COLOR, "active": True, "base_weight": 10},
        {"type": "Heal", "color": HEAL_COLOR, "active": True, "base_weight": 17},
    ]

    def __init__(self, s:int, difficulty_level:int = 0):
        self.size = s
        self.floorMap = []
        self.difficulty_level = difficulty_level
        #Sets starting and ending point of maze
        self.startPos = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
        self.endPos = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
        while self.endPos == self.startPos:
            self.endPos = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
            
        self.safe_path = self._build_safe_path()
        self.tile_options = self._build_tile_options()

    def floorBase(self,screen, yOff):
        #Places random tiles on floorMap
        for row in range(0,self.size):
            r = []
            for col in range(0,self.size):
                t = Tile.Tile()
                current_pos = [row, col]
                if current_pos == self.startPos:
                    t.visible = True
                    t.type = "Start"
                    t.active = True
                    t.color = START_COLOR
                elif current_pos == self.endPos:
                    t.visible = False
                    t.type = "End"
                    t.active = True
                    t.color = GOAL_COLOR
                else:
                    t.visible = False
                    tile_type, color, is_active = self._random_tile_definition(current_pos)
                    t.type = tile_type
                    t.active = is_active
                    t.color = color
                
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

    def _random_tile_definition(self, position:list[int]):
        if tuple(position) in self.safe_path:
            return "Nothing", NOTHING_COLOR, False
            
        weights = [option["weight"] for option in self.tile_options]
        choice = random.choices(self.tile_options, weights=weights, k=1)[0]
        return choice["type"], choice["color"], choice["active"]

    def _build_safe_path(self):
        path = set()
        current = self.startPos.copy()
        path.add(tuple(current))
        max_steps = self.size * self.size * 4
        steps = 0
        
        while current != self.endPos and steps < max_steps:
            steps += 1
            directional_moves = []
            if current[0] < self.endPos[0]:
                directional_moves.append((1,0))
            elif current[0] > self.endPos[0]:
                directional_moves.append((-1,0))
                
            if current[1] < self.endPos[1]:
                directional_moves.append((0,1))
            elif current[1] > self.endPos[1]:
                directional_moves.append((0,-1))
                
            if not directional_moves:
                break
                
            move = random.choice(directional_moves)
            current = [current[0] + move[0], current[1] + move[1]]
            path.add(tuple(current))
            
        return path

    def _build_tile_options(self):
        options = []
        for option in self.BASE_TILE_POOL:
            adjusted_weight = self._adjusted_weight(option["type"], option["base_weight"])
            tile_option = option.copy()
            tile_option["weight"] = max(1, adjusted_weight)
            options.append(tile_option)
        return options

    def _adjusted_weight(self, tile_type:str, base_weight:int):
        d = self.difficulty_level
        weight = base_weight
        if tile_type == "Trap":
            weight += d * 4
        elif tile_type == "Cursed":
            weight += d * 2
        elif tile_type == "Heal":
            weight = max(5, weight - d * 2)
        elif tile_type == "Treasure":
            weight = max(4, weight - d)
        elif tile_type == "Nothing":
            weight = max(6, weight - d)
        elif tile_type == "GoldBonus":
            weight += max(0, d - 1)
        elif tile_type == "SilverBonus":
            weight += max(0, d // 2)
        return weight
