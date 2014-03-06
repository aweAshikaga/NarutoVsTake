#! usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, sys, random

class Rect(object):
    
    def __init__(self, color, rect, image, width=0):
        self.rect = rect
        self.color = color
        self.width = width
        self.img = image
        self.blendSurf = pygame.Surface((self.img.get_rect()[2], self.img.get_rect()[3])).convert()
        self.blendSurf.fill(self.color)
        self.alpha = 255
        self.fadeIn = False
        self.fadeOut = False
        self.timePassed = 0.0
        self.isDoneShowing = True
    
    def getIsdoneShowing(self):
        return self.isDoneShowing
    
    def setAlpha(self, value):
        self.alpha = value
    
    def setIsDoneShowing(self, value):
        self.isDoneShowing = value
    
    def setFadeIn(self, value):
        self.fadeIn = value
    
    def get_rect(self):
        return self.rect
    
    def update(self, dt):
        self.timePassed = self.timePassed + dt
        if self.timePassed >= 0.02:
            if self.fadeIn:
                self.alpha = self.alpha - 5
                self.blendSurf.set_alpha(self.alpha)
                if self.alpha == 0:
                    self.fadeIn = False
                    self.fadeOut = True
            elif self.fadeOut:
                self.alpha = self.alpha + 5
                self.blendSurf.set_alpha(self.alpha)
                if self.alpha == 255:
                    self.fadeOut = False
                    self.isDoneShowing = True
            self.timePassed = 0.0
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect, self.width)
        if self.fadeIn or self.fadeOut:
            window.blit(self.img, (self.rect[0]+self.rect[2]/2-self.img.get_rect()[2]/2, self.rect[1]+self.rect[3]/2-self.img.get_rect()[3]/2))
            window.blit(self.blendSurf, (self.rect[0]+self.rect[2]/2-self.img.get_rect()[2]/2, self.rect[1]+self.rect[3]/2-self.img.get_rect()[3]/2))


def detectMouseclickArea(mouseX, mouseY, rectBrown, rectBlue, rectRed, rectSilver):
    if mouseX >= rectBrown[0] and mouseX <= rectBrown[0] + rectBrown[2] and mouseY >= rectBrown[1] and mouseY <= rectBrown[1] + rectBrown[3]:
        return "brownHit"
    elif mouseX >= rectBlue[0] and mouseX <= rectBlue[0] + rectBlue[2] and mouseY >= rectBlue[1] and mouseY <= rectBlue[1] + rectBlue[3]:
        return "blueHit"
    elif mouseX >= rectRed[0] and mouseX <= rectRed[0] + rectRed[2] and mouseY >= rectRed[1] and mouseY <= rectRed[1] + rectRed[3]:
        return "redHit"
    elif mouseX >= rectSilver[0] and mouseX <= rectSilver[0] + rectSilver[2] and mouseY >= rectSilver[1] and mouseY <= rectSilver[1] + rectSilver[3]:
        return "silverHit"
    else:
        return "noHit"

