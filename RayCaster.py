# -*- coding: utf-8 -*-
# Silvio Orozco 18282
# Universidad del Valle de Guatemala
# Gráficas por computadora
# Guatemala 15/10/2020
#  RayCasterayCaster.py

#This an implentation of a RayCaster using PyGame
import pygame
from math import cos, sin, pi,atan2



# Colors used in our RayCaster
BLACK = (0,0,0)
WHITE = (255,255,255)
BACKGROUND = (64,64,64)
SPRITE_BACKGROUND = (152, 0, 136, 255)
# Colors used for RayCasting colors of maps
colors = {
    '1' : (106, 59, 3),
    '2' : (215, 117, 0),
    '3' : (255, 207, 149),
    '4' : (0, 20, 201),
    '5' : (133, 145, 255)
}

#Loading textures
textures = {
    '1' : pygame.image.load('wall1.png'),
    '2' : pygame.image.load('wall2.png'),
    '3' : pygame.image.load('wall3.png'),
    '4' : pygame.image.load('wall11.png'),
    '5' : pygame.image.load('wall5.png')
}

enemies = [{"x": 130,
            "y": 300,
            "texture" : pygame.image.load('enemy1.png')},

           {"x": 180,
            "y": 250,
            "texture" : pygame.image.load('enemy2.png')},

           {"x": 130,
            "y": 100,
            "texture" : pygame.image.load('enemy3.png')} ,

           {"x": 400,
            "y": 75,
            "texture" : pygame.image.load('enemy4.png')}  ,

           {"x": 375,
            "y": 425,
            "texture" : pygame.image.load('enemy5.png')}  ,

           {"x": 100,
            "y": 420,
            "texture" : pygame.image.load('enemy6.png')}     
    ]


