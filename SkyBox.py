import pygame, pygame.font, pygame.event, pygame.draw
from pygame.locals import *
import os
import Render
import Planets
import Gravity
import math
pygame.init()

x = 200
y = 45
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

PlayImage = pygame.image.load("Play.png")
Play = pygame.transform.scale(PlayImage, (100, 100))

PauseImage = pygame.image.load("Pause.png")
Pause = pygame.transform.scale(PauseImage, (120, 120))

TrashImage = pygame.image.load("Trash.png")
Trash = pygame.transform.scale(TrashImage, (100, 100))

PlanetImage = pygame.image.load("Planet.png")
Planet = pygame.transform.scale(PlanetImage, (150, 150))

StarImage = pygame.image.load("Star.png")
Star = pygame.transform.scale(StarImage, (180, 180))

EyeImage = pygame.image.load("Eye.png")
Eye = pygame.transform.scale(EyeImage, (39,26))

Black = [0, 0, 0]
White = [255, 255, 255]
Red = [255, 0, 0]
Green = [0, 255, 0]
Blue = [0, 0, 255]
Light_Blue = [102, 255, 255]

arial_font = pygame.font.SysFont('arial', 30)
arial_font_small = pygame.font.SysFont('arial', 18)

VALID_KEYS = '0123456789 . -'

saveFile = "testSystem.txt"


def display_box(screen, message, r):
    fontobject = pygame.font.Font(None, 18)
    message_surface = fontobject.render(message, 1, Black)

    pygame.draw.rect(screen, Red, r, 0)
    pygame.draw.rect(screen, Black, r, 1)
    if len(message) != 0:
        screen.blit(message_surface, (r[0] + 3, r[1] + 9))


