import pygame as pg
pg.init()
from pygame.locals import *
import pygame.gfxdraw as gfx

import time
# surface = pg.display.set_mode((500, 500))
surface = pg.display.set_mode((0, 0), pg.RESIZABLE)  # window
background = (255, 255, 255)
surface.fill(background)
color = (201, 201, 189)
defaultColor = (56, 56, 56)

clock = pg.time.Clock()
largeTxt = pg.font.Font(None, 32)
medTxt = pg.font.Font(None, 20)

editScreen = True
knotMap = None

class button:
    def __init__(self, screen, x, y, w, h, showTxt=""):
        self.screen = screen
        self.txtInput = pg.Rect(x, y, w, h)
        self.x = x
        self.y =  y
        self.text = medTxt.render(showTxt, True, (0, 0, 0))

        pg.draw.rect(screen, (0, 204, 102), self.txtInput, border_radius=5)
        screen.blit(self.text, (self.x + 15, self.y + 9))

    def isPressed(self, event):
        pg.draw.rect(self.screen, (0, 204, 102), self.txtInput, border_radius=5)
        self.screen.blit(self.text, (self.x + 15, self.y + 9))
        if self.txtInput.collidepoint(event.pos):
            return True
        else:
            return False

class ColorPicker:
    def __init__(self, x, y, l, size):
        self.rect = pg.Rect(x, y, size, l)
        self.image = pg.Surface((size, l))
        self.image.fill((255, 255, 255))
        self.rad = size // 2
        self.color = (255, 0, 0)
        self.pwidth = l - self.rad * 2

        for i in range(self.pwidth):
            color = pg.Color(0)
            color.hsla = (int(360 * i / self.pwidth), 100, 50, 100)
            pg.draw.rect(self.image, color, (size // 3, i + self.rad, size - 2 * size // 3, 1), border_radius=5)
        self.p = 0

    '''def currentColor(self):
        print("ok3")
        print(self.color)
        p = pg.Color(0)
        p.hsla = (int(self.p * self.pwidth), 100, 50, 100)
        self.color = p'''

    def update(self, screen):
        mouse_buttons = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        if mouse_buttons[0] and self.rect.collidepoint(mouse_pos):
            self.p = (mouse_pos[1] - self.rect.top - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

            getColor = pg.Color(0)
            getColor.hsla = (int(self.p * 360), 100, 50, 100)
            self.color = getColor

        screen.blit(self.image, self.rect)
        center = self.rect.centerx, self.rect.top + self.rad + self.p * self.pwidth
        pg.draw.circle(screen, self.color, center, self.rect.width // 2.5)

    '''def draw(self, screen):
        screen.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pg.draw.circle(screen, self.color, center, self.rect.height // 2.5)'''

class txtInputBox:
    def __init__(self, screen, x, y, w, h, showTxt="", txt=""):
        self.txtInput = pg.Rect(x, y, w, h)
        self.txt = txt
        self.enterTxt = False
        self.txt_surface = largeTxt.render(self.txt, True, (0, 255, 0))
        self.showTxt = showTxt
        self.text = medTxt.render(self.showTxt, True, (0, 0, 0))
        self.w = w
        self.screen = screen
        self.color = (92, 93, 95)
        self.x = x
        self.y = y

    def displayTxt(self):
        if self.txt == "":
            self.screen.blit(self.text, (self.x + 5, self.y + 5))
        else:
            self.txt_surface = largeTxt.render(self.txt, True, (0, 0, 0))
            self.screen.blit(self.txt_surface, (self.txtInput.x + 5, self.txtInput.y + 3))

    def update(self):
        # self.screen.fill((255, 255, 255), self.txtInput)
        inner = self.txtInput.inflate(-2, -2)
        self.screen.fill((255, 255, 255), inner)
        width = max(self.w, self.txt_surface.get_width() + 10)
        self.txtInput.w = width
        # Blit the input_box rect.
        pg.draw.rect(self.screen, self.color, self.txtInput, 2, border_radius=5)

    # previously called event
    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.txtInput.collidepoint(event.pos):
                self.enterTxt = True
                self.txt = ""
                # print(self.enterTxt)
            else:
                self.enterTxt = False

        if event.type == pg.KEYDOWN:
            if self.enterTxt:
                if event.key == pg.K_BACKSPACE:
                    self.txt = self.txt[:-1]
                    self.displayTxt()
                else:
                    self.txt += event.unicode
                    self.displayTxt()

                if not self.txt.isdigit():
                    self.color = (255, 0, 0)
                    print("not red")
                else:
                    # drawBitmap(7, int(self.txt))
                    # print(self.txt)
                    self.color = (92, 93, 95)

class knotList:
    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.braceletKnots = []
        self.x = 0
        self.y = 0

    class knotInfo:
        def __init__(self, color):
            self.color = color

def editBitmap(screen, pos, bitmap, size, color=0):
    spacing = size + 1
    if not len(bitmap.braceletKnots) == 0:
        found = False

        knotCount = 0
        while found == False:
            for yRow in range(bitmap.length):
                for xRow in range(bitmap.width):
                    testKnot = pg.Rect(xRow * spacing + bitmap.x, yRow * spacing + bitmap.y, size, size)
                    if testKnot.collidepoint(pos):
                        bitmap.braceletKnots[knotCount].color = color
                        pg.draw.rect(screen, bitmap.braceletKnots[knotCount].color, (xRow * spacing + bitmap.x, yRow * spacing + bitmap.y, size, size))
                        found = True
                    elif xRow >= bitmap.width - 1:
                        found = True
                    knotCount = knotCount + 1

def createBitmap(screen, x, y, bitmap, size, create=False):
    spacing = size + 1

    if create == True:
        bitmap.x = x
        bitmap.y = y
        bitmap.braceletKnots.clear()

        for knot in range(bitmap.width * bitmap.length):
            bitmap.braceletKnots.append(bitmap.knotInfo(defaultColor))

    knotCount = 0
    for yRow in range(bitmap.length):
        for xRow in range(bitmap.width):
            pg.draw.rect(screen, bitmap.braceletKnots[knotCount].color, (xRow * spacing + x, yRow * spacing + y, size, size))
            knotCount = knotCount + 1

def instructionScreen():
    surface.fill((255, 255, 255))
    back = button(surface, 30, 50, 60, 30, "Back")
    save = button(surface, 30, 100, 60, 30, "Save")
    txt = None
    global editScreen
    global knotMap

    if knotMap is not None:
        #createBitmap(100, 100, knotMap)
        pass
    else:
        print("ok6")


    x = 170
    y = 100

    size = 18
    #spacing = size + 50

    global knotCount
    knotCount = 0
    yScroll = 0
    enterStringOffset = 70

    maxKnots = 8
    if knotMap.width > maxKnots:
        size = ((maxKnots * size + (maxKnots - 1)) + (knotMap.width - 1)) // knotMap.width

    spacing = (size*3)
    gridWidth = knotMap.width * spacing + (knotMap.width - 1) + enterStringOffset
    x = (surface.get_width() - gridWidth) // 2
    txt = pg.font.Font(None, size)


    class colorPoints:
        def __init__(self):
            self.braceletKnots = []

        class knotInfo:
            def __init__(self, color, x, y):
                self.color = color
                self.x = x
                self.y = y

    lineCords = colorPoints()

    oldRow = None
    global posX
    posX = x + spacing

    scrollWindow = pg.Surface((gridWidth+50, y + knotMap.length * spacing + 100))
    scrollWindow.fill((255, 255, 255))

    #info for dynamically loaded pollygon arrow:
    w = size * 0.9  # total width
    h = size * 0.4  # total height

    head = w * 0.4
    body = w - head


    for run in range(0, 2):
        #knotCount = 0

        for yRow in range(knotMap.length):
            posY = y + yRow * spacing

            if yRow % 2 == 0:
                x_range = range(knotMap.width)
                direction = True
                knotCount = knotCount - knotMap.width
            else:
                x_range = range(knotMap.width - 1, -1, -1)
                direction = False
                knotCount = knotCount + knotMap.width

            for xRow in x_range:
                posX = enterStringOffset + xRow * spacing
                knotCount = yRow * knotMap.width + xRow

                if run == 0:
                    dynamicSize = round(size * 0.5)
                    if oldRow != xRow and yRow == 0:
                        # center empty rectangle through circles
                        pg.draw.rect(scrollWindow, (0, 0, 0),  pg.Rect(posX - dynamicSize*-1.5 // 2, y - 50, dynamicSize*-1.5, knotMap.length * spacing + 40), 1, border_radius=15)

                        # draw grey line in between
                        pg.draw.rect(scrollWindow, (214, 214, 214), pg.Rect(posX - dynamicSize*-0.4 // 2, y - 40, dynamicSize*-0.4, knotMap.length * spacing + 20), border_radius=15)
                        oldRow = xRow

                    text = txt.render(str(yRow), True, (128, 128, 128))
                    scrollWindow.blit(text, (posX + ((knotMap.width - 1 - xRow) * spacing) + 60, posY-size//4)) #right side
                    scrollWindow.blit(text, ((posX - xRow * spacing) - 70, posY-size//4)) #left side
                    #this puts greys lines to mark the y level, useful for the user to keep track
                    if direction:  # ->
                        if xRow == knotMap.width - 1:
                            pg.draw.line(scrollWindow, (199, 199, 199), (posX, posY),(posX + ((knotMap.width - 1 - xRow) * spacing) + 50, posY), 1)
                        elif xRow == 0:
                            pg.draw.line(scrollWindow, (199, 199, 199), (posX, posY),((posX - xRow * spacing) - 50, posY), 1)
                    else:  # <-

                        if xRow == 0:
                            pg.draw.line(scrollWindow, (199, 199, 199), (posX, posY), ((posX - xRow * spacing) - 50, posY), 1)
                        elif xRow == knotMap.width - 1:
                            pg.draw.line(scrollWindow, (199, 199, 199), (posX, posY), (posX + ((knotMap.width - 1 - xRow) * spacing) + 50, posY), 1)


                    #this while draws the lines  between the  knots that shows where the strings are suppose to go next
                    lining = True
                    i = 0

                    while lining:
                        # if at the start or finish of the width draw a line
                        # going into the pattern to show that a new string is being added
                        if len(lineCords.braceletKnots) == 0 or i == len(lineCords.braceletKnots):
                            lineCords.braceletKnots.append(lineCords.knotInfo(knotMap.braceletKnots[knotCount].color, posX, posY))

                            if direction == False: # <-
                                pg.draw.rect(scrollWindow, (0, 0, 0),(min(posX, posX + ((knotMap.width - 1 - xRow) * spacing) + 50) + 1, (posY - dynamicSize // 2) - 1, abs(posX + ((knotMap.width - 1 - xRow) * spacing) + 50 - posX), dynamicSize+2), border_radius=15)
                                pg.draw.rect(scrollWindow, lineCords.braceletKnots[i].color,(min(posX, posX + ((knotMap.width - 1 - xRow) * spacing) + 50), (posY - dynamicSize // 2), abs(posX + ((knotMap.width - 1 - xRow) * spacing) + 50 - posX), dynamicSize), border_radius=15)
                            else:
                                pg.draw.rect(scrollWindow, (0, 0, 0), (min(posX, posX - (xRow * spacing) - 50) - 1, (posY - dynamicSize // 2) - 1, abs((posX - (xRow * spacing) - 50) - posX), dynamicSize+2), border_radius=15)
                                pg.draw.rect(scrollWindow, lineCords.braceletKnots[i].color,(min(posX, posX - (xRow * spacing) - 50), (posY - dynamicSize // 2),abs((posX - (xRow * spacing) - 50) - posX), dynamicSize), border_radius=15)
                            lining = False

                        elif lineCords.braceletKnots[i].color != knotMap.braceletKnots[knotCount].color:
                            i += 1
                        else:  # ->
                            pg.draw.line(scrollWindow, (0, 0, 0), (posX, posY+1), (lineCords.braceletKnots[i].x, lineCords.braceletKnots[i].y+1), dynamicSize+4)
                            pg.draw.line(scrollWindow, lineCords.braceletKnots[i].color, (posX, posY),(lineCords.braceletKnots[i].x, lineCords.braceletKnots[i].y), dynamicSize)
                            lineCords.braceletKnots[i].x = posX
                            lineCords.braceletKnots[i].y = posY
                            lining = False
                else:
                    gfx.filled_circle(scrollWindow, posX, posY, size + 2, (0, 0, 0))  # border
                    gfx.filled_circle(scrollWindow, posX, posY,  size, knotMap.braceletKnots[knotCount].color)

                    left = posX - w / 2
                    right = posX + w / 2
                    top = posY - h / 2
                    bottom = posY + h / 2
                    mid = posY

                    if direction: #facing right ->
                        '''text = arrowIn.render("->", True, (255, 255, 255))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle
                        text = arrowOut.render("->", True, (0, 0, 0))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle'''

                        points = [
                            (left, posY - h * 0.25),
                            (left + body, posY - h * 0.25),
                            (left + body, top),
                            (right, mid),
                            (left + body, bottom),
                            (left + body, posY + h * 0.25),
                            (left, posY + h * 0.25),
                        ]

                    else: #facing left <-
                        '''text = arrowIn.render("<-", True, (255, 255, 255))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle
                        text = arrowOut.render("<-", True, (0, 0, 0))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle'''
                        points = [
                            (right, posY - h * 0.25),
                            (right - body, posY - h * 0.25),
                            (right - body, top),
                            (left, mid),
                            (right - body, bottom),
                            (right - body, posY + h * 0.25),
                            (right, posY + h * 0.25),
                        ]

                    r, g, b = knotMap.braceletKnots[knotCount].color[:3]
                    if r // 2 <= 127 and g // 2 <= 127 and b // 2 <= 127:
                        inside = (255, 255, 255)
                        outside = (0, 0, 0)
                    else:
                        inside = (0, 0, 0)
                        outside = (255, 255, 255)

                    pg.draw.polygon(scrollWindow, inside, points)
                    # border
                    pg.draw.polygon(scrollWindow, outside, points, 1)

                '''if direction == False:
                    knotCount = knotCount + 1
                elif direction == True:
                    knotCount = knotCount - 1'''

                #knotCount = knotCount + 1


                #pg.display.update()  # show the new circle

                #pg.time.delay(500)  # 1000 ms = 1 second
    #xS = 0
    while editScreen == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:# left click
                    if back.isPressed(event):
                        editScreen = True
                    if save.isPressed(event):
                        pg.image.save(scrollWindow, 'surface.png')
            elif event.type == pg.MOUSEWHEEL:
                yScroll -= event.y * 30.5
                #xS += event.x* 30.5

        #scrollWindow.fill((255, 255, 255))
        surface.blit(scrollWindow, (x, 0), area=pg.Rect(0, yScroll, surface.get_width(), surface.get_height()))
        pg.display.flip()
        clock.tick(60)

def main():
    # global surface
    # global x, y
    global editScreen
    global knotMap
    xStringInput = txtInputBox(surface, 900, 200, 60, 30, "Strings")
    yStringInput = txtInputBox(surface, 900, 250, 60, 30, "Length")
    xStringInput.update()
    yStringInput.update()

    cp = ColorPicker(900, 450, 200, 40)
    # drawBitmap(5, 5)
    surface.fill((255, 255, 255))

    editGridSize = 25
    maxKnots = 30
    editScreenSpacing = 25

    displayEditGrid = button(surface, 900, 300, 60, 30, "Load")
    displayInstruction = button(surface, 900, 100, 60, 30, "Apply")
    clearGrid = button(surface, 900, 160, 60, 30, "Clear")
    hasCreatedBitmap = False
    firstGridUse = True
    #x = 2
    #y = 100
    yScroll = 0
    scrollWindow = pg.Surface((1, 1))

    if not knotMap is None:
        y = 100
        x = 2
        if knotMap.width > maxKnots:
            editGridSize = ((maxKnots * editGridSize + (maxKnots - 1)) - (knotMap.width - 1)) // knotMap.width

        gridWidth = knotMap.width * editGridSize + (knotMap.width - 1)
        scrollWindow = pg.Surface((gridWidth, y + knotMap.length * editScreenSpacing + 100))
        scrollWindow.fill((255, 255, 255))

        createBitmap(scrollWindow, x, y, knotMap, editGridSize, False)
        x = (surface.get_width() - gridWidth) // 2

        hasCreatedBitmap = True
        firstGridUse = False


    while editScreen:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == VIDEORESIZE:
                # surface = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                # x = surface.get_height()/100
                # y = surface.get_width()/100
                pass

            if pg.mouse.get_pressed()[0]:
                if hasCreatedBitmap == True:
                    xScrollWindow, y = pg.mouse.get_pos()
                    editBitmap(scrollWindow, (xScrollWindow - x, y + yScroll), knotMap, editGridSize, cp.color)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    cp.update(surface)

                    if xStringInput.txt.isdigit() and yStringInput.txt.isdigit() and displayEditGrid.isPressed(event):
                        x = 2
                        y = 100
                        editGridSize =  25

                        if firstGridUse == False:
                            scrollWindow.fill((255, 255, 255))
                            x = (surface.get_width() - gridWidth) // 2
                            surface.blit(scrollWindow, (x, 0), area=pg.Rect(0, yScroll, surface.get_width(), surface.get_height()))
                            x  =  2

                        #if not knotMap is None:
                            #editBitmap()
                        knotMap = knotList(int(xStringInput.txt), int(yStringInput.txt))

                        if knotMap.width > maxKnots:
                            editGridSize = ((maxKnots * editGridSize + (maxKnots - 1)) - (knotMap.width - 1)) // knotMap.width

                        gridWidth = knotMap.width * editGridSize + (knotMap.width - 1)
                        scrollWindow = pg.Surface((gridWidth, y + knotMap.length * editScreenSpacing + 100))
                        scrollWindow.fill((255, 255, 255))
                        createBitmap(scrollWindow, x, y, knotMap, editGridSize, True)
                        x = (surface.get_width() - gridWidth) // 2

                        hasCreatedBitmap = True
                        firstGridUse = False

                    if displayInstruction.isPressed(event) and hasCreatedBitmap:
                        editScreen = False

                    if clearGrid.isPressed(event) and hasCreatedBitmap: #if there is  already  a grid loop through the  color and set everything to grey
                        y = 100
                        x = 2
                        for knot in knotMap.braceletKnots:
                            knot.color = defaultColor
                        createBitmap(scrollWindow, x, y, knotMap, editGridSize, False)
                        x = (surface.get_width() - gridWidth) // 2


                elif event.button == 3:  # right click
                    cp.color = surface.get_at(pg.mouse.get_pos())
                    cp.update(surface)

            elif event.type == pg.MOUSEWHEEL:
                yScroll -= event.y * 30.5
            if event.type == pg.KEYDOWN:
                pass

            xStringInput.event(event)
            xStringInput.update()
            xStringInput.displayTxt()
            yStringInput.event(event)
            yStringInput.update()
            yStringInput.displayTxt()

            cp.update(surface)
            # cp.draw(surface)

            # xStringInput.update()
        # print(input_box1.txt)
        if not knotMap is None:
            surface.blit(scrollWindow, (x, 0), area=pg.Rect(0, yScroll, surface.get_width(), surface.get_height()))

        pg.display.flip()
        clock.tick(60)

while True:
    if  editScreen:
        main()
    elif editScreen == False:
        instructionScreen()