#Class Ray Caster
class Raycaster(object):
    #Init gets screen where it will render
    def __init__(self,screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.map = []
        #Block size of each point in map
        self.blocksize = 50
        self.wallHeight = 50
        #Step size our player will be moving
        self.stepSize = 10
        #We set our block color
        self.setBlockColor(WHITE)

        #Zbuffer
        self.zbuffer = [-float('inf') for z in range(int(self.width / 2))]
        #We create our player that has information of its position, angle of view and fov field of view
        self.player = {
            "x" : 120,
            "y" : 200,
            "angle" : 0,
            "fov" : 60
        }

    #Set Block Color
    def setBlockColor(self, color):
        self.blockColor = color

    #Load a map from a file
    def loadMap(self, filename):
        #We open file and read each line and append it to our self.map as a list
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))
        self.blocksize = int((self.width/2)/len(self.map))

    #Draw a reactangle
    def drawRectangle(self, x, y,texture=None):
        
        texture = pygame.transform.scale(texture, (self.blocksize, self.blocksize))
        rectangle=texture.get_rect()
        rectangle=rectangle.move((x,y))
        self.screen.blit(texture, rectangle)

    #Draw our players icon
    def drawPlayerIcon(self,color=BLACK):
        rectangle = (self.player['x'] - 2, self.player['y'] - 2, 6, 6)
        self.screen.fill(color, rectangle)


    #Function to draw a sprite
    def drawSprite(self, sprite, size):
        # pythagorean theorem to calculate sprite distance between player and sprite
        spriteDist = ((self.player['x'] - sprite['x'])**2 + (self.player['y'] - sprite['y'])**2) ** 0.5
        
        # calculate angule between sprite and player
        spriteAngle = atan2(sprite['y'] - self.player['y'], sprite['x'] - self.player['x'])

        # calculate aspect ratio and with the size given 
        aspectRatio = sprite["texture"].get_width() / sprite["texture"].get_height()
        spriteHeight = (self.height / spriteDist) * size
        spriteWidth = spriteHeight * aspectRatio

        # change angles to radians
        angleRadians = self.player['angle'] * pi / 180
        fovRadians = self.player['fov'] * pi / 180

        #Check for start point to visualize sprite and then make a loop to end to draw sprite
        startX = (self.width * 3 / 4) + (spriteAngle - angleRadians)*(self.width/2) / fovRadians - (spriteWidth/2)
        startY = (self.height / 2) - (spriteHeight / 2)
        startX = int(startX)
        startY = int(startY)

        for x in range(startX, int(startX + spriteWidth)):
            for y in range(startY, int(startY + spriteHeight)):
                if (self.width / 2) < x < self.width:
                    if self.zbuffer[ x - int(self.width/2)] >= spriteDist:
                        tx = int( (x - startX) * sprite["texture"].get_width() / spriteWidth )
                        ty = int( (y - startY) * sprite["texture"].get_height() / spriteHeight )
                        texColor = sprite["texture"].get_at((tx, ty))
                        if texColor[3] > 128 and texColor != SPRITE_BACKGROUND:
                            self.screen.set_at((x,y), texColor)
                            #Z buffer to calculate if sprite is in front or behind
                            self.zbuffer[ x - int(self.width/2)] = spriteDist

    #Function for casting a ray
    def castRay(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))
            i = int(x/self.blocksize)
            j = int(y/self.blocksize)
            #Verify where ray hits and return distance, texture and tx if hits
            if self.map[j][i] != ' ':
                hitX = x - i*self.blocksize
                hitY = y - j*self.blocksize

                if 1 < hitX < self.blocksize - 1:
                    maxHit = hitX
                else:
                    maxHit = hitY

                tx = maxHit / self.blocksize

                return dist, self.map[j][i], tx
                
            self.screen.set_at((x,y), WHITE)
            dist += 2

    #Function to render our scene
    #This has to be called each time to update our scene
    def render(self):
        halfWidth = int(self.width / 2)
        halfHeight = int(self.height / 2)
        #Half width for 2d View, halfwidth for 3D view
        #We first draw our map left
        for x in range(0, halfWidth, self.blocksize):
            for y in range(0, self.height, self.blocksize):
                i = int(x/self.blocksize)
                j = int(y/self.blocksize)
                if self.map[j][i] != ' ':
                    self.drawRectangle(x, y, texture=textures[self.map[j][i]])

        self.drawPlayerIcon(BLACK)

        #We draw our 3D World
        for i in range(halfWidth):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / halfWidth
            dist, textureType,tx = self.castRay(angle)
            self.zbuffer[i] = dist
            x = halfWidth + i
            
            # perceivedHeight = screenHeight / (distance * cos( rayAngle - viewAngle) * wallHeight
            try:
                h = self.height / (dist * cos( (angle - self.player['angle']) * pi / 180 )) * self.wallHeight

                start = int( halfHeight - h/2)
                end = int( halfHeight + h/2)
                texture = textures[textureType]
                tx = int(tx * texture.get_width())
                for y in range(start, end):
                    ty = (y - start) / (end - start)
                    ty = int(ty * texture.get_height())
                    textureColor = texture.get_at((tx, ty))
                    self.screen.set_at((x, y), textureColor)
            except ZeroDivisionError:
                print("Error on wall")


        #Render enemies
        for enemy in enemies:
            self.screen.fill(pygame.Color("red"), (enemy['x'], enemy['y'], 4,4))
            self.drawSprite(enemy, 30)

        #Render middle lines for division
        for i in range(self.height):
            self.screen.set_at( (halfWidth, i), BLACK)
            self.screen.set_at( (halfWidth+1, i), BLACK)
            self.screen.set_at( (halfWidth-1, i), BLACK)


