# By Stashito
# 18/12/2019

# This is a raspberry pi sense HAT display editor, where you can draw your own designs, click save,
# and they will be saved in an array format as needed for projects involving the 8x8 display.
# The saved files will be saved in a .txt file called savedGrids.txt, where each new save is ordered from old to new.


import pygame as pg

pg.init()
win = pg.display.set_mode((1920, 1080), pg.DOUBLEBUF)

pg.display.set_caption("Raspberry Pi Sense HAT Display Editor")
clock = pg.time.Clock()
clock.tick(15)

largeText = pg.font.Font('freesansbold.ttf', 140)
mediumText = pg.font.Font('freesansbold.ttf', 90)
smallText = pg.font.Font('freesansbold.ttf', 40)

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

currentColor = (255, 255, 255)

class InputBox:

    def __init__(self, x, y, w, h, rgbVal, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.rgb = rgbVal

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    global currentColor
                    if self.rgb == 0:
                        currentColor = (int(self.text), currentColor[1], currentColor[2])
                    elif self.rgb == 1:
                        currentColor = (currentColor[0], int(self.text), currentColor[2])
                    else:
                        currentColor = (currentColor[0], currentColor[1], int(self.text))

                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, win):
        # Blit the text.
        win.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(win, self.color, self.rect, 2)



def text_objects(text, font, color):
    s = font.render(text, True, color)
    return s, s.get_rect()



titleSurf, titleRect = text_objects("8x8 Display Editor", mediumText, (255,0,0))
titleRect.center = ((1920/2), (50))

saveSurf, saveRect = text_objects("Save", smallText, (255,255,255))
saveRect.center = ((1800), (50))

rS, rR = text_objects("R", FONT, (255,0,0))
rR.center = ((50), (210))
gS, gR = text_objects("G", FONT, (0,255,0))
gR.center = ((50), (260))
bS, bR = text_objects("B", FONT, (0,0,255))
bR.center = ((50), (310))



input_r = InputBox(100,200,140,32, 0)
input_g = InputBox(100,250,140,32, 1)
input_b = InputBox(100,300,140,32, 2)
input_boxes = [input_r, input_g, input_b]

isSaving = False
savingTick = 0

def display():
    win.fill((20,20,20))

    global isSaving
    if isSaving:
        global savingTick
        pg.draw.rect(win, (255,0,0), ((1750, 30), (100,40)))
        savingTick += 1
        if savingTick == 50:
            isSaving = False
            savingTick = 0

    colorsS, colorsR = text_objects(str(currentColor[0]) + ", " + str(currentColor[1]) + ", " + str(currentColor[2]), FONT, (150,150,150))
    colorsR.center = ((200), (360))

    for i in range(8):
        for j in range(8):
            pg.draw.rect(win, pixels[j+(i*8)].getColorTuple(), ((800+(j*40), 400+40*i), (30,30)))

    for box in input_boxes:
        box.update()
        box.draw(win)

    win.blit(rS, rR)
    win.blit(gS, gR)
    win.blit(bS, bR)
    win.blit(colorsS, colorsR)

    win.blit(titleSurf, titleRect)
    win.blit(saveSurf, saveRect)
    pg.display.update()

class pixel(object):
    def __init__(self, color):
        self.color = color

    def color(self, color):
        self.color = color

    def getColor(self):
        return "("+str(self.color[0])+","+str(self.color[1])+","+str(self.color[2])+")"

    def getColorTuple(self):
        return self.color

pixels = []
for i in range(64):
    pixels.append(pixel((0,0,0)))

def saveGrid():
    global isSaving
    isSaving = True
    with open("savedGrids.txt", 'a') as f:
        output = "\n\npixels= [\n\t"

        for i in range(8):
            for j in range(8):
                output += pixels[j + 8*i].getColor() + ", "
            output += "\n\t"

        f.write(output+"]")
        f.close()


def checkEvents():
    for event in pg.event.get():
        for box in input_boxes:
            box.handle_event(event)

        if event.type == pg.QUIT:
            print("quitting...")
            pg.quit()
            quit()

        elif event.type == pg.MOUSEBUTTONUP:
            x, y = pg.mouse.get_pos()
            if x > 1750 and y < 60 and x < 1860 and y > 30:
                print("saving...")
                saveGrid()

            for i in range(8):
                for j in range(8):
                    if y > 400 + 40*i and y < 430 + 40*i and x > 800 + 40*j and x < 830 + 40*j:
                        pixels[j+8*i].color = currentColor

while True:
    checkEvents()
    display()