def scoreScreen(window, winner, length):
    #VARIABLES
    isRunning = True
    fpsClock = pygame.time.Clock()
    if winner == "Take":
        takeScore = 1
        narutoScore = 0
    else:
        takeScore = 0
        narutoScore = 1
    
    #IMAGES
    imgTake = pygame.image.load("res/stimbreak/takeHead.png").convert_alpha()
    imgNaruto = pygame.image.load("res/stimbreak/narutoHead.png").convert_alpha()
    
    #SOUNDS
    sndGG = pygame.mixer.Sound("res/sound/gg.ogg")
    sndGG.play()
    
    #FONTS AND TEXT
    stdFont = pygame.font.SysFont("Arial", 20)
    txtWinner = stdFont.render(u"Der Gewinner ist: %s!" %(winner), 1 , (0,0,0))
    if winner == "Take":
        txtWrongButton = stdFont.render(u"Naruto hat auf ein falsches Rechteck gedrückt", 1, (0,0,0))
    else:
        txtWrongButton = stdFont.render(u"Take hat auf ein falsches Rechteck gedrückt", 1, (0,0,0))
    txtSeqLength = stdFont.render(u"Die Sequenz hatte eine Länge von %i." %(length), 1 , (0,0,0))
    
    
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
        window.blit(txtWrongButton,(window.get_rect()[2]/2 - txtWrongButton.get_rect()[2]/2, 20))
        window.blit(txtSeqLength,(window.get_rect()[2]/2 - txtSeqLength.get_rect()[2]/2, 50))
        if takeScore > narutoScore:
            window.blit(txtWinner,(window.get_rect()[2]/2 - txtWinner.get_rect()[2]/2, 150))
            window.blit(imgTake, (window.get_rect()[2]/2 - imgTake.get_rect()[2]/2, 300))
        elif takeScore < narutoScore:
            window.blit(txtWinner,(window.get_rect()[2]/2 - txtWinner.get_rect()[2]/2, 150))
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
    isRunning = True
    showingSequence = True
    showManual = True
    FPS = 100
    fpsClock = pygame.time.Clock()
    dt = 0.0
    newRoundShowTime = 4.0
    timePassed = newRoundShowTime
    choiceList = ["brown","blue","red","silver"]
    playSequence = []
    playSequenceCounter = 0
    playSequence.append(random.choice(choiceList))
    playSequence.append(random.choice(choiceList))
    playSequence.append(random.choice(choiceList))
    playerList = ["take", "naruto"]
    playersTurn = random.choice(playerList)
    txtCorrectAlpha= 0
    firstIteration = True
    isFirstRound = True
    
    BROWN = (109,56,7)
    BLUE = (45,119,168)
    RED = (200,0,0)
    SILVER = (227,228,229)
    colorTxtCorrect = (255,168,0)

    
    #IMAGES
    imgCouch = pygame.image.load("res/mmsfemsm/ggcouch.png").convert_alpha()
    imgHouse = pygame.image.load("res/mmsfemsm/gghouse.png").convert_alpha()
    imgStimtime = pygame.image.load("res/mmsfemsm/stimtime.png").convert_alpha()
    imgViking = pygame.image.load("res/mmsfemsm/viking.png").convert_alpha()
    
    #RECTS
    rectBrown = Rect(BROWN, (window.get_rect()[2]/2-300-25,window.get_rect()[3]/2-300-25,300,300), imgCouch, 0)
    rectBlue = Rect(BLUE, (window.get_rect()[2]/2+25,window.get_rect()[3]/2-300-25,300,300), imgHouse, 0)
    rectRed = Rect(RED, (window.get_rect()[2]/2-300-25,window.get_rect()[3]/2+25,300,300), imgStimtime, 0)
    rectSilver = Rect(SILVER, (window.get_rect()[2]/2+25,window.get_rect()[3]/2+25,300,300), imgViking,0)
    
    #FONTS AND TEXT
    stdFont = pygame.font.SysFont("Arial", 20)
    stdFont2 = pygame.font.SysFont("Arial", 35)
    txtHasTurn = stdFont.render(u"An der Reihe:", 1 , (255,255,255))
    txtTake = stdFont.render(u"Take",1, BLUE)
    txtNaruto = stdFont.render(u"Naruto",1,RED)
    txtCorrect = stdFont2.render(u"RICHTIG. %s ist dran" %(playersTurn), 0, colorTxtCorrect)
    txtFirstRound = stdFont2.render(u"ERSTE RUNDE: %s beginnt." % (playersTurn), 0, colorTxtCorrect)
    txtCorrect.set_alpha(txtCorrectAlpha)
    
    #text for the manual
    txtMan0 = stdFont.render(u"ANLEITUNG:",1,(255,255,255))
    txtMan1 = stdFont.render(u"Es wird eine zufällige Sequenz gespielt, welche von den Spielern abwechselnd",1,(255,255,255))
    txtMan2 = stdFont.render(u"nachgespielt werden muss. Der Startspieler wird vom Programm zufällig",1,(255,255,255))
    txtMan3 = stdFont.render(u"ausgewählt.",1,(255,255,255))
    txtMan4 = stdFont.render(u"Man spielt die Sequenz indem man mit der Maus in der richtigen Reihenfolge",1,(255,255,255))
    txtMan5 = stdFont.render(u"auf die Rechtecke klickt. Sobald man auf ein falsches Rechteck klickt",1,(255,255,255))
    txtMan6 = stdFont.render(u"ist das Spiel vorbei und der andere Spieler hat gewonnen.",1,(255,255,255))
    txtMan7 = stdFont.render(u"Nach jeder erfolgreichen Runde wird die Sequenz nochmal von vorne gespielt",1,(255,255,255))
    txtMan8 = stdFont.render(u"und die Sequenz wird um eins erhöht. Außerdem wechselt selbstverständlich",1,(255,255,255))
    txtMan9 = stdFont.render(u"nach jeder Runde der Spieler, welcher an der Reihe ist.",1,(255,255,255))
    txtMan10 = stdFont.render(u"Sollte der Startspieler direkt in der ersten Runde versagen, hat der",1,(255,255,255))
    txtMan11 = stdFont.render(u"andere Spieler gewonnen, ohne dafür etwas getan zu haben.",1,(255,255,255))
    txtMan12 = stdFont.render(u"Die Startsequenz hat eine Länge von drei.",1,(255,255,255))
    txtMan13 = stdFont.render(u"",1,(255,255,255))
    txtMan14 = stdFont.render(u"Drücke ENTER um das Spiel zu beginnen.",1,(255,255,255))
    
    mantxtList = [txtMan0, txtMan1, txtMan2,txtMan3, txtMan4, txtMan5, txtMan6, txtMan7, txtMan8, txtMan9, txtMan10, txtMan11, txtMan12, txtMan13]
    
    #MANUAL
    manualSurf = pygame.Surface((768,576))
    manualSurf.convert_alpha()
    manualSurf.set_alpha(200)
    for item, i in zip(mantxtList, xrange(1,len(mantxtList)+1)):
        manualSurf.blit(item, (10,i*30))
    manualSurf.blit(txtMan14, (10,manualSurf.get_rect()[3] - txtMan9.get_rect()[3] - 20))
    
    #SOUNDS
    sndC = pygame.mixer.Sound("res/mmsfemsm/c.ogg")
    sndD = pygame.mixer.Sound("res/mmsfemsm/d.ogg")
    sndE = pygame.mixer.Sound("res/mmsfemsm/e.ogg")
    sndF = pygame.mixer.Sound("res/mmsfemsm/f.ogg")
    
    
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    showManual = False
                elif event.key == pygame.K_ESCAPE:
                    isRunning = False
                    return 0
            elif event.type == pygame.MOUSEBUTTONDOWN and not showingSequence and not showManual:
                mouseX, mouseY = event.pos
                hitRect = detectMouseclickArea(mouseX,mouseY, rectBrown.get_rect(), rectBlue.get_rect(), rectRed.get_rect(), rectSilver.get_rect())
                if playSequence[playSequenceCounter] == "brown":
                    if hitRect == "brownHit":
                        sndC.play()
                        rectBrown.setFadeIn(True)
                        rectBrown.setAlpha(255)
                        rectBrown.setIsDoneShowing(False)
                        playSequenceCounter = playSequenceCounter + 1
                        if playSequenceCounter == len(playSequence):
                            playSequence.append(random.choice(choiceList))
                            playSequenceCounter = 0
                            showingSequence = True
                            timePassed = newRoundShowTime
                            if playersTurn == "take":
                                playersTurn = "naruto"
                            elif playersTurn == "naruto":
                                playersTurn = "take"
                            txtCorrect = stdFont2.render(u"RICHTIG. %s ist dran" %(playersTurn), 0, colorTxtCorrect)
                    elif hitRect == "noHit":
                        pass
                    else:
                        if playersTurn == "take":
                            return scoreScreen(window, "Naruto", len(playSequence))
                        elif playersTurn == "naruto":
                            return scoreScreen(window, "Take", len(playSequence))
                elif playSequence[playSequenceCounter] == "blue":
                    if hitRect == "blueHit":
                        sndD.play()
                        rectBlue.setFadeIn(True)
                        rectBlue.setAlpha(255)
                        rectBlue.setIsDoneShowing(False)
                        playSequenceCounter = playSequenceCounter + 1
                        if playSequenceCounter == len(playSequence):
                            playSequence.append(random.choice(choiceList))
                            playSequenceCounter = 0
                            showingSequence = True
                            timePassed = newRoundShowTime
                            if playersTurn == "take":
                                playersTurn = "naruto"
                            elif playersTurn == "naruto":
                                playersTurn = "take"
                            txtCorrect = stdFont2.render(u"RICHTIG. %s ist dran" %(playersTurn), 0, colorTxtCorrect)
                    elif hitRect == "noHit":
                        pass
                    else:
                        if playersTurn == "take":
                            return scoreScreen(window, "Naruto", len(playSequence))
                        elif playersTurn == "naruto":
                            return scoreScreen(window, "Take", len(playSequence))
                elif playSequence[playSequenceCounter] == "red":
                    if hitRect == "redHit":
                        sndE.play()
                        rectRed.setFadeIn(True)
                        rectRed.setAlpha(255)
                        rectRed.setIsDoneShowing(False)
                        playSequenceCounter = playSequenceCounter + 1
                        if playSequenceCounter == len(playSequence):
                            playSequence.append(random.choice(choiceList))
                            playSequenceCounter = 0
                            showingSequence = True
                            timePassed = newRoundShowTime
                            if playersTurn == "take":
                                playersTurn = "naruto"
                            elif playersTurn == "naruto":
                                playersTurn = "take"
                            txtCorrect = stdFont2.render(u"RICHTIG. %s ist dran" %(playersTurn), 0, colorTxtCorrect)
                    elif hitRect == "noHit":
                        pass
                    else:
                        if playersTurn == "take":
                            return scoreScreen(window, "Naruto", len(playSequence))
                        elif playersTurn == "naruto":
                            return scoreScreen(window, "Take", len(playSequence))
                elif playSequence[playSequenceCounter] == "silver":
                    if hitRect == "silverHit":
                        sndF.play()
                        rectSilver.setFadeIn(True)
                        rectSilver.setAlpha(255)
                        rectSilver.setIsDoneShowing(False)
                        playSequenceCounter = playSequenceCounter + 1
                        if playSequenceCounter == len(playSequence):
                            playSequence.append(random.choice(choiceList))
                            playSequenceCounter = 0
                            showingSequence = True
                            timePassed = newRoundShowTime
                            if playersTurn == "take":
                                playersTurn = "naruto"
                            elif playersTurn == "naruto":
                                playersTurn = "take"
                            txtCorrect = stdFont2.render(u"RICHTIG. %s ist dran" %(playersTurn), 0, colorTxtCorrect)
                    elif hitRect == "noHit":
                        pass
                    else:
                        if playersTurn == "take":
                            return scoreScreen(window, "Naruto", len(playSequence))
                        elif playersTurn == "naruto":
                            return scoreScreen(window, "Take", len(playSequence))
                        
                
        #LOGIC
        dt = fpsClock.tick(FPS) / 1000.0
        if not showManual:
            if timePassed > 0.0:
                if not isFirstRound:
                    if txtCorrectAlpha <=250:
                        txtCorrectAlpha = txtCorrectAlpha + 5
                    txtCorrect.set_alpha(txtCorrectAlpha)
                    timePassed = timePassed - dt
                else:
                    if txtCorrectAlpha <= 250:
                        txtCorrectAlpha = txtCorrectAlpha + 5
                    txtFirstRound.set_alpha(txtCorrectAlpha)
                    timePassed = timePassed -dt
            elif timePassed <= 0.0:
                timePassed = 0.0
                isFirstRound = False
            
            #showing the sequence
            if showingSequence and timePassed == 0.0:
                if playSequence[playSequenceCounter] == "brown":
                    if firstIteration:
                        sndC.play()
                        rectBrown.setFadeIn(True)
                        rectBrown.setIsDoneShowing(False)
                        firstIteration = False
                    if rectBrown.getIsdoneShowing():
                        playSequenceCounter = playSequenceCounter + 1
                        firstIteration = True
                        if playSequenceCounter == len(playSequence):
                            showingSequence = False
                            playSequenceCounter = 0
                elif playSequence[playSequenceCounter] == "blue":
                    if firstIteration:
                        sndD.play()
                        rectBlue.setFadeIn(True)
                        rectBlue.setIsDoneShowing(False)
                        firstIteration = False
                    if rectBlue.getIsdoneShowing():
                        playSequenceCounter = playSequenceCounter + 1
                        firstIteration = True
                        if playSequenceCounter == len(playSequence):
                            showingSequence = False
                            playSequenceCounter = 0
                elif playSequence[playSequenceCounter] == "red":
                    if firstIteration:
                        sndE.play()
                        rectRed.setFadeIn(True)
                        rectRed.setIsDoneShowing(False)
                        firstIteration = False
                    if rectRed.getIsdoneShowing():
                        playSequenceCounter = playSequenceCounter + 1
                        firstIteration = True
                        if playSequenceCounter == len(playSequence):
                            showingSequence = False
                            playSequenceCounter = 0
                elif playSequence[playSequenceCounter] == "silver":
                    if firstIteration:
                        sndF.play()
                        rectSilver.setFadeIn(True)
                        rectSilver.setIsDoneShowing(False)
                        firstIteration = False
                    if rectSilver.getIsdoneShowing():
                        playSequenceCounter = playSequenceCounter + 1
                        firstIteration = True
                        if playSequenceCounter == len(playSequence):
                            showingSequence = False
                            playSequenceCounter = 0
            
            rectBrown.update(dt)
            rectBlue.update(dt)
            rectRed.update(dt)
            rectSilver.update(dt)
        
        #DRAW
        window.fill((50,50,50))
        rectBrown.draw(window)
        rectBlue.draw(window)
        rectRed.draw(window)
        rectSilver.draw(window)
        window.blit(txtHasTurn, (10,10))
        
        if not showManual:
            if timePassed > 0.0:
                if isFirstRound:
                    window.blit(txtFirstRound, (window.get_rect()[2]/2 - txtFirstRound.get_rect()[2]/2, window.get_rect()[3]/2 - txtFirstRound.get_rect()[3]/2))
                else:
                    window.blit(txtCorrect, (window.get_rect()[2]/2 - txtCorrect.get_rect()[2]/2, window.get_rect()[3]/2 - txtCorrect.get_rect()[3]/2))
            if playersTurn == "take":
                window.blit(txtTake, (10, 10 + txtHasTurn.get_rect()[3]+5))
            elif playersTurn == "naruto":
                window.blit(txtNaruto, (10, 10 + txtHasTurn.get_rect()[3]+5))
        else:
            window.blit(manualSurf, (window.get_rect()[2]/2 - manualSurf.get_rect()[2]/2, 100))
        pygame.display.update()
