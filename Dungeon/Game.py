#Game.py
#Michael Berkley
#Imports all classes and manages interactions.

##Imports##
#Pygame Imports
import pygame
import pygame_gui
import sys
#Class Imports
import Floor
import Tile
import Player

##Pygame Setup##
WIDTH = 600
UI_HEIGHT = 150
HEIGHT = WIDTH + UI_HEIGHT
fHEIGHT = UI_HEIGHT

pygame.init()
pygame.font.init()
pygame.key.set_repeat()

manager = pygame_gui.UIManager((WIDTH,HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
time_delta = 0
summary_font = pygame.font.SysFont("arial", 26)

##Initial Game Values##
#Gets valid sizes for floors based on screen size
usableSizes = []
for i in range(3, WIDTH):
    if WIDTH % i == 0:
        usableSizes.append(i)

print(usableSizes)

#Intializes global variables for tracking progress
floorLevel = 0
score = 0
scoreRecord = []
floor_stats = {"lost": 0, "gained": 0}
feed_text = "Find the orange tile to advance."
game_state = "playing"
summary_data = None

#Set new player and floor
p = Player.Player()
f = None

def load_floor(level_index:int):
    global f, floorLevel, floor_stats, feed_text
    size_index = level_index % len(usableSizes)
    floorLevel = level_index
    f = Floor.Floor(usableSizes[size_index], difficulty_level=level_index)
    f.floorBase(screen, fHEIGHT)
    p.posGrid = f.startPos.copy()
    current_tile = f.floorMap[p.posGrid[0]][p.posGrid[1]]
    current_tile.visible = True
    p.pos = current_tile.pos
    floor_stats = {"lost": 0, "gained": 0}
    feed_text = f"Floor {floorLevel + 1}: Find the Goal."
    return True

load_floor(0)

##Main Function##
def main():
    running = True
    ##Calls sequence every frame##
    while running:
        time_delta = clock.tick(60)/1000.0
        input()
        if game_state == "playing":
            checkClear()
            setUI()
            manager.update(time_delta)
            drawScreen()
        
    pygame.quit()
    pass

##UI Functions##
def setUI():
    ##UI Setup##
    surroundings = p.surroundingTiles(f)
    surroundings_text = (
        f"Surroundings<br>"
        f"Up: {surroundings['Up']} Down: {surroundings['Down']}<br>"
        f"Left: {surroundings['Left']} Right: {surroundings['Right']}"
    )

    # key: [x,y,text,ElementClass, width_ratio]
    # Grid is 3x2 (3 columns, 2 rows in the UI area)
    # Row 0: Score, Pos, Floor
    # Row 1: HP, Surroundings (spanning 2 cols)
    
    #Clear current UI
    manager.clear_and_reset()
    
    #Split UI into 3 rows
    row_h = fHEIGHT / 3
    
    # Row 0
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, 0), (WIDTH/3, row_h)),
        text='Score: ' + str(score),
        manager=manager
    )
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((WIDTH/3, 0), (WIDTH/3, row_h)),
        text='Pos: ' + str(p.posGrid),
        manager=manager
    )
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((WIDTH*2/3, 0), (WIDTH/3, row_h)),
        text='Floor: ' + str(floorLevel + 1),
        manager=manager
    )
    
    # Row 1
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, row_h), (WIDTH/3, row_h)),
        text='HP: ' + str(p.HP) + '/' + str(p.max_hp),
        manager=manager
    )
    
    # Surroundings Box - spanning 2 cols
    pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((WIDTH/3, row_h), (WIDTH*2/3, row_h*2)),
        html_text=surroundings_text,
        manager=manager
    )
    
    # Feed
    pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((0, row_h*2), (WIDTH/3, row_h)),
        text='Feed: ' + feed_text,
        manager=manager,
        object_id='#feed_label' # Optional styling
    )    
    pass

def drawScreen():
    screen.fill("Black")
    #Draws Floor, Player, and UI
    f.drawFloor(screen, fHEIGHT)
    p.drawPlayer(screen,f)
    manager.draw_ui(screen)
    
    if game_state == "summary":
        draw_summary_overlay()

    pygame.display.flip()
    pygame.display.update()
    pass

