#! usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, sys, random

class StimbreakPlayer(object):
    """
    Contains the attributes of each player which are needed for this
    game.
    
    Args:
        posX (int): x-coordinate
        posY (int): y-coordinate
        imgUp (pygame.image): image in the upwards position
        imgDown (pygame.image): image in the downwards position
    """
    
    def __init__(self, posX, posY, imgUp, imgDown):
        self.pushUpCounter = 0
        self.imgUp = imgUp
        self.imgDown = imgDown
        self.img = self.imgUp
        self.posX = posX
        self.posY = posY
        self.state = "up"
    
    def getState(self):
        """
        Returns the state the player is in, which can either be "up"
        or "down".
        
        Args:
            no arguments
        
        Returns:
            self.state (str): the state is eiher "up" or "down"
        """
        
        return self.state
        
    
    def setState(self, newState):
        """
        Sets self.state and self.img to either "up" or "down", 
        depending on the given argument.
        
        Args:
            newState (str): can either be "up" or "down".
        
        Returns:
            self.state (str): the new state it was set to.
        """
        
        
        if newState == "up":
            self.img = self.imgUp
            self.state = newState
        elif newState == "down":
            self.img = self.imgDown
            self.state = newState
        else:
            print("Wrong argument was given")
        return self.state
        
    
    def setPosX(self, posX):
        """
        Sets the current X-position to the given argument.
        
        Args:
            posX (int): the new X-position.
        
        Returns:
            self.posX (int): the X-position it was set to.
        """
        
        self.posX = posX
        return self.posX
    
    
    def setPosY(self, posY):
        """
        Sets the current Y-position to the given argument.
        
        Args:
            posY (int): the new Y-position.
        
        Returns:
            self.posY (int): the Y-position it was set to.
        """
        
        self.posY = posY
        return self.posY
        
    
    def getPosition(self):
        """
        Returns the current position in the form (posX, posY)
        
        Args:
            no arguments
        
        Returns:
            (self.posX, self.posY) (tuple): the x-position and 
                                            y-position of the player
        """
        
        return (self.posX, self.posY)
    
    def getImg(self):
        """
        Returns the current image
        
        Args:
            no arguments
        
        Returns:
            self.img (pygame.image): the current image the variable is
                                     set to.
        """
        
        return self.img
        
    
    def addPushUp(self):
        """
        Adds one to the pushUpCounter variable and returns the
        pushUpCounter variable.
        
        Args:
            no arguments
        
        Returns:
            self.pushUpCounter (int): the amount of push ups that the 
                                      player has done.
        """
        
        self.pushUpCounter = self.pushUpCounter + 1
        return self.pushUpCounter
    
    def subtractPushUp(self):
        """
        Subtracts one from the pushUpCounter variable and returns the
        pushUpCounter variable
        
        Args:
            no arguments
        
        Returns:
        self.pushUpCounter (int): the amount of push ups that the
                                  player has done.
        """
        self.pushUpCounter = self.pushUpCounter - 1
        return self.pushUpCounter
        
        
    def getPushUpCounter(self):
        """
        Returns the pushUpCounter varaible
        
        Args:
            no arguments
        
        Returns:
            self.pushUpCounter (int): the amount of push ups that the 
                                      player has done.
        """
        
        return self.pushUpCounter

