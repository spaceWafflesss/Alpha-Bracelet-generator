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
# width = int(input("Enter the amount of string you will use: "))
# length = int(input("Minimum length: "))

# pygame.draw.rect(surface, color, pygame.Rect(100, 30, 25, 25))
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
        self.rect = pg.Rect(x, y, l, size)
        self.image = pg.Surface((l, size))
        self.image.fill((255, 255, 255))
        self.rad = size // 2
        self.color = (255, 0, 0)
        self.pwidth = l - self.rad * 2

        for i in range(self.pwidth):
            color = pg.Color(0)
            color.hsla = (int(360 * i / self.pwidth), 100, 50, 100)
            pg.draw.rect(self.image, color, (i + self.rad, size // 3, 1, size - 2 * size // 3), border_radius=5)
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
            self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
            self.p = (max(0, min(self.p, 1)))

            getColor = pg.Color(0)
            getColor.hsla = (int(self.p * 360), 100, 50, 100)
            self.color = getColor

        screen.blit(self.image, self.rect)
        center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
        pg.draw.circle(screen, self.color, center, self.rect.height // 2.5)

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

def editBitmap(event, bitmap, color=0):

    if not len(bitmap.braceletKnots) == 0:
        found = False

        knotCount = 0
        while found == False:
            for yRow in range(bitmap.length):
                for xRow in range(bitmap.width):
                    testKnot = pg.Rect(xRow * 26 + bitmap.x, yRow * 26 + bitmap.y, 25, 25)
                    if testKnot.collidepoint(event.pos):
                        bitmap.braceletKnots[knotCount].color = color
                        pg.draw.rect(surface, bitmap.braceletKnots[knotCount].color, (xRow * 26 + bitmap.x, yRow * 26 + bitmap.y, 25, 25))
                        found = True
                    elif xRow >= bitmap.width - 1:
                        found = True
                    knotCount = knotCount + 1

def createBitmap(x, y, bitmap, create=False):
    if create == True:
        bitmap.x = x
        bitmap.y = y
        bitmap.braceletKnots.clear()

        for knot in range(bitmap.width * bitmap.length):
            bitmap.braceletKnots.append(bitmap.knotInfo(knot, (92, 93, 95)))


    knotCount = 0
    for yRow in range(bitmap.length):
        for xRow in range(bitmap.width):
            pg.draw.rect(surface, bitmap.braceletKnots[knotCount].color, (xRow * 26 + x, yRow * 26 + y, 25, 25))
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
    text = medTxt.render("HI!", True, (0, 255, 0))
    x,y = 150, 100

    spacing = 80
    size = 2
    global knotCount
    knotCount = 0

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
                        pg.draw.rect(surface, (0, 0, 0), pg.Rect(posX - recWidth // 2, y - 50, recWidth, knotMap.length * spacing + 50), 1, border_radius=15)

                        # draw grey line in between
                        pg.draw.line(surface, (218, 218, 218), (posX, y - 40), (posX, knotMap.length * spacing + 90), 3 * size)
                        oldRow = xRow


                    lining = True
                    i = 0
                    while lining:
                        if len(lineCords.braceletKnots) == 0 or i == len(lineCords.braceletKnots):
                            lineCords.braceletKnots.append(lineCords.knotInfo(knotMap.braceletKnots[knotCount].color, posX, posY))

                            if direction == False:
                                pg.draw.line(surface, lineCords.braceletKnots[i].color, (posX, posY), (posX + x_range + 50, posY), 6 * size)
                            else:
                                pg.draw.line(surface, lineCords.braceletKnots[i].color, (posX, posY), (posX - xRow -50, posY), 6 * size)

                            lining = False
                        elif lineCords.braceletKnots[i].color != knotMap.braceletKnots[knotCount].color:
                            i += 1
                        else:
                            pg.draw.line(surface, lineCords.braceletKnots[i].color, (posX, posY), (lineCords.braceletKnots[i].x, lineCords.braceletKnots[i].y), 8 * size)
                            lineCords.braceletKnots[i].x = posX
                            lineCords.braceletKnots[i].y = posY
                            lining = False
                else:
                    gfx.filled_circle(surface, posX, posY, 15 * size, knotMap.braceletKnots[knotCount].color)
                    gfx.aacircle(surface, posX, posY, 15 * size, knotMap.braceletKnots[knotCount].color)

                    gfx.aacircle(surface, posX, posY, 16 * size, (0, 0, 0))
                    gfx.aacircle(surface, posX, posY, 17 * size, (0, 0, 0))

                    if direction:
                        text = arrowIn.render("->", True, (255, 255, 255))
                        surface.blit(text, (posX - 10, posY - 10))  # center text in circle
                        text = arrowOut.render("->", True, (0, 0, 0))
                        surface.blit(text, (posX - 10, posY - 10))  # center text in circle

                    else:
                        text = arrowIn.render("<-", True, (255, 255, 255))
                        surface.blit(text, (posX - 10, posY - 10))  # center text in circle
                        text = arrowOut.render("<-", True, (0, 0, 0))
                        surface.blit(text, (posX - 10, posY - 10))  # center text in circle

                '''if direction == False:
                    knotCount = knotCount + 1
                elif direction == True:
                    knotCount = knotCount - 1'''

                #knotCount = knotCount + 1


                pg.display.update()  # show the new circle
                #pg.time.delay(500)  # 1000 ms = 1 second



    while editScreen == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:# left click
                    if back.isPressed(event):
                        editScreen = True


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

    cp = ColorPicker(500, 30, 200, 40)
    # drawBitmap(5, 5)
    surface.fill((255, 255, 255))

    displayEditGrid = button(surface, 900, 300, 60, 30, "Load")
    displayInstruction = button(surface, 900, 100, 60, 30, "Apply")
    hasCreatedBitmap = False

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
                    editBitmap(event, knotMap, cp.color)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click

                    cp.update(surface)

                    if xStringInput.txt.isdigit() and yStringInput.txt.isdigit() and displayEditGrid.isPressed(event):
                        knotMap = knotList(int(xStringInput.txt), int(yStringInput.txt))
                        createBitmap(50, 50, knotMap, True)
                        hasCreatedBitmap = True

                    if displayInstruction.isPressed(event) and hasCreatedBitmap:
                        editScreen = False

                elif event.button == 3:  # right click
                    cp.color = surface.get_at(pg.mouse.get_pos())
                    cp.update(surface)

            elif event.type == pg.MOUSEWHEEL:
                pass
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
            # can access properties with
            # proper notation(ex: event.y)
        # print(input_box1.txt)
        pg.display.flip()
        clock.tick(60)


while True:
    if  editScreen:
        main()
    elif editScreen == False:
        instructionScreen()
