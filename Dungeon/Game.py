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
HEIGHT = 500 #At least 500 for window size
WIDTH = HEIGHT - 60
fHEIGHT = HEIGHT - WIDTH
pygame.init()
pygame.key.set_repeat()
manager = pygame_gui.UIManager((WIDTH,HEIGHT))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
time_delta = clock.tick(60)/1000.0
#manager.process_events(event)

##Initial Game Values##
#Gets valid sizes for floors based on screen size
usableSizes = [] 
for i in range(3,screen.get_width()):
    if screen.get_width()%i == 0:
        usableSizes.append(i)
print(usableSizes)

#Intializes global variables for tracking proogress
floorLevel = 0
score = 0
floorScore = 0
scoreRecord = []

#Set new player and floor
p = Player.Player()
f = Floor.Floor(usableSizes[floorLevel])
f.floorBase(screen, fHEIGHT)

#Set player position to start position.
p.posGrid = f.startPos
p.pos = f.floorMap[p.posGrid[0]][p.posGrid[1]].pos


##Main Function##
def main():
    running = True
    ##Calls sequence every frame##
    while running:  
        input()
        setUI()
        drawScreen()
        checkClear()
        manager.update(time_delta)  
    pygame.quit()    
    pass

##UI Functions##
def setUI():
    ##UI Setup##
    # key: [x,y,text,UILabel]
    uiElements = [[0,0,'Score: ' + str(score),pygame_gui.elements.UILabel],
                  [1,0,'Pos: ' + str(p.posGrid),pygame_gui.elements.UILabel],
                  [2,0,'Floor: ' + str(floorLevel),pygame_gui.elements.UILabel],
                  [0,1,'HP: ' + str(p.HP),pygame_gui.elements.UILabel],
                  [1,1,'[N,S,E,W]: ' + p.surroundingTiles(f),pygame_gui.elements.UILabel],
                  [0,2,'Feed: ', pygame_gui.elements.UILabel]
                  ]
    #Clears all UI elements 
    manager.clear_and_reset()
    #Initializes UI elements
    
    for element in uiElements:
        if element == uiElements[4]:
            uiElements[4][3] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((element[0] * WIDTH/3, element[1]*fHEIGHT/3), (WIDTH*2/3, fHEIGHT/3)),
                                             text=element[2],
                                             manager=manager)
        elif element == uiElements[5]:
            uiElements[5][3] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((element[0] * WIDTH/3, element[1]*fHEIGHT/3), (WIDTH, fHEIGHT/3)),
                                             text=element[2],
                                             manager=manager)
        else:
            element[3] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((element[0] * WIDTH/3, element[1]*fHEIGHT/3), (WIDTH/3, fHEIGHT/3)),
                                             text=element[2],
                                             manager=manager)     
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
    
##Input Function##
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
    #effect = p.checkPos(f)
    #floorScore += effect[0]
    #p.HP += effect[1]
    pass

main()