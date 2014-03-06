#! usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys, random

class Paddle(object):
    """
    A typical paddle of a pong game
    
    Args:
        posX (int): x-Coordinate
        posY (int): y-Coordinate
        width (int): width of the paddle
        height (int): height of the paddle
        surface (pygame.Surface): Surface the paddle is drawn to
        color (pygame.Color): Color of the paddle
        speed (float): the speed of the paddle in pixels per second
    """
    
    def __init__(self,posX, posY, width, height, window, color,speed):
        self.posX = posX
        self.posY = posY
        self.height = height
        self.width = width
        self.color = color
        self.direction = "idle"
        self.speed = speed
        self.score = 0
        self.rect = pygame.draw.rect(window, color, (posX,posY,width,height))
    
    def get_rect(self):
        return (self.posX, self.posY, self.width, self.height)
    
    def setDirection(self, direction):
        """
        Sets the direction
        
        Args:
            direction (str): is either "up", "down" or "idle"
        
        Returns:
            no returns
        """
        
        self.direction = direction
    
    def addScore(self, amount):
        """
        Adds the amount to the score
        
        Args:
            amount (int)
            
        Returns:
            no returns
        """
        self.score = self.score + amount
    
    def getScore(self):
        """
        Returns the score
        
        Args:
            no arguments
        
        Returns:
            self.score (int)
        """
        return self.score
    
    def getDirection(self):
        """Returns the direction (str) of the paddle"""
        
        return self.direction
    
    def update(self,window,dt):
        """
        updates the state of the paddle
        
        Args:
            window (pygame.Surface): The surface the paddle is drawn to
            dt (float): the delta time since the last update
        
        Returns:
            no return
        """
        
        if self.direction == "up":
            self.posY = self.posY - self.speed * dt
            if self.posY < 0:
                self.posY = 0
        elif self.direction == "down":
            self.posY = self.posY + self.speed * dt
            if self.posY > window.get_rect()[3]-self.height:
                self.posY = window.get_rect()[3]-self.height
        
        self.rect = pygame.draw.rect(window, self.color, (self.posX,self.posY,self.width,self.height))
            
class Ball(object):
    def __init__(self, posX, posY, imagePath, speedX, speedY):
        self.posX = posX
        self.posY = posY
        self.img = pygame.image.load(imagePath).convert_alpha()
        self.speedX = speedX
        self.speedY = speedY
    
    def getImage(self):
        return self.img
    
    def get_rect(self):
        return (self.posX, self.posY, self.img.get_rect()[2], self.img.get_rect()[3])
    
    def setPosX(self, posX):
        self.posX = posX
    
    def getPosX(self):
        return self.posX
    
    def setPosY(self, posY):
        self.posY = posY
    
    def getPosY(self):
        return self.posY
    
    def setSpeedX(self, speedX):
        self.speedX = speedX
    
    def getSpeedX(self):
        return self.speedX
    
    def setSpeedY(self, speedY):
        self.speedY = speedY
    
    def getSpeedY(self):
        return self.speedY
    
    def update(self, window, dt):
        self.posY = self.posY + self.speedY * dt
        self.posX = self.posX + self.speedX * dt
        increment = 50
        if self.posY <= 0:
            self.posY = 0
            self.speedY = - self.speedY
            if self.speedY < 0:
                self.speedY = self.speedY - increment
            else:
                self.speedY = self.speedY + increment
            if self.speedX <= 0:
                self.speedX = self.speedX - increment
            else:
                self.speedX = self.speedX + increment
        elif self.posY >= window.get_rect()[3] - self.img.get_rect()[3]:
            self.posY = window.get_rect()[3] - self.img.get_rect()[3]
            self.speedY = - self.speedY
            if self.speedY < 0:
                self.speedY = self.speedY - increment
            else:
                self.speedY = self.speedY + increment
            if self.speedX <= 0:
                self.speedX = self.speedX - increment
            else:
                self.speedX = self.speedX + increment
        
        window.blit(self.img, (self.posX,self.posY))

def detectCollision(rect1, rect2):
    #rect (x,y,width,height)
    if rect1[0]+rect1[2] > rect2[0] and rect1[0] < rect2[0]+rect2[2] and rect1[1]+rect1[3] > rect2[1] and rect1[1] < rect2[1]+rect2[3]:
        return True
    else:
        return False