def ask(screen, question, max_length, r):
    global inPlay
    pygame.font.init()
    if inputValues[inputBoxes.index(r)]:
        current_string = list(str(inputValues[inputBoxes.index(r)]))
    else:
        current_string = []
    display_box(screen, question + ": " + ''.join(current_string), r)
    enteringText = True
    while enteringText:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                enteringText = False
                inPlay = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    enteringText = False
                    inPlay = False
                if event.key == K_BACKSPACE:
                    current_string = current_string[0:-1]
                if chr(event.key) in VALID_KEYS:
                    inkeyLtr = chr(event.key)
                    current_string.append(inkeyLtr)
            if len(current_string) > max_length:
                current_string = current_string[0:-1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                newButtonInput = False
                newButtonOther = False
                for i, button in enumerate(all_buttons):
                    if pygame.Rect(button).collidepoint(clickPos):
                        if i < 6:
                            newButtonInput = True
                        else:
                            newButtonOther = True
                        break
                inputValues[inputBoxes.index(r)] = ''.join(current_string)
                if newButtonInput:
                    for i, inputBox in enumerate(inputBoxes):
                        if pygame.Rect(inputBox).collidepoint(clickPos):
                            ask(win, f'{inputLabels[i]}: ', 10, inputBox)
                elif newButtonOther:
                    for i, other_button in enumerate(other_buttons):
                        if pygame.Rect(other_button).collidepoint(clickPos):
                            #button management
                            if i == 0:
                                checkConfirm()
                            elif i == 1:
                                if 1 not in selected:
                                    selected.append(1)
                                
                                else:
                                    selected.remove(1)
                                stopPlanets(selected)
                            elif i == 2:
                                playSim = True
                                if 2 not in selected:
                                    if 3 in selected:
                                        selected.remove(3)
                                    selected.append(2)
                            elif i == 3:
                                playSim = False
                                if 3 not in selected:
                                    if 2 in selected:
                                        selected.remove(2)
                                    selected.append(3)
                            elif i == 4:
                                deleteSelected()
                            elif i == 7:
                                myPers.saveToFile(saveFile)
                            elif i == 8:
                                myPers.loadFromFile(saveFile)
                            
                enteringText = False

        display_box(screen, question + ''.join(current_string), r)
        pygame.display.flip()
    return ''.join(current_string)


def blitText(message, fontSize, x, y, center=False):
    defaultFont = pygame.font.SysFont('arial', fontSize)
    textSurface = defaultFont.render(message, True, Black)
    if center:
        x = win.get_width() // 2 + 500 - textSurface.get_width() // 2
    win.blit(textSurface, (x, y))


def drawButton(win, text, r, bColor, fColor, font):
    pygame.draw.rect(win, bColor, r)
    pygame.draw.rect(win, fColor, r, 3)
    txtSurface = font.render(text, True, fColor)
    win.blit(txtSurface, (r[0] + (r[2]-txtSurface.get_width())//2, r[1] + (r[3]-txtSurface.get_height())//2))


def checkConfirm():
    global errorMessage
    wrongList = []
    for i, input in enumerate(inputValues):
        if i != 8:
            try:
                inputValues[i] = float(input)
                if inputValues[i].is_integer():
                    inputValues[i] = int(inputValues[i])
            except ValueError:
                wrongList.append(inputLabels[i])
    try:
        inputValues[-1] = int(inputValues[-1])
        if not 1 <= inputValues[-1] <= 6:
            raise ValueError
    except ValueError:
        if inputLabels[-1] not in wrongList:
            wrongList.append(inputLabels[-1])
    '''try:
        if not 0 <= inputValues[8] <= 10:
            wrongList.append(inputLabels[8])
    except:
        wrongList.append(inputLabels[8])'''
    try:
        if not 0 <= inputValues[6]:
            if inputLabels[6] not in wrongList:
                wrongList.append(inputLabels[6])
    except:
        if inputLabels[6] not in wrongList:
            wrongList.append(inputLabels[6])
    if wrongList:
        s = ''
        for wrongInput in wrongList:
            s += f'{wrongInput}, '
        s = s[0:-2]
        if len(wrongList) == 1:
            s += ' is not inputted correctly.'
        else:
            s += ' are not inputted correctly.'
        errorMessage = s
    else:
        errorMessage = ''
        color = [255, 255, 255]
        if inputValues[9] == 1:
            color = [0, 0, 0]
        elif inputValues[9] == 2:
            color = [255, 255, 255]
        elif inputValues[9] == 3:
            color = [255, 0, 0]
        elif inputValues[9] == 4:
            color = [0, 255, 0]
        elif inputValues[9] == 5:
            color = [0, 0, 255]
        elif inputValues[9] == 6:
            color = [130, 130, 255]
        else:
            color = [255, 255, 255]
        myPers.grid.stuff.append(Planets.Entity([inputValues[1], inputValues[3], inputValues[5]], [inputValues[0], inputValues[2], inputValues[4]], inputValues[7], inputValues[6], color, 1+int(5 in selected)))
        if 1 not in selected:
            myPers.grid.stuff[-1].movable = False

def resetPerspective(myPers):
    myPers.anglex = 0
    myPers.angley = 0
    myPers.coords = [0, 20, 0]
def rotate(point,pivot,angle): #2d
    newXY = [0,0]
    rad = (((point[0] - pivot[0])**2) + ((point[1] - pivot[1])**2))**(1/2)
    if rad == 0:
        return pivot
    newAngle = math.acos((point[0] - pivot[0])/rad) + angle
    newXY[0] = pivot[0] + math.cos(newAngle)*rad
    newXY[1] = pivot[1] + math.sin(newAngle)*rad
    return newXY

radarRange = 200
def miniMap():
    viewing = myPers.checkLook()
    pygame.draw.circle (win, Black, (100,900) ,100)
    pygame.draw.line(win,White,(100,800), (100,1000))
    pygame.draw.line(win,White,(0,900), (200,900))
    newCoords = rotate((viewing[0]*20, viewing[1]*20), (0,0), math.pi/3)
    newCoords2 = rotate((viewing[0]*20, viewing[1]*20), (0,0), -math.pi/3)
    if viewing[1] < 0:
        pygame.draw.line(win,White,(100,900), (100 - round(newCoords[0]), 900 - round(newCoords[1])))
        pygame.draw.line(win,White,(100,900), (100 - round(newCoords2[0]), 900 - round(newCoords2[1])))
    else:
        pygame.draw.line(win,White,(100,900), (100 - round(newCoords[0]), 900 + round(newCoords[1])))
        pygame.draw.line(win,White,(100,900), (100 - round(newCoords2[0]), 900 + round(newCoords2[1])))

    zoom = pygame.font.SysFont('arial', 10).render(str(round(math.log(radarRange/50, 2))), True, White)
    win.blit (zoom, (2,885))
    for i in myPers.grid.stuff:
        if ((i.coords[0]**2) + (i.coords[1]**2))**(1/2) <= radarRange:
            if round(i.radius*100/radarRange) <= 0:
                vRadius = 0
            else:
                vRadius = round(i.radius*100/radarRange)
            pygame.draw.circle (win, i.color, (round(((i.coords[0]-myPers.coords[0])*100/radarRange) + 100), round(((i.coords[1]-myPers.coords[1])*100/radarRange) + 900)), vRadius)

def deleteSelected():
    for i in myPers.grid.stuff:
        if i.selected == True:
            i.alive = False

def stopPlanets(selected):
    for i in myPers.grid.stuff:
        if i.selected == True:
            i.movable = 1 in selected
            
def d2p(point1, point2):
    return (((point1[0]-point2[0])**2) + ((point1[1]-point2[1])**2))**(1/2)

def overlay(clickPos):
    pygame.draw.rect(win, White, (0, 800, 1000, 200))
    pygame.draw.rect(win, White, (1000, 0, 500, 1000))
    blitText('Planet', 30, 1082, 5)
    win.blit(Planet, (1050, 50))
    blitText('Star', 30, 1348, 5)
    win.blit(Star, (1285, 35))
    blitText('VELOCITY', 40, 1025, 210)
    blitText('POSITION', 40, 1280, 210)
    blitText('1: Black  2:   White   ', 20, 1275, 728)
    blitText('3: Red    4:   Green   ', 20, 1275, 758)
    blitText('5: Blue   6: Light Blue', 20, 1275, 788)

    if pygame.Rect(1025, 740, 200, 40).collidepoint(clickPos):
        drawButton(win, "Apply", (1025, 740, 200, 40), Red, Light_Blue, arial_font)

    else:
        drawButton(win, "Apply", (1025, 740, 200, 40), Red, Black, arial_font)
        
    if pygame.Rect(1150, 835, 200, 50).collidepoint(clickPos):
        drawButton(win, 'Confirm', (1150, 835, 200, 50), Red, Light_Blue, arial_font)

    else:
        confirm = drawButton(win, 'Confirm', (1150, 835, 200, 50), Red, Black, arial_font)

    if pygame.Rect(773, 875, 200, 50).collidepoint(clickPos):
        drawButton(win, 'Moveable', (773, 875, 200, 50), Red, Light_Blue, arial_font)

    else:
        drawButton(win, 'Moveable', (773, 875, 200, 50), Red, Black, arial_font)

    if pygame.Rect(1025, 925, 200, 50).collidepoint(clickPos):
        drawButton(win, 'Save', (1025, 925, 200, 50), Red, Light_Blue, arial_font)

    else:
        drawButton(win, 'Save', (1025, 925, 200, 50), Red, Black, arial_font)

    if pygame.Rect(1275, 925, 200, 50).collidepoint(clickPos):
        drawButton(win, 'Load', (1275, 925, 200, 50), Red, Light_Blue, arial_font)

    else:
        drawButton(win, 'Load', (1275, 925, 200, 50), Red, Black, arial_font)

    if d2p(clickPos, (470,900)) < 50:
        pygame.draw.circle(win,Light_Blue,(470,900),50)
    if d2p(clickPos, (630,900)) < 50:
        pygame.draw.circle(win,Light_Blue,(630,900),50)

        
    win.blit(Play, (420, 850))
    win.blit(Pause, (570, 840))
    win.blit(Trash, (250, 850))
    win.blit(Eye, (854, 840))
    
    textSurface = arial_font_small.render(errorMessage, True, Red)
    win.blit(textSurface, (win.get_width() // 2 - 100 - textSurface.get_width() // 2, 802))
    if 1 in selected:
        pygame.draw.circle(win, Green, (750, 900), 10)
    else:
        pygame.draw.circle(win, Red, (750, 900), 10)
    if 2 in selected:
        pygame.draw.circle(win, Green, (530, 900), 10)
        pygame.draw.circle(win, Red, (575, 900), 10)
    else:
        pygame.draw.circle(win, Red, (530, 900), 10)
        pygame.draw.circle(win, Green, (575, 900), 10)
    if 6 in selected:
        pygame.draw.circle(win, Green, (1277, 120), 10)
        pygame.draw.circle(win, Red, (1223, 120), 10)
    else:
        pygame.draw.circle(win, Red, (1277, 120), 10)
        pygame.draw.circle(win, Green, (1223, 120), 10)
    y = 285
    for i in range(len(inputBoxes)):
        if i % 2 == 0:
            textSurface = arial_font.render(inputLabels[i], True, Black)
            win.blit(textSurface, (win.get_width() // 2 + 375 - textSurface.get_width() // 2, y))
            display_box(win, f'{inputLabels[i]}: {inputValues[i]}', inputBoxes[i])
        else:

            textSurface = arial_font.render(inputLabels[i], True, Black)
            win.blit(textSurface, (win.get_width() // 2 + 625 - textSurface.get_width() // 2, y))
            y += 90
            display_box(win, f'{inputLabels[i]}: {inputValues[i]}', inputBoxes[i])



def redraw_game_window(clickPos):
    win.fill(Black)
    overlay(clickPos)
    renderWin.fill((0, 0, 0))
    myPers.drawPerspective(renderWin)
    
    miniMap()
    win.blit(renderWin, (0, 0))
    pygame.display.update()



errorMessage = ''
inputLabels = ['X Velocity', 'X Position', 'Y Velocity', 'Y Position', 'Z Velocity', 'Z Position', 'Radius', 'Mass', 'Gravity Constant', 'Color']
inputValues = ['', '', '', '', '', '', '', '', '', '']
all_buttons = ((1025, 320, 200, 30), (1275, 320, 200, 30), (1025, 410, 200, 30), (1275, 410, 200, 30), (1025, 500, 200, 30), (1275, 500, 200, 30), (1025, 590, 200, 30), (1275, 590, 200, 30), (1025, 680, 200, 30), (1275, 680, 200, 30),
               (1150, 835, 200, 50), (800, 875, 200, 50), (420, 850, 100, 100), (570, 840, 120, 120), (250, 850, 100, 100), (1050, 50, 150, 150), (1285, 35, 180, 180), (1025, 925, 200, 50), (1275, 925, 200, 50), (1025, 740, 200, 40), (854, 840, 39, 26))
inputBoxes = ((1025, 320, 200, 30), (1275, 320, 200, 30), (1025, 410, 200, 30), (1275, 410, 200, 30), (1025, 500, 200, 30), (1275, 500, 200, 30), (1025, 590, 200, 30), (1275, 590, 200, 30), (1025, 680, 200, 30), (1275, 680, 200, 30))
other_buttons = ((1150, 835, 200, 50), (800, 875, 200, 50), (420, 850, 100, 100), (570, 840, 120, 120), (250, 850, 100, 100), (1050, 50, 150, 150), (1285, 35, 180, 180), (1025, 925, 200, 50), (1275, 925, 200, 50), (1025, 740, 200, 40),(854, 840, 39, 26))
# 0 = confirm, 1 = moveable, 2 = play, 3 = pause, 4 = trash, 5 = planet, 6 = sun
win = pygame.display.set_mode((1500, 1000))
renderWin = pygame.Surface((1000, 800))
myPers = Render.perspective(1.0, 0, 0, [0, 20, 0], (1000, 800))


focused = False
playSim = False
clicked = []
selected = [1]

pygame.display.set_caption('SkyBox')
clickPos = (-1, -1)
gravity = None
inPlay = True
while inPlay:
    clickPos = pygame.mouse.get_pos()
    redraw_game_window(clickPos)
    if playSim:
        Gravity.newPositions(myPers.grid.stuff, False, gravity)
        Gravity.newPositions(myPers.grid.stuff, False, gravity)
        Gravity.newPositions(myPers.grid.stuff, False, gravity)
        Gravity.newPositions(myPers.grid.stuff, False, gravity)
        Gravity.newPositions(myPers.grid.stuff, False, gravity)
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
            

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if 0 <= clickPos[0] <= 1000 and 0 <= clickPos[1] <= 800:
                clickk = True
                focused = True
                if event.button == 4:
                    myPers.move("forward", 5)
                elif event.button == 5:
                    myPers.move("backward", 5)
                
                        
            else:
                focused = False
            
            inputButton = False
            otherButton = False
            for i, button in enumerate(all_buttons):
                if pygame.Rect(button).collidepoint(clickPos):
                    if i < len(inputBoxes):
                        inputButton = True
                    else:
                        otherButton = True
                    break
            if inputButton:
                for i, inputBox in enumerate(inputBoxes):
                    if pygame.Rect(inputBox).collidepoint(clickPos):
                        ask(win, f'{inputLabels[i]}: ', 10, inputBox)
            elif otherButton:
                for i, other_button in enumerate(other_buttons):
                    if pygame.Rect(other_button).collidepoint(clickPos):
                        # button management
                        if i == 0:
                            checkConfirm()
                        elif i == 1:
                            if 1 not in selected:
                                selected.append(1)
                                
                            else:
                                selected.remove(1)
                            stopPlanets(selected)
                                
                        elif i == 2:
                            playSim = True
                            if 2 not in selected:
                                if 3 in selected:
                                    selected.remove(3)
                                selected.append(2)
                        elif i == 3:
                            playSim = False
                            if 3 not in selected:
                                if 2 in selected:
                                    selected.remove(2)
                                selected.append(3)
                        elif i == 4:
                            deleteSelected()
                            Gravity.newPositions(myPers.grid.stuff, False, gravity)
                            Gravity.newPositions(myPers.grid.stuff, False, gravity)
                            
                        elif i == 5:
                            if 5 not in selected:
                                if 6 in selected:
                                    selected.remove(6)
                                selected.append(5)
                        elif i == 6:
                            if 6 not in selected:
                                if 5 in selected:
                                    selected.remove(5)
                                selected.append(6)
                        elif i == 7:
                            myPers.saveToFile(saveFile)
                        elif i == 8:
                            myPers.loadFromFile(saveFile)

                        elif i == 9:
                            try:
                                gravity = float(inputValues[8])
                            except:
                                pass
                        elif i == 10:
                            resetPerspective(myPers)
                            
    if pygame.mouse.get_pressed()[0] and pygame.mouse.get_pos()[0] <= 1000 and pygame.mouse.get_pos()[1] <= 800:
        if clicked:
            myPers.turn(clicked, list(pygame.mouse.get_pos()))
            clicked = list(pygame.mouse.get_pos())
        else:
            clicked = list(pygame.mouse.get_pos())
    else:
        if clicked:
            for thing in myPers.newThings:
                
                if math.hypot(clicked[0]-thing[0], clicked[1]-thing[1]) <= thing[2].clickRad:
                    if thing[2].selected:
                        thing[2].selected = False
                    else:
                        thing[2].selected = True
                    break
        clicked = []

    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_w]:
        myPers.move("up", 1)
    if keypress[pygame.K_s]:
        myPers.move("down", 1)
    if keypress[pygame.K_d]:
        myPers.move("right", 1)
    if keypress[pygame.K_a]:
        myPers.move("left", 1)

    if keypress[pygame.K_PAGEUP]:
        if radarRange >= 100:
            radarRange /= 2
    if keypress[pygame.K_PAGEDOWN]:
        radarRange *= 2

pygame.quit()