def scoreScreen(window, takePushUpCounter, narutoPushUpCounter):
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
    txtTakeScore = stdFont.render(u"Take hat %i Liegestütze geschafft" %(takePushUpCounter), 1 , (0,0,0))
    txtNarutoScore = stdFont.render(u"Naruto hat %i Liegestütze geschafft" %(narutoPushUpCounter), 1 , (0,0,0))
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
                    if takePushUpCounter > narutoPushUpCounter:
                        return 1
                    elif takePushUpCounter < narutoPushUpCounter:
                        return 2
                    else:
                        return 3
        
        #DRAW
        window.fill((150,150,150))
        window.blit(txtTakeScore,(window.get_rect()[2]/2 - txtTakeScore.get_rect()[2]/2, 20))
        window.blit(txtNarutoScore,(window.get_rect()[2]/2 - txtNarutoScore.get_rect()[2]/2, 50))
        if takePushUpCounter > narutoPushUpCounter:
            window.blit(txtTakeWon,(window.get_rect()[2]/2 - txtTakeWon.get_rect()[2]/2, 150))
            window.blit(imgTake, (window.get_rect()[2]/2 - imgTake.get_rect()[2]/2, 300))
        elif takePushUpCounter < narutoPushUpCounter:
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
    isRunning = True    #manages the execution of the game loop
    showManual = True  #is True at the beginning when it shows the manual and pauses the game
    fpsClock = pygame.time.Clock()
    takeKeyList = ["w","s","a","d"]
    narutoKeyList = ["up", "down", "left", "right"]
    takeRndKeyChoice = random.choice(takeKeyList)
    narutoRndKeyChoice = random.choice(narutoKeyList)
    takeNeedsNewKey = False
    narutoNeedsNewKey = False
    dt = 0.0
    timeLeft = 30.0
    
    
    #IMAGES
    imgTakeUp = pygame.image.load('res/stimbreak/takeUp.png').convert_alpha()
    imgTakeDown = pygame.image.load('res/stimbreak/takeDown.png').convert_alpha()
    imgNarutoUp = pygame.image.load('res/stimbreak/narutoUp.png').convert_alpha()
    imgNarutoDown = pygame.image.load('res/stimbreak/narutoDown.png').convert_alpha()
    imgKeyW = pygame.image.load("res/stimbreak/keyW.png").convert()
    imgKeyS = pygame.image.load("res/stimbreak/keyS.png").convert()
    imgKeyA = pygame.image.load("res/stimbreak/keyA.png").convert()
    imgKeyD = pygame.image.load("res/stimbreak/keyD.png").convert()
    imgKeyArrowUp = pygame.image.load("res/stimbreak/keyArrowUp.png").convert()
    imgKeyArrowDown = pygame.image.load("res/stimbreak/keyArrowDown.png").convert()
    imgKeyArrowLeft = pygame.image.load("res/stimbreak/keyArrowLeft.png").convert()
    imgKeyArrowRight = pygame.image.load("res/stimbreak/keyArrowRight.png").convert()
    imgBackground = pygame.image.load("res/stimbreak/bg.png").convert()
    
    dictKeyImages = {
                        "w"     : imgKeyW,
                        "s"     : imgKeyS,
                        "a"     : imgKeyA,
                        "d"     : imgKeyD,
                        "up"    : imgKeyArrowUp,
                        "down"  : imgKeyArrowDown,
                        "left"  : imgKeyArrowLeft,
                        "right" : imgKeyArrowRight
                    }
    #PLAYERS
    take = StimbreakPlayer(10,300, imgTakeUp, imgTakeDown)
    naruto = StimbreakPlayer(550,300, imgNarutoUp, imgNarutoDown)
    
    #FONTS AND TEXT
    stdFont = pygame.font.SysFont("Arial", 20)
    txtPushUps = stdFont.render(u"Liegestütze:", 1, (0,0,0))
    txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
    txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
    txtTimeLeft = stdFont.render(str(int(timeLeft)),1,(255,255,255))
    txtTime = stdFont.render(u"Verbleibende Zeit", 1, (255,255,255))
    
    #text for the manual
    txtMan0 = stdFont.render(u"ANLEITUNG:",1,(255,255,255))
    txtMan1 = stdFont.render(u"Jedem Spieler werden zufällige Tasten angezeigt, die er drücken muss.",1,(255,255,255))
    txtMan2 = stdFont.render(u"Für Take können die Tasten 'W', 'A', 'S' oder 'D' erscheinen.",1,(255,255,255))
    txtMan3 = stdFont.render(u"Naruto bekommt eine der Pfeiltasten zugewiesen.",1,(255,255,255))
    txtMan4 = stdFont.render(u"Für jede richtig gedrückte Taste wird eine halbe Liegestütze ausgeführt.",1,(255,255,255))
    txtMan5 = stdFont.render(u"Drückt man also zweimal die korrekte Taste hat man eine komplette ",1,(255,255,255))
    txtMan6 = stdFont.render(u"Liegestütze ausgeführt und bekommt diese gut geschrieben.",1,(255,255,255))
    txtMan7 = stdFont.render(u"Sollte man jedoch eine falsche Taste drücken, wird eine Liegestütze",1,(255,255,255))
    txtMan8 = stdFont.render(u"abgezogen. Wer am Ende die meisten Liegestütze hat gewinnt das Spiel.",1,(255,255,255))
    txtMan9 = stdFont.render(u"Drücke ENTER um das Spiel zu beginnen.",1,(255,255,255))
    
    mantxtList = [txtMan0, txtMan1, txtMan2,txtMan3, txtMan4, txtMan5, txtMan6, txtMan7, txtMan8]
    
    #MANUAL
    manualSurf = pygame.Surface((768,576))
    manualSurf.convert_alpha()
    manualSurf.set_alpha(200)
    for item, i in zip(mantxtList, xrange(1,len(mantxtList)+1)):
        manualSurf.blit(item, (10,i*30))
    manualSurf.blit(txtMan9, (10,manualSurf.get_rect()[3] - txtMan9.get_rect()[3] - 20))
    
    
    #GAME LOOP
    while isRunning:
        #USER INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and not takeNeedsNewKey and not showManual:
                    if takeRndKeyChoice == "w":
                        if take.getState() == "up":
                            take.setState("down")
                        elif take.getState() == "down":
                            take.setState("up")
                            take.addPushUp()
                            txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                        takeNeedsNewKey = True
                    elif takeRndKeyChoice != "w" and take.getPushUpCounter() > 0:
                        take.subtractPushUp()
                        txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_s and not takeNeedsNewKey and not showManual:
                    if takeRndKeyChoice == "s":
                        if take.getState() == "up":
                            take.setState("down")
                        elif take.getState() == "down":
                            take.setState("up")
                            take.addPushUp()
                            txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                        takeNeedsNewKey = True
                    elif takeRndKeyChoice != "s" and take.getPushUpCounter() > 0:
                        take.subtractPushUp()
                        txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_a and not takeNeedsNewKey and not showManual:
                    if takeRndKeyChoice == "a":
                        if take.getState() == "up":
                            take.setState("down")
                        elif take.getState() == "down":
                            take.setState("up")
                            take.addPushUp()
                            txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                        takeNeedsNewKey = True
                    elif takeRndKeyChoice != "a" and take.getPushUpCounter() > 0:
                        take.subtractPushUp()
                        txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_d and not takeNeedsNewKey and not showManual:
                    if takeRndKeyChoice == "d":
                        if take.getState() == "up":
                            take.setState("down")
                        elif take.getState() == "down":
                            take.setState("up")
                            take.addPushUp()
                            txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                        takeNeedsNewKey = True
                    elif takeRndKeyChoice != "d" and take.getPushUpCounter() > 0:
                        take.subtractPushUp()
                        txtTakeScore = stdFont.render(str(take.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_UP and not narutoNeedsNewKey and not showManual:
                    if narutoRndKeyChoice == "up":
                        if naruto.getState() == "up":
                            naruto.setState("down")
                        elif naruto.getState() == "down":
                            naruto.setState("up")
                            naruto.addPushUp()
                            txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                        narutoNeedsNewKey = True
                    elif narutoRndKeyChoice != "up" and naruto.getPushUpCounter() > 0:
                        naruto.subtractPushUp()
                        txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_DOWN and not narutoNeedsNewKey and not showManual:
                    if narutoRndKeyChoice == "down":
                        if naruto.getState() == "up":
                            naruto.setState("down")
                        elif naruto.getState() == "down":
                            naruto.setState("up")
                            naruto.addPushUp()
                            txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                        narutoNeedsNewKey = True
                    elif narutoRndKeyChoice != "down" and naruto.getPushUpCounter() > 0:
                        naruto.subtractPushUp()
                        txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_LEFT and not narutoNeedsNewKey and not showManual:
                    if narutoRndKeyChoice == "left":
                        if naruto.getState() == "up":
                            naruto.setState("down")
                        elif naruto.getState() == "down":
                            naruto.setState("up")
                            naruto.addPushUp()
                            txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                        narutoNeedsNewKey = True
                    elif narutoRndKeyChoice != "left" and naruto.getPushUpCounter() > 0:
                        naruto.subtractPushUp()
                        txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_RIGHT and not narutoNeedsNewKey and not showManual:
                    if narutoRndKeyChoice == "right":
                        if naruto.getState() == "up":
                            naruto.setState("down")
                        elif naruto.getState() == "down":
                            naruto.setState("up")
                            naruto.addPushUp()
                            txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                        narutoNeedsNewKey = True
                    elif narutoRndKeyChoice != "right" and naruto.getPushUpCounter() > 0:
                        naruto.subtractPushUp()
                        txtNarutoScore = stdFont.render(str(naruto.getPushUpCounter()), 1, (0,0,0))
                elif event.key == pygame.K_RETURN and showManual:
                    showManual = False
                elif event.key == pygame.K_ESCAPE:
                    return 0
        
        #GAME LOGIC
        dt = fpsClock.tick(60) / 1000.0 #delta time since the last loop iteration
        
        if not showManual:
            if timeLeft > 0.0:
                timeLeft = timeLeft - dt
            else:
                timeLeft = 0.0
                isRunning = False
                return scoreScreen(window, take.getPushUpCounter(), naruto.getPushUpCounter())
            txtTimeLeft = stdFont.render(str(int(timeLeft)),1,(255,255,255))
            
            if takeNeedsNewKey:
                takeRndKeyChoice = random.choice(takeKeyList)
                takeNeedsNewKey = False
            if narutoNeedsNewKey:
                narutoRndKeyChoice = random.choice(narutoKeyList)
                narutoNeedsNewKey = False
        
        #DRAW
        window.blit(imgBackground,(0,0))
        window.blit(take.getImg(), take.getPosition())
        window.blit(naruto.getImg(), naruto.getPosition())
        window.blit(txtPushUps,(185,20))
        window.blit(txtPushUps,(725,20))
        window.blit(dictKeyImages[takeRndKeyChoice], (210,80))
        window.blit(dictKeyImages[narutoRndKeyChoice], (750,80))
        window.blit(txtTakeScore,(txtPushUps.get_rect()[2]+185+5,20))
        window.blit(txtNarutoScore, (txtPushUps.get_rect()[2]+725+5,20))
        window.blit(txtTimeLeft, (512-txtTimeLeft.get_rect()[2]/2, 50))
        window.blit(txtTime, (512-txtTime.get_rect()[2]/2, 20))
        if showManual:
            window.blit(manualSurf, (window.get_rect()[2]/2 - manualSurf.get_rect()[2]/2, 100))
        pygame.display.update()
        
    