def draw_summary_overlay():
    if summary_data is None: return
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    status_line = "Level Complete!" if summary_data.get("advance", True) else "Out of HP!"
    next_floor_index = summary_data.get("next_floor", floorLevel)
    if next_floor_index >= len(usableSizes):
        next_level_text = "Next Level: All floors cleared!"
    else:
        next_level_text = f"Next Level: Floor {next_floor_index + 1}"
        
    lines = [
        status_line,
        summary_data.get("message", ""),
        f"HP Remaining: {summary_data.get('hp_left', p.HP)}/{p.max_hp}",
        f"HP Lost: {summary_data.get('hp_lost', 0)}",
        f"HP Regained: {summary_data.get('hp_gained', 0)}",
        f"Score: {summary_data.get('score', score)}",
        next_level_text,
        "Press SPACE or ENTER to continue."
    ]
    
    for idx, line in enumerate(lines):
        text_surface = summary_font.render(line, True, pygame.Color('white'))
        screen.blit(text_surface, (WIDTH * 0.08, HEIGHT * 0.25 + idx * 32))

def checkClear():
    if f.endPos == p.posGrid:
        start_floor_summary("You found the goal!", advance=True)
    pass

def start_floor_summary(message:str, advance:bool=True, next_floor_override:int | None = None):
    global summary_data, game_state, feed_text
    if next_floor_override is not None:
        next_floor_target = next_floor_override
    else:
        next_floor_target = floorLevel + 1 if advance else floorLevel
        
    summary_data = {
        "floor": floorLevel,
        "hp_left": p.HP,
        "hp_lost": floor_stats.get("lost", 0),
        "hp_gained": floor_stats.get("gained", 0),
        "score": score,
        "message": message,
        "advance": advance,
        "next_floor": next_floor_target
    }
    feed_text = message
    game_state = "summary"

def handle_summary_continue():
    global summary_data, game_state
    if summary_data is None: return
    next_floor_index = summary_data.get("next_floor", floorLevel)
    advance = summary_data.get("advance", True)
    summary_data = None
    
    if not advance:
        p.HP = p.max_hp
        
    load_floor(next_floor_index)
    game_state = "playing"

def move_player(delta_row:int, delta_col:int):
    global feed_text
    if game_state != "playing": return
    
    new_row = p.posGrid[0] + delta_row
    new_col = p.posGrid[1] + delta_col
    
    if new_row < 0 or new_row >= f.size or new_col < 0 or new_col >= f.size:
        feed_text = "You can't move outside the floor."
        return
        
    p.posGrid = [new_row, new_col]
    tile = f.floorMap[new_row][new_col]
    tile.visible = True
    p.pos = tile.pos
    feed_text = f"{tile.type} tile."
    apply_tile_effect(tile)

def apply_tile_effect(tile:Tile.Tile):
    global feed_text, floor_stats
    if tile.type == "End":
        feed_text = "You found the goal!"
    
    if not tile.active:
        if tile.type not in ("Nothing", "Start", "End"):
            feed_text = "This tile is inactive."
        return
        
    messages = []
    hp_delta, event = p.apply_tile_effect(tile)
    if hp_delta < 0:
        floor_stats["lost"] += abs(hp_delta)
    elif hp_delta > 0:
        floor_stats["gained"] += hp_delta
        
    if event:
        messages.append(event)
        
    score_msg = handle_score_effect(tile)
    if score_msg:
        messages.append(score_msg)
        
    if messages:
        feed_text = " ".join(messages)
        
    tile.active = False
    
    if not p.is_alive():
        start_floor_summary("You ran out of HP and will restart on Floor 1.", advance=False, next_floor_override=0)

def handle_score_effect(tile:Tile.Tile):
    global score
    message = ""
    if tile.type == "Treasure":
        score += 100
        message = "Blue tile, +100 points."
    elif tile.type == "SilverBonus":
        start_score = score
        score = int(round(score * 1.5))
        if start_score > 0:
            message = f"Silver; 1.5xScore to {score}."
    elif tile.type == "GoldBonus":
        start_score = score
        score = int(round(score * 2))
        if start_score > 0:
            message = f"Gold; 2xScore to {score}."
    elif tile.type == "Cursed":
        start_score = score
        score = int(round(score * 0.5))
        if start_score > 0:
            message = f"Purple; .5xScore to {score}."
    return message

##Input Function##
def input():
    for event in pygame.event.get():
        manager.process_events(event)
        if event.type == pygame.QUIT:
            sys.exit()
            
        if game_state == "summary":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                handle_summary_continue()
            continue
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move_player(-1, 0)
            elif event.key == pygame.K_s:
                move_player(1, 0)
            elif event.key == pygame.K_a:
                move_player(0, -1)
            elif event.key == pygame.K_d:
                move_player(0, 1)
            elif event.key == pygame.K_ESCAPE:
                sys.exit()

main()
