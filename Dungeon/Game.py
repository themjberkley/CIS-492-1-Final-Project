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
import Enemy

##Pygame Setup##
HEIGHT = 500 #At least 500 for window size
WIDTH = HEIGHT - 40
fHEIGHT = HEIGHT - WIDTH
pygame.init()
pygame.key.set_repeat()
manager = pygame_gui.UIManager((WIDTH,HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
time_delta = clock.tick(60)/1000.0
            #manager.process_events(event)


##UI Setup##
uiElements = {"Position": [0,pygame_gui.elements.UILabel],
              "Stats": [1,pygame_gui.elements.UILabel],
              "Floor": [2,pygame_gui.elements.UILabel]}

##Initial Game Values##
#Gets valid sizes for floors based on screen size
usableSizes = [] 
for i in range(3,screen.get_width()):
    if screen.get_width()%i == 0:
        usableSizes.append(i)
print(usableSizes)

#Intializes global variables for tracking proogress
floorLevel = 0
enemiesDefeated = 0
bossesDefeated = 0

#Set new player and floor
p = Player.Player()
f = Floor.Floor(usableSizes[floorLevel])
f.floorBase(screen, fHEIGHT)

#Set player position to start position.
p.posGrid = f.startPos
p.pos = f.floorMap[p.posGrid[0]][p.posGrid[1]].pos

def main():
    running = True
    ##Calls sequence every frame##
    while running:     
        input()
        setUI()
        drawScreen()
        checkClear()
        #print(p.pos)
        #print(p.posGrid)
    pygame.quit()    
    pass

def setUI():
    #Initializes UI elements
    uiElements["Position"][1] = pygame_gui.elements.UILabel(text='Pos: ' + str(p.pos),
                                                            relative_rect=pygame.Rect(((uiElements["Position"][0] * WIDTH/uiElements.__len__()), 0), (WIDTH/uiElements.__len__(), fHEIGHT)),
                                                            manager=manager)
    uiElements["Stats"][1] = pygame_gui.elements.UILabel(text=p.printStats(),
                                                        relative_rect=pygame.Rect(((uiElements["Stats"][0] * WIDTH/uiElements.__len__()), 0), (WIDTH/uiElements.__len__(), fHEIGHT)),
                                                        manager=manager)
    uiElements["Floor"][1] = pygame_gui.elements.UILabel(text='Floor: ' + str(floorLevel),
                                                        relative_rect=pygame.Rect(((uiElements["Floor"][0] * WIDTH/uiElements.__len__()), 0), (WIDTH/uiElements.__len__(), fHEIGHT)),
                                                        manager=manager)        
    pass

def updateUI():
    #Update UI
    global uiElements
    uiElements["Position"]
    uiElements["Position"][1].text = 'Pos: ' + str(p.pos)
    uiElements["Stats"][1].text= p.printStats()
    uiElements["Floor"][1].text= 'Floor: ' + str(floorLevel)
    manager.update(time_delta)
    print(p.pos)
    pass

def drawScreen():
    screen.fill("Black")
    #Draws Floor, Player, and UI
    f.drawFloor(screen, fHEIGHT)
    p.drawPlayer(screen,f)
    manager.draw_ui(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()
    # update() the display to update image on screen
    pygame.display.update()
    pass

#f:Floor.Floor, p:Player.Player
def checkClear():
    global p,f, floorLevel
    if f.endPos == p.posGrid:
        floorLevel += 1
        f = Floor.Floor(usableSizes[floorLevel])
        f.floorBase(screen, fHEIGHT)
        p.posGrid = f.startPos
        p.pos = f.floorMap[p.posGrid[0]][p.posGrid[1]].pos
        print("New Floor")
        print(floorLevel)
    else:
        pass    
    pass
    

def input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.QUIT:
                    running = False
                case pygame.K_w:        
                    ##MOVE UP##
                    #Checks Bounds
                    if p.posGrid[0] - 1 < 0:
                        pass
                    else:
                        p.posGrid[0] -= 1
                case pygame.K_s:
                    #MOVE DOWN##
                    #Checks Bounds
                    if p.posGrid[0] + 1 > f.size-1:
                        pass
                    else:
                        p.posGrid[0] += 1
                case pygame.K_a:
                    ##MOVE LEFT##
                    #Checks Bounds
                    if p.posGrid[1] - 1 < 0:
                        pass
                    else:
                        p.posGrid[1] -= 1
                case pygame.K_d:
                    ##MOVE RIGHT##
                    #Checks Bounds
                    if p.posGrid[1] + 1 > f.size-1:
                        pass
                    else:
                        p.posGrid[1] += 1
            #Sets new position and makes tile visible
            f.floorMap[p.posGrid[0]][p.posGrid[1]].visible = True
            p.pos = f.floorMap[p.posGrid[0]][p.posGrid[1]].pos
    pass


main()