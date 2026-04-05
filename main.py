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
clock = pg.time.Clock()
largeTxt = pg.font.Font(None, 32)
medTxt = pg.font.Font(None, 20)

editScreen = True
knotMap = None

'''class bk:
    def __init__(self, x, y, w, h,):
        self.x = x
        self.y = y'''

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
        def __init__(self, ID, color):
            self.color = color
            self.ID = ID

def editBitmap(screen, pos, bitmap, size, color=0):
    spacing = size - 1
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
    spacing = size - 1
    if create == True:
        bitmap.x = x
        bitmap.y = y
        bitmap.braceletKnots.clear()

        for knot in range(bitmap.width * bitmap.length):
            bitmap.braceletKnots.append(bitmap.knotInfo(knot, (92, 93, 95)))

    knotCount = 0
    for yRow in range(bitmap.length):
        for xRow in range(bitmap.width):
            pg.draw.rect(screen, bitmap.braceletKnots[knotCount].color, (xRow * spacing + x, yRow * spacing + y, size, size))
            knotCount = knotCount + 1

def instructionScreen():
    surface.fill((255, 255, 255))
    back = button(surface, 30, 50, 60, 30, "Back")
    global editScreen
    global knotMap

    if knotMap is not None:
        #createBitmap(100, 100, knotMap)
        pass
    else:
        print("ok6")

    pg.draw.circle(surface, (255, 38, 0), (900, 480), 10)
    #pg.draw.rect(surface, (0, 0, 0), pg.Rect(400, 260, 20, 70), 1, border_radius=15)
    arrowOut = pg.font.Font(None, 30)
    arrowIn = pg.font.Font(None, 29)
    x = 170
    y = 100

    spacing = 70
    size = 1
    global knotCount
    knotCount = 0
    yScroll = 0

    # color, coorodinates
    #linesCords = []

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
    scrollWindow = pg.Surface((x+knotMap.width * spacing, y+knotMap.length * spacing + 50))
    scrollWindow.fill((255, 255, 255))

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
                posX = x + xRow * spacing
                knotCount = yRow * knotMap.width + xRow

                if run == 0:
                    recWidth = 12
                    recWidth = recWidth * size
                    if oldRow != xRow and yRow == 0:
                        # center empty rectangle through circles
                        pg.draw.rect(scrollWindow, (0, 0, 0), pg.Rect(posX - recWidth // 2, y - 50, recWidth, knotMap.length * spacing + 50), 1, border_radius=15)

                        # draw grey line in between
                        pg.draw.line(scrollWindow, (218, 218, 218), (posX, y - 40), (posX, knotMap.length * spacing + 90), 3 * size)
                        oldRow = xRow


                    lining = True
                    i = 0
                    while lining:
                        if len(lineCords.braceletKnots) == 0 or i == len(lineCords.braceletKnots):
                            lineCords.braceletKnots.append(lineCords.knotInfo(knotMap.braceletKnots[knotCount].color, posX, posY))

                            if direction == False:
                                pg.draw.line(scrollWindow, lineCords.braceletKnots[i].color, (posX, posY), (posX + ((knotMap.width - 1 - xRow) * spacing) + 50, posY), 6 * size)
                            else:
                                pg.draw.line(scrollWindow, lineCords.braceletKnots[i].color, (posX, posY), ((posX - xRow * spacing) - 50, posY), 6 * size)

                            lining = False
                        elif lineCords.braceletKnots[i].color != knotMap.braceletKnots[knotCount].color:
                            i += 1
                        else:
                            pg.draw.line(scrollWindow, lineCords.braceletKnots[i].color, (posX, posY), (lineCords.braceletKnots[i].x, lineCords.braceletKnots[i].y), 8 * size)
                            lineCords.braceletKnots[i].x = posX
                            lineCords.braceletKnots[i].y = posY
                            lining = False
                else:
                    gfx.filled_circle(scrollWindow, posX, posY, 15 * size, knotMap.braceletKnots[knotCount].color)
                    gfx.aacircle(scrollWindow, posX, posY, 15 * size, knotMap.braceletKnots[knotCount].color)

                    gfx.aacircle(scrollWindow, posX, posY, 16 * size, (0, 0, 0))
                    gfx.aacircle(scrollWindow, posX, posY, 17 * size, (0, 0, 0))

                    if direction:
                        text = arrowIn.render("->", True, (255, 255, 255))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle
                        text = arrowOut.render("->", True, (0, 0, 0))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle

                    else:
                        text = arrowIn.render("<-", True, (255, 255, 255))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle
                        text = arrowOut.render("<-", True, (0, 0, 0))
                        scrollWindow.blit(text, (posX - 10, posY - 10))  # center text in circle

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
    editScreenSpacing = editGridSize - 1

    displayEditGrid = button(surface, 900, 300, 60, 30, "Load")
    displayInstruction = button(surface, 900, 100, 60, 30, "Apply")
    hasCreatedBitmap = False

    #x = 2
    #y = 100
    yScroll = 0
    scrollWindow = pg.Surface((1, 1))

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
                        maxKnots = 30
                        knotMap = knotList(int(xStringInput.txt), int(yStringInput.txt))
                        if knotMap.width > maxKnots:
                            editGridSize = editGridSize - (knotMap.width - maxKnots)
                            #editGridSize = editGridSize - (knotMap.width - maxKnots) * -2
                            #editScreenSpacing = max(10, min(40, surface.get_width() // knotMap.width))

                        scrollWindow = pg.Surface((knotMap.width * editScreenSpacing, y + knotMap.length * editScreenSpacing + 50))
                        scrollWindow.fill((255, 255, 255))
                        createBitmap(scrollWindow, x, y, knotMap, editGridSize, True)
                        x = (surface.get_width() - scrollWindow.get_width()) // 2

                        hasCreatedBitmap = True

                    if displayInstruction.isPressed(event) and hasCreatedBitmap:
                        editScreen = False

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
        if hasCreatedBitmap == True:
            surface.blit(scrollWindow, (x, 0), area=pg.Rect(0, yScroll, surface.get_width(), surface.get_height()))

        pg.display.flip()
        clock.tick(60)


while True:
    if  editScreen:
        main()
    elif editScreen == False:
        instructionScreen()
