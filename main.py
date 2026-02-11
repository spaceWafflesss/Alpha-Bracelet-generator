import pygame as pg
pg.init()
from pygame.locals import *

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
braceletKnots = []
# pygame.draw.rect(surface, color, pygame.Rect(100, 30, 25, 25))
editScreen = True

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
        self.text = medTxt.render(showTxt, True, (0, 255, 0))

        pg.draw.rect(screen, (0, 0, 0), self.txtInput)
        screen.blit(self.text, (self.x, self.y))

    def isPressed(self, event):
        pg.draw.rect(self.screen, (255, 255, 255), self.txtInput)
        self.screen.blit(self.text, (self.x, self.y))
        print("ok5")
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
            pg.draw.rect(self.image, color, (i + self.rad, size // 3, 1, size - 2 * size // 3))
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
        pg.draw.rect(self.screen, self.color, self.txtInput, 2, 1)

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


class knotInfo:
    def __init__(self, ID, color):
        self.color = color
        self.ID = ID


def editBitmap(event, x=0, y=0, color=0):
    knotCount = 2
    found = True

    if not len(braceletKnots) == 0:
        width = braceletKnots[0]
        length = braceletKnots[1]
        found = False

        while found == False:
            for xRow in range(width):
                for yRow in range(length):
                    testKnot = pg.Rect(xRow * 26 + x, yRow * 26 + y, 25, 25)
                    if testKnot.collidepoint(event.pos):
                        braceletKnots[knotCount].color = color
                        pg.draw.rect(surface, braceletKnots[knotCount].color, (xRow * 26 + x, yRow * 26 + y, 25, 25))
                        found = True
                    elif xRow >= width - 1:
                        found = True
                knotCount = knotCount + 1


def createBitmap(x, y, width, length, create=False):
    if create == True:
        braceletKnots.clear()
        braceletKnots.append(width)
        braceletKnots.append(length)

        for knot in range(width * length):
            braceletKnots.append(knotInfo(knot, (92, 93, 95)))

    knotCount = 2
    for xRow in range(width):
        for yRow in range(length):
            pg.draw.rect(surface, braceletKnots[knotCount].color, (xRow * 26 + x, yRow * 26 + y, 25, 25))
        knotCount = knotCount + 1


def main():
    # global surface
    # global x, y
    global editScreen
    xStringInput = txtInputBox(surface, 900, 200, 60, 30, "Strings")
    yStringInput = txtInputBox(surface, 900, 250, 60, 30, "Length")
    xStringInput.update()
    yStringInput.update()

    cp = ColorPicker(500, 50, 200, 40)
    # drawBitmap(5, 5)
    surface.fill((255, 255, 255))

    displayEditGrid = button(surface, 300, 300, 60, 30, "Load")

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
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:# left click
                    editBitmap(event, 50, 50, cp.color)
                    cp.update(surface)

                    if xStringInput.txt.isdigit() and yStringInput.txt.isdigit() and displayEditGrid.isPressed(event):
                        createBitmap(50, 50, int(xStringInput.txt), int(yStringInput.txt), True)
                        print("ok1")

                elif event.button == 3:  # right click
                    print("ok5")
                    cp.color = surface.get_at(pg.mouse.get_pos())
                    cp.update(surface)

            elif event.type == pg.MOUSEWHEEL:
                editScreen = False
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

    while not editScreen:
        surface.fill((255, 255, 255))
        pg.display.flip()
        clock.tick(60)


# Execute game:


'''input_box = pg.draw.rect(surface, (0,  0, 0), (100, 180, 100, 32), 1)
pg.display.flip()
pg.time.wait(5000)  # Pause for 3 seconds
pg.quit()'''
main()
