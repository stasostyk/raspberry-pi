# By Stashito
# 18/12/2019
# Python 3

# This is a raspberry pi sense HAT display editor, where you can draw your own designs, click save,
# and they will be saved in an array format as needed for projects involving the 8x8 display.
# The saved files will be saved in a .txt file called savedGrids.txt, where each new save is ordered from old to new.
# To run, simply go into the directory of this file in your terminal and type "python displayEditor.py"


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
    # x, y = pg.mouse.get_pos()
    # pS, pR = text_objects(str(x) + " " + str(y), smallText, (0,255,0))
    # pR.center = ((x), (y))
    # win.blit(pS,pR)
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
        pg.draw.rect(win, pixels[i].getColorTuple(), ((800+(i*40), 400), (30,30)))
    for i in range(8):
        pg.draw.rect(win, pixels[i+8].getColorTuple(), ((800+(i*40), 440), (30,30)))
    for i in range(8):
        pg.draw.rect(win, pixels[i+16].getColorTuple(), ((800+(i*40), 480), (30,30)))
    for i in range(8):
        pg.draw.rect(win, pixels[i+24].getColorTuple(), ((800+(i*40), 520), (30,30)))
    for i in range(8):
        pg.draw.rect(win, pixels[i+32].getColorTuple(), ((800+(i*40), 560), (30,30)))
    for i in range(8):
        pg.draw.rect(win, pixels[i+40].getColorTuple(), ((800+(i*40), 600), (30,30)))
    for i in range(8):
        pg.draw.rect(win, pixels[i+48].getColorTuple(), ((800+(i*40), 640), (30,30)))
    for i in range(8):
        pg.draw.rect(win, pixels[i+56].getColorTuple(), ((800+(i*40), 680), (30,30)))

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
        f.write("\n\n"
            "pixels = ["
            +pixels[0].getColor()+", "+pixels[1].getColor()+", "+pixels[2].getColor()+", "+pixels[3].getColor()+", "
            +pixels[4].getColor()+", "+pixels[5].getColor()+", "+pixels[6].getColor()+", "+pixels[7].getColor()+", \n\t"
            +pixels[8].getColor()+", "+pixels[9].getColor()+", "+pixels[10].getColor()+", "+pixels[11].getColor()+", "
            +pixels[12].getColor()+", "+pixels[13].getColor()+", "+pixels[14].getColor()+", "+pixels[15].getColor()+", \n\t"
            +pixels[16].getColor()+", "+pixels[17].getColor()+", "+pixels[18].getColor()+", "+pixels[19].getColor()+", "
            +pixels[20].getColor()+", "+pixels[21].getColor()+", "+pixels[22].getColor()+", "+pixels[23].getColor()+", \n\t"
            +pixels[24].getColor()+", "+pixels[25].getColor()+", "+pixels[26].getColor()+", "+pixels[27].getColor()+", "
            +pixels[28].getColor()+", "+pixels[29].getColor()+", "+pixels[30].getColor()+", "+pixels[31].getColor()+", \n\t"
            +pixels[32].getColor()+", "+pixels[33].getColor()+", "+pixels[34].getColor()+", "+pixels[35].getColor()+", "
            +pixels[36].getColor()+", "+pixels[37].getColor()+", "+pixels[38].getColor()+", "+pixels[39].getColor()+", \n\t"
            +pixels[40].getColor()+", "+pixels[41].getColor()+", "+pixels[42].getColor()+", "+pixels[43].getColor()+", "
            +pixels[44].getColor()+", "+pixels[45].getColor()+", "+pixels[46].getColor()+", "+pixels[47].getColor()+", \n\t"
            +pixels[48].getColor()+", "+pixels[49].getColor()+", "+pixels[50].getColor()+", "+pixels[51].getColor()+", "
            +pixels[52].getColor()+", "+pixels[53].getColor()+", "+pixels[54].getColor()+", "+pixels[55].getColor()+", \n\t"
            +pixels[56].getColor()+", "+pixels[57].getColor()+", "+pixels[58].getColor()+", "+pixels[59].getColor()+", "
            +pixels[60].getColor()+", "+pixels[61].getColor()+", "+pixels[62].getColor()+", "+pixels[63].getColor() + "]")

        f.close()


def checkEvents():
    # print("checkin")
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

            elif y > 400 and y < 430:
                if x > 800 and x < 840:
                    pixels[0].color=currentColor
                elif x > 840 and x < 880:
                    pixels[1].color=currentColor
                elif x > 880 and x < 920:
                    pixels[2].color=currentColor
                elif x > 920 and x < 960:
                    pixels[3].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[4].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[5].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[6].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[7].color=currentColor

            elif y > 440 and y < 480:
                if x > 800 and x < 840:
                    pixels[8].color=currentColor
                elif x > 840 and x < 880:
                    pixels[9].color=currentColor
                elif x > 880 and x < 920:
                    pixels[10].color=currentColor
                elif x > 920 and x < 960:
                    pixels[11].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[12].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[13].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[14].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[15].color=currentColor

            elif y > 480 and y < 520:
                if x > 800 and x < 840:
                    pixels[16].color=currentColor
                elif x > 840 and x < 880:
                    pixels[17].color=currentColor
                elif x > 880 and x < 920:
                    pixels[18].color=currentColor
                elif x > 920 and x < 960:
                    pixels[19].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[20].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[21].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[22].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[23].color=currentColor

            elif y > 520 and y < 560:
                if x > 800 and x < 840:
                    pixels[24].color=currentColor
                elif x > 840 and x < 880:
                    pixels[25].color=currentColor
                elif x > 880 and x < 920:
                    pixels[26].color=currentColor
                elif x > 920 and x < 960:
                    pixels[27].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[28].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[29].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[30].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[31].color=currentColor

            elif y > 560 and y < 600:
                if x > 800 and x < 840:
                    pixels[32].color=currentColor
                elif x > 840 and x < 880:
                    pixels[33].color=currentColor
                elif x > 880 and x < 920:
                    pixels[34].color=currentColor
                elif x > 920 and x < 960:
                    pixels[35].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[36].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[37].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[38].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[39].color=currentColor

            elif y > 600 and y < 640:
                if x > 800 and x < 840:
                    pixels[40].color=currentColor
                elif x > 840 and x < 880:
                    pixels[41].color=currentColor
                elif x > 880 and x < 920:
                    pixels[42].color=currentColor
                elif x > 920 and x < 960:
                    pixels[43].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[44].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[45].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[46].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[47].color=currentColor

            elif y > 640 and y < 680:
                if x > 800 and x < 840:
                    pixels[48].color=currentColor
                elif x > 840 and x < 880:
                    pixels[49].color=currentColor
                elif x > 880 and x < 920:
                    pixels[50].color=currentColor
                elif x > 920 and x < 960:
                    pixels[51].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[52].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[53].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[54].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[55].color=currentColor

            elif y > 680 and y < 720:
                if x > 800 and x < 840:
                    pixels[56].color=currentColor
                elif x > 840 and x < 880:
                    pixels[57].color=currentColor
                elif x > 880 and x < 920:
                    pixels[58].color=currentColor
                elif x > 920 and x < 960:
                    pixels[59].color=currentColor
                elif x > 960 and x < 1000:
                    pixels[60].color=currentColor
                elif x > 1000 and x < 1040:
                    pixels[61].color=currentColor
                elif x > 1040 and x < 1080:
                    pixels[62].color=currentColor
                elif x > 1080 and x < 1120:
                    pixels[63].color=currentColor

while True:
    checkEvents()
    display()