def scoreScreen(window, takeScore, narutoScore):
    #VARIABLES
    isRunning = True
    fpsClock = pygame.time.Clock()
    
    #IMAGES
    imgTake = pygame.image.load("res/stimbreak/takeHead.png").convert_alpha()
    imgNaruto = pygame.image.load("res/stimbreak/narutoHead.png").convert_alpha()
    
    #SOUNDS
    sndGG = pygame.mixer.Sound("res/sound/gg.ogg")
    sndGG.play()
    
    #FONTS AND TEXT
    stdFont = pygame.font.SysFont("Arial", 20)
    txtTakeScore = stdFont.render(u"Take hat %i Punkte erzielt" %(takeScore), 1 , (0,0,0))
    txtNarutoScore = stdFont.render(u"Naruto hat %i Punkte erzielt" %(narutoScore), 1 , (0,0,0))
    txtTakeWon = stdFont.render(u"Take hat gewonnen", 1, (0,0,0))
    txtNarutoWon = stdFont.render(u"Naruto hat gewonnen", 1, (0,0,0))
    txtDraw = stdFont.render(u"Unentschieden", 1, (0,0,0))
    
    
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    if takeScore > narutoScore:
                        return 1
                    elif takeScore < narutoScore:
                        return 2
                    else:
                        return 3
        
        #DRAW
        window.fill((150,150,150))
        window.blit(txtTakeScore,(window.get_rect()[2]/2 - txtTakeScore.get_rect()[2]/2, 20))
        window.blit(txtNarutoScore,(window.get_rect()[2]/2 - txtNarutoScore.get_rect()[2]/2, 50))
        if takeScore > narutoScore:
            window.blit(txtTakeWon,(window.get_rect()[2]/2 - txtTakeWon.get_rect()[2]/2, 150))
            window.blit(imgTake, (window.get_rect()[2]/2 - imgTake.get_rect()[2]/2, 300))
        elif takeScore < narutoScore:
            window.blit(txtNarutoWon,(window.get_rect()[2]/2 - txtNarutoWon.get_rect()[2]/2, 150))
            window.blit(imgNaruto, (window.get_rect()[2]/2 - imgNaruto.get_rect()[2]/2, 300))
        else:
            window.blit(txtDraw,(window.get_rect()[2]/2 - txtDraw.get_rect()[2]/2, 150))
        pygame.display.update()
        fpsClock.tick(60)