global returnMainScreen
returnMainScreen=False
global closeExit
closeExit=False
#Init Pygame
pygame.init()
screenWidth=1000
screenHeight=500
#Main Menu Screen
def mainMenu():
    pygame.mixer.music.load("musicRockstar.mp3")
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((screenWidth,screenHeight),pygame.DOUBLEBUF | pygame.HWACCEL ) #, pygame.FULLSCREEN)
    pygame.display.set_caption('Main Menu')
    
    #Background image
    bg = pygame.image.load("bgg.png")
    screen.fill([255, 255, 255])
    rectangle=bg.get_rect()
    bg=pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    screen.blit(bg,((screen.get_width()-bg.get_width())/2,0))

    #Title of Screen
    font = pygame.font.SysFont("Arial", 40)
    title = str((" "*3+"Ray Caster Graffitti"+" "*3))
    title = font.render(title, 1, pygame.Color("black"))
    titleRec = title.get_rect()
    titleRec.center = (screen.get_width() // 2, screen.get_height() // 6) 
    screen.fill(pygame.Color("white"), titleRec)
    screen.blit(title, titleRec)

    #Button Start
    buttonStart = str((" "*3+"Start"+" "*3))
    buttonStart = font.render(buttonStart, 1, pygame.Color("black"))
    buttonStartRec = buttonStart.get_rect()
    buttonStartRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
    screen.fill(pygame.Color("white"), buttonStartRec)
    screen.blit(buttonStart, buttonStartRec)

    #Button Quit
    buttonQuit = str((" "*3+"Quit"+" "*3))
    buttonQuit = font.render(buttonQuit, 1, pygame.Color("black"))
    buttonQuitRec = buttonQuit.get_rect()
    buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
    screen.fill(pygame.Color("white"), buttonQuitRec)
    screen.blit(buttonQuit, buttonQuitRec)




    isRunning = True
    closeExit=False
    buttonPressed=None
    while isRunning:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False
                closeExit = True
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                    closeExit = True
                elif ev.key == pygame.K_DOWN:
                    if(buttonPressed==buttonQuitRec):
                        bp=None
                    elif(buttonPressed==buttonStartRec):
                        bp=buttonQuitRec
                    elif(buttonPressed==None):
                        bp=buttonStartRec
                    
                    buttonPressed=bp
                elif ev.key == pygame.K_UP:
                    if(buttonPressed==buttonStartRec):
                        bp=None
                    elif(buttonPressed==buttonQuitRec):
                        bp=buttonStartRec
                    elif(buttonPressed==None):
                        bp=buttonQuitRec
                    buttonPressed=bp
                elif ev.key == pygame.K_RETURN:
                    if buttonPressed==buttonQuitRec: 
                        isRunning = False 
                        closeExit=True
                    elif buttonPressed==buttonStartRec: 
                        isRunning = False 
                        closeExit=False
                    

            #Check for mouse clicks
            elif ev.type == pygame.MOUSEBUTTONDOWN: 
                mouse = pygame.mouse.get_pos()
                
                #Button Quit
                if buttonQuitRec.collidepoint(mouse): 
                    isRunning = False 
                    closeExit=True
                elif buttonStartRec.collidepoint(mouse): 
                    isRunning = False 
                    closeExit=False
                else:
                    buttonPressed=None
            #Check for hovers on buttons
            mouse = pygame.mouse.get_pos()
            if buttonQuitRec.collidepoint(mouse) or buttonPressed==buttonQuitRec: 
                buttonPressed=buttonQuitRec
                buttonQuit = str((" "*3+"Quit"+" "*3))
                buttonQuit = font.render(buttonQuit, 1, pygame.Color("WHITE"))
                buttonQuitRec = buttonQuit.get_rect()
                buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
                screen.fill(pygame.Color("gray"), buttonQuitRec)
                screen.blit(buttonQuit, buttonQuitRec)
            else:
                
                buttonQuit = str((" "*3+"Quit"+" "*3))
                buttonQuit = font.render(buttonQuit, 1, pygame.Color("black"))
                buttonQuitRec = buttonQuit.get_rect()
                buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
                screen.fill(pygame.Color("white"), buttonQuitRec)
                screen.blit(buttonQuit, buttonQuitRec)
            
            if buttonStartRec.collidepoint(mouse) or buttonPressed==buttonStartRec: 
                buttonPressed=buttonStartRec
                buttonStart = str((" "*3+"Start"+" "*3))
                buttonStart = font.render(buttonStart, 1, pygame.Color("white"))
                buttonStartRec = buttonStart.get_rect()
                buttonStartRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
                screen.fill(pygame.Color("gray"), buttonStartRec)
                screen.blit(buttonStart, buttonStartRec)
            else: 
                
                buttonStart = str((" "*3+"Start"+" "*3))
                buttonStart = font.render(buttonStart, 1, pygame.Color("black"))
                buttonStartRec = buttonStart.get_rect()
                buttonStartRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
                screen.fill(pygame.Color("white"), buttonStartRec)
                screen.blit(buttonStart, buttonStartRec)
        pygame.display.update()
    pygame.mixer.music.stop()
    #Start of our Real Raytracer
    if(not closeExit):
        closeExit=rayCasterScreen()
        if(closeExit):
            mainMenu()

#Pause Menu Screen
def pauseMenu():
    screen = pygame.display.set_mode((screenWidth,screenHeight),pygame.DOUBLEBUF | pygame.HWACCEL ) #, pygame.FULLSCREEN)
    pygame.display.set_caption('Pause Menu')
    
    #Background image
    bg = pygame.image.load("bgg.png")
    screen.fill([255, 255, 255])
    rectangle=bg.get_rect()
    bg=pygame.transform.scale(bg, (screen.get_width(), screen.get_height()))
    screen.blit(bg,((screen.get_width()-bg.get_width())/2,0))

    #Title of Screen
    font = pygame.font.SysFont("Arial", 40)
    title = str((" "*3+"Ray Caster Graffitti"+" "*3))
    title = font.render(title, 1, pygame.Color("black"))
    titleRec = title.get_rect()
    titleRec.center = (screen.get_width() // 2, screen.get_height() // 6) 
    screen.fill(pygame.Color("white"), titleRec)
    screen.blit(title, titleRec)

    #Button Start
    buttonContinue = str((" "*3+"Start"+" "*3))
    buttonContinue = font.render(buttonContinue, 1, pygame.Color("black"))
    buttonContinueRec = buttonContinue.get_rect()
    buttonContinueRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
    screen.fill(pygame.Color("white"), buttonContinueRec)
    screen.blit(buttonContinue, buttonContinueRec)

    #Button Quit
    buttonQuit = str((" "*3+"Quit"+" "*3))
    buttonQuit = font.render(buttonQuit, 1, pygame.Color("black"))
    buttonQuitRec = buttonQuit.get_rect()
    buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
    screen.fill(pygame.Color("white"), buttonQuitRec)
    screen.blit(buttonQuit, buttonQuitRec)




    isRunning = True
    closeExitPause=False
    buttonPressed=None
    closeExit=False
    while isRunning:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False
                closeExitPause = False
                closeExit=True
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    isRunning = False
                    closeExitPause = False
                elif ev.key == pygame.K_DOWN:
                    if(buttonPressed==buttonQuitRec):
                        bp=None
                    elif(buttonPressed==buttonContinueRec):
                        bp=buttonQuitRec
                    elif(buttonPressed==None):
                        bp=buttonContinueRec
                    
                    buttonPressed=bp
                elif ev.key == pygame.K_UP:
                    if(buttonPressed==buttonContinueRec):
                        bp=None
                    elif(buttonPressed==buttonQuitRec):
                        bp=buttonContinueRec
                    elif(buttonPressed==None):
                        bp=buttonQuitRec
                    buttonPressed=bp
                elif ev.key == pygame.K_RETURN:
                    if buttonPressed==buttonQuitRec: 
                        isRunning = False 
                        closeExitPause=True
                    elif buttonPressed==buttonContinueRec: 
                        isRunning = False 
                        closeExitPause=False
                    

            #Check for mouse clicks
            elif ev.type == pygame.MOUSEBUTTONDOWN: 
                mouse = pygame.mouse.get_pos()
                
                #Button Quit
                if buttonQuitRec.collidepoint(mouse): 
                    isRunning = False 
                    closeExitPause=True
                elif buttonContinueRec.collidepoint(mouse): 
                    isRunning = False 
                    closeExitPause=False
                else:
                    buttonPressed=None
            #Check for hovers on buttons
            mouse = pygame.mouse.get_pos()
            if buttonQuitRec.collidepoint(mouse) or buttonPressed==buttonQuitRec: 
                buttonPressed=buttonQuitRec
                buttonQuit = str((" "*3+"Main Menu"+" "*3))
                buttonQuit = font.render(buttonQuit, 1, pygame.Color("WHITE"))
                buttonQuitRec = buttonQuit.get_rect()
                buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
                screen.fill(pygame.Color("gray"), buttonQuitRec)
                screen.blit(buttonQuit, buttonQuitRec)
            else:
                
                buttonQuit = str((" "*3+"Main Menu"+" "*3))
                buttonQuit = font.render(buttonQuit, 1, pygame.Color("black"))
                buttonQuitRec = buttonQuit.get_rect()
                buttonQuitRec.center = (screen.get_width() // 2, screen.get_height()*3.5 // 6) 
                screen.fill(pygame.Color("white"), buttonQuitRec)
                screen.blit(buttonQuit, buttonQuitRec)
            
            if buttonContinueRec.collidepoint(mouse) or buttonPressed==buttonContinueRec: 
                buttonPressed=buttonContinueRec
                buttonContinue = str((" "*3+"Continue"+" "*3))
                buttonContinue = font.render(buttonContinue, 1, pygame.Color("white"))
                buttonContinueRec = buttonContinue.get_rect()
                buttonContinueRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
                screen.fill(pygame.Color("gray"), buttonContinueRec)
                screen.blit(buttonContinue, buttonContinueRec)
            else: 
                
                buttonContinue = str((" "*3+"Continue"+" "*3))
                buttonContinue = font.render(buttonContinue, 1, pygame.Color("black"))
                buttonContinueRec = buttonContinue.get_rect()
                buttonContinueRec.center = (screen.get_width() // 2, screen.get_height()*2.5 // 6) 
                screen.fill(pygame.Color("white"), buttonContinueRec)
                screen.blit(buttonContinue, buttonContinueRec)
        pygame.display.update()
    return closeExitPause,closeExit

def rayCasterScreen():
    pygame.mixer.music.load("musicTown.mp3")
    pygame.mixer.music.play(-1)
    pygame.display.set_caption('Ray Caster')
    screen = pygame.display.set_mode((screenWidth,screenHeight),pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
    screen.set_alpha(None)

    #Used to calculate FPS
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)
    def updateFPS():
        fps = str(int(clock.get_fps()))
        fps = font.render(fps, 1, pygame.Color("white"))
        return fps

    rayCaster = Raycaster(screen)
    rayCaster.setBlockColor( (128,0,0) )
    rayCaster.loadMap('ownmap.txt')
    closeExit=False
    isRunning = True
    pause=False
    global returnMainScreen
    while isRunning:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                isRunning = False
                closeExit=True

            playerXpos = rayCaster.player['x']
            playerYpos = rayCaster.player['y']
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    if(not pause):
                        pause = True
                        closeExitMenu,closeExit = pauseMenu()
                        if(not closeExit):
                            if(closeExitMenu):
                                returnMainScreen=True
                                isRunning=False
                            else:
                                pygame.display.set_caption('Ray Caster')
                                screen = pygame.display.set_mode((screenWidth,screenHeight),pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
                                screen.set_alpha(None)
                        else:
                            isRunning=False
                    else:
                        pause=False
                        pygame.display.set_caption('Ray Caster')
                        screen = pygame.display.set_mode((screenWidth,screenHeight),pygame.DOUBLEBUF | pygame.HWACCEL) #, pygame.FULLSCREEN)
                        screen.set_alpha(None)
                elif ev.key == pygame.K_w:
                    playerXpos += cos(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                    playerYpos += sin(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                elif ev.key == pygame.K_s:
                    playerXpos -= cos(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                    playerYpos -= sin(rayCaster.player['angle'] * pi / 180) * rayCaster.stepSize
                elif ev.key == pygame.K_a:
                    playerXpos -= cos((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                    playerYpos -= sin((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                elif ev.key == pygame.K_d:
                    playerXpos += cos((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                    playerYpos += sin((rayCaster.player['angle'] + 90) * pi / 180) * rayCaster.stepSize
                elif ev.key == pygame.K_q:
                    rayCaster.player['angle'] -= 5
                elif ev.key == pygame.K_e:
                    rayCaster.player['angle'] += 5

                i = int(playerXpos / rayCaster.blocksize)
                j = int(playerYpos / rayCaster.blocksize)

                if rayCaster.map[j][i] == ' ':
                    rayCaster.player['x'] = playerXpos
                    rayCaster.player['y'] = playerYpos

        #Floor on our mini map
        floor = pygame.image.load("floor4.png")
        rectangle=floor.get_rect()
        floor=pygame.transform.scale(floor, (screen.get_width(), screen.get_height()))
        screen.fill(BACKGROUND)
        screen.blit(floor, (int(0), int(0), int(rayCaster.width / 2),int(rayCaster.height)))
        


        #Ceilign
        screen.fill(pygame.Color("skyblue"), (int(rayCaster.width / 2), 0, int(rayCaster.width / 2),int(rayCaster.height / 2)))
        
        #Floor
        #screen.fill(pygame.Color("dimgray"), (int(rayCaster.width / 2), int(rayCaster.height / 2), int(rayCaster.width / 2),int(rayCaster.height / 2)))
        
        #Floor image
        floor = pygame.image.load("floor4.png")
        rectangle=floor.get_rect()
        floor=pygame.transform.scale(floor, (screen.get_width(), screen.get_height()))
        screen.blit(floor, (int(rayCaster.width / 2), int(rayCaster.height / 2), int(rayCaster.width / 2),int(rayCaster.height / 2)))

        #Render RayCaster
        rayCaster.render()

        # FPS
        screen.fill(pygame.Color("black"), (0,0,30,30))
        screen.blit(updateFPS(), (10,5))
        clock.tick(30)  

        pygame.display.update()
    
    pygame.mixer.music.stop()
    if(closeExit):
        return False
    else:
        if(returnMainScreen):
            return True
        else:
            return False
    

mainMenu()


pygame.quit()