def start(window):
    """
    Starts the stimbreak game and handles the entire minigame from
    here on out by itself
    
    Args:
        window (pygame.Surface): the standard window of the programm
    
    Returns:
        0: if the user cancels the game
        1: if Take wins
        2: if Naruto wins
        3: if it is a tie
    """
    
    #VARIABLES
    fpsClock = pygame.time.Clock()
    isRunning = True
    FPS = 150
    increment = 50
    hasBouncedTakeBall = False
    hasBouncedNarutoBall = False
    paddleSpeed = 400 #speed in pixels per second
    ballTakeSpeedX = - random.randint(70, 150)
    ballNarutoSpeedX = random.randint(70,150)
    showManual = True
    dt = 0.0
    
    #IMAGES
    imgBackground = pygame.image.load("res/lepongo/bg.jpg").convert()
    
    #PADDLES
    paddleTake = Paddle(20,100, 10,100, window, (0,0,255), paddleSpeed)
    paddleNaruto = Paddle(window.get_rect()[2]-20, 400, 10,100, window, (255,0,0), paddleSpeed)
    
    #BALLS
    ballTake = Ball(window.get_rect()[2] / 2-25,random.randint(10,600), "res/lepongo/takeBall.png", ballTakeSpeedX, random.randint((ballTakeSpeedX / 2), - ballTakeSpeedX /2))
    ballNaruto = Ball(window.get_rect()[2] / 2-25,random.randint(10,600), "res/lepongo/narutoBall.png", ballNarutoSpeedX,random.randint(-(ballNarutoSpeedX / 2), ballNarutoSpeedX /2))
    
    #FONTS AND TEXT
    stdFont = pygame.font.SysFont("Arial", 20)
    txtScore = stdFont.render(u"%i : %i" %(paddleTake.getScore(), paddleNaruto.getScore()),1,(255,255,255))
    
    #text for the manual
    txtMan0 = stdFont.render(u"ANLEITUNG:",1,(255,255,255))
    txtMan1 = stdFont.render(u"Take steuert den linken Schläger mit 'W' und 'S' nach oben bzw. nach unten.",1,(255,255,255))
    txtMan2 = stdFont.render(u"Naruto steuert den rechten Schläger mit den Pfeiltasten.",1,(255,255,255))
    txtMan3 = stdFont.render(u"Sobald ein Schläger in Bewegung gesetzt wurde, bewegt er sich",1,(255,255,255))
    txtMan4 = stdFont.render(u"solange in eine Richtung, bis er entweder in die entgegengesetzte",1,(255,255,255))
    txtMan5 = stdFont.render(u"Richtung gesteuert wird, oder den Rand des Spielfeldes erreicht.",1,(255,255,255))
    txtMan6 = stdFont.render(u"Immer wenn ein Ball vom Schläger oder von der Wand abprallt, erhöht er",1,(255,255,255))
    txtMan7 = stdFont.render(u"seine Geschwindigkeit.",1,(255,255,255))
    txtMan8 = stdFont.render(u"Es gibt zwei Bälle: einen Take-Ball und einen Naruto-Ball.",1,(255,255,255))
    txtMan9 = stdFont.render(u"Lässt man den 'gegnerischen' Ball in sein Tor, bekommt der Gegenspieler",1,(255,255,255))
    txtMan10 = stdFont.render(u"zwei Punkte. Lässt man seinen eigenen Ball ins Netz bekommt der Gegner",1,(255,255,255))
    txtMan11 = stdFont.render(u"nur einen Punkt. Wer zuerst 10 Punkte hat gewinnt das Spiel.",1,(255,255,255))
    txtMan12 = stdFont.render(u"Nach einem Tor erscheint der Ball wieder in der Mitte des Spielfeldes",1,(255,255,255))
    txtMan13 = stdFont.render(u"und fliegt in einem zufälligen Winkel auf das Tor des Ballbesitzers zu.",1,(255,255,255))
    txtMan14 = stdFont.render(u"Drücke ENTER um das Spiel zu beginnen.",1,(255,255,255))
    
    mantxtList = [txtMan0, txtMan1, txtMan2,txtMan3, txtMan4, txtMan5, txtMan6, txtMan7, txtMan8, txtMan9, txtMan10, txtMan11, txtMan12, txtMan13]
    
    #MANUAL
    manualSurf = pygame.Surface((768,576))
    manualSurf.convert_alpha()
    manualSurf.set_alpha(200)
    for item, i in zip(mantxtList, xrange(1,len(mantxtList)+1)):
        manualSurf.blit(item, (10,i*30))
    manualSurf.blit(txtMan14, (10,manualSurf.get_rect()[3] - txtMan9.get_rect()[3] - 20))
    
    window.blit(imgBackground,(0,0))
    window.blit(txtScore,(window.get_rect()[2]/2 - txtScore.get_rect()[2]/2 -4, 10))
    paddleTake.update(window,dt)
    paddleNaruto.update(window,dt)
    ballTake.update(window,dt)
    ballNaruto.update(window,dt)
    
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = False
                    return 0
                elif event.key == pygame.K_RETURN and showManual:
                    showManual = False
                elif event.key == pygame.K_w and not showManual:
                    paddleTake.setDirection("up")
                elif event.key == pygame.K_s and not showManual:
                    paddleTake.setDirection("down")
                elif event.key == pygame.K_UP and not showManual:
                    paddleNaruto.setDirection("up")
                elif event.key == pygame.K_DOWN and not showManual:
                    paddleNaruto.setDirection("down")
        
        #GAME LOGIC
        dt = fpsClock.tick(FPS) / 1000.0
        
        if not showManual:
            if detectCollision(ballTake.get_rect(), paddleTake.get_rect()) and not hasBouncedTakeBall:
                ballTake.setSpeedX(-ballTake.getSpeedX()+increment)
                hasBouncedTakeBall = True
            elif detectCollision(ballTake.get_rect(), paddleNaruto.get_rect()) and not hasBouncedTakeBall:
                ballTake.setSpeedX(-ballTake.getSpeedX()-increment)
                hasBouncedTakeBall = True
            
            if detectCollision(ballNaruto.get_rect(), paddleTake.get_rect()) and not hasBouncedNarutoBall:
                ballNaruto.setSpeedX(-ballNaruto.getSpeedX()+increment)
                hasBouncedNarutoBall = True
            elif detectCollision(ballNaruto.get_rect(), paddleNaruto.get_rect()) and not hasBouncedNarutoBall:
                ballNaruto.setSpeedX(-ballNaruto.getSpeedX()-increment)
                hasBouncedNarutoBall = True
                
            if hasBouncedTakeBall:
                if ballTake.getSpeedX() > 0:
                    if ballTake.getPosX() > 100:
                        hasBouncedTakeBall = False
                elif ballTake.getSpeedX() < 0:
                    if ballTake.getPosX() < 500:
                        hasBouncedTakeBall = False
            
            if hasBouncedNarutoBall:
                if ballNaruto.getSpeedX() > 0:
                    if ballNaruto.getPosX() > 100:
                        hasBouncedNarutoBall = False
                elif ballNaruto.getSpeedX() < 0:
                    if ballNaruto.getPosX() < 500:
                        hasBouncedNarutoBall = False
            
            if ballTake.getPosX()+ballTake.getImage().get_rect()[2] < 0:
                paddleNaruto.addScore(1)
                txtScore = stdFont.render(u"%i : %i" %(paddleTake.getScore(), paddleNaruto.getScore()),1,(255,255,255))
                ballTake.setPosX(window.get_rect()[2] / 2-25)
                ballTake.setPosY(random.randint(10,600))
                ballTakeSpeedX = - random.randint(70, 150)
                ballTake.setSpeedX(ballTakeSpeedX)
                ballTake.setSpeedY(random.randint((ballTakeSpeedX / 2), - ballTakeSpeedX /2))
            elif ballTake.getPosX() > window.get_rect()[2]:
                paddleTake.addScore(2)
                txtScore = stdFont.render(u"%i : %i" %(paddleTake.getScore(), paddleNaruto.getScore()),1,(255,255,255))
                ballTake.setPosX(window.get_rect()[2] / 2-25)
                ballTake.setPosY(random.randint(10,600))
                ballTakeSpeedX = - random.randint(70, 150)
                ballTake.setSpeedX(ballTakeSpeedX)
                ballTake.setSpeedY(random.randint((ballTakeSpeedX / 2),  -ballTakeSpeedX /2))
            
            if ballNaruto.getPosX()+ ballNaruto.getImage().get_rect()[2] < 0:
                paddleNaruto.addScore(2)
                txtScore = stdFont.render(u"%i : %i" %(paddleTake.getScore(), paddleNaruto.getScore()),1,(255,255,255))
                ballNaruto.setPosX(window.get_rect()[2] / 2-25)
                ballNaruto.setPosY(random.randint(10,600))
                ballNarutoSpeedX = random.randint(70, 150)
                ballNaruto.setSpeedX(ballNarutoSpeedX)
                ballNaruto.setSpeedY(random.randint(-(ballNarutoSpeedX / 2), ballNarutoSpeedX /2))
            elif ballNaruto.getPosX() > window.get_rect()[2]:
                paddleTake.addScore(1)
                txtScore = stdFont.render(u"%i : %i" %(paddleTake.getScore(), paddleNaruto.getScore()),1,(255,255,255))
                ballNaruto.setPosX(window.get_rect()[2] / 2-25)
                ballNaruto.setPosY(random.randint(10,600))
                ballNarutoSpeedX = random.randint(70, 150)
                ballNaruto.setSpeedX(ballNarutoSpeedX)
                ballNaruto.setSpeedY(random.randint(-(ballNarutoSpeedX / 2), ballNarutoSpeedX /2))
            
            if paddleTake.getScore() >= 10 or paddleNaruto.getScore() >= 10:
                return scoreScreen(window, paddleTake.getScore(), paddleNaruto.getScore())
        
        
        
        #DRAW
        if not showManual:
            window.blit(imgBackground,(0,0))
            window.blit(txtScore,(window.get_rect()[2]/2 - txtScore.get_rect()[2]/2 -4, 10))
            paddleTake.update(window,dt)
            paddleNaruto.update(window,dt)
            ballTake.update(window,dt)
            ballNaruto.update(window,dt)
        elif showManual:
            window.blit(manualSurf, (window.get_rect()[2]/2 - manualSurf.get_rect()[2]/2, 100))
        pygame.display.update()

