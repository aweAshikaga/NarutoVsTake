#! usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, os, sys
import globalObjects as go
import stimbreak, lepongo, mmsfemsm
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
os.environ['SDL_VIDEO_CENTERED'] = '1'
SCREENSIZE = (1024,768)



def menu(window, take, naruto):
    #VARIABLES
    isRunning = True
    fpsClock = pygame.time.Clock()
    timePassed = 0.0
    choice = 0  #keeps track of which menu choice is currently selected
                #0: Stimbreak
                #1: LePongo
                #2: Muss man sich fairerweise einfach mal so merken
                #3: Quit
    maxChoice = 4
    
    #SOUNDS
    sndMenuSelect = pygame.mixer.Sound("res/sound/menu_select.wav")
    
    #IMAGES
    imgLogo = pygame.image.load("res/logo.png").convert()
    imgTakeHead = pygame.image.load("res/takeHead.png").convert_alpha()
    imgNarutoHead = pygame.image.load("res/narutoHead.png").convert_alpha()
    
    #FONT
    stdFont = pygame.font.SysFont("Arial", 30)
    stdFont2 = pygame.font.SysFont("Arial", 20)
    txtStimbreak = stdFont.render(u"Stimbreak", 1, (200,0,0))
    txtLePongo = stdFont.render(u"LePongo",1,(200,0,0))
    txtMmsfemsm = stdFont.render(u"Muss man sich fairerweise einfach mal so merken",1,(200,0,0))
    txtEnd = stdFont.render(u"Beenden", 1, (200,0,0))
    txtScore = stdFont2.render(u"Spielstand", 1 , (0,0,0))
    txtTake = stdFont2.render(u"Take: %i" %(take.getScore()),1,(0,0,0))
    txtNaruto = stdFont2.render(u"Naruto: %i" %(naruto.getScore()), 1, (0,0,0))
    
    dictTxt =   {
                    0   :   txtStimbreak,
                    1   :   txtLePongo,
                    2   :   txtMmsfemsm,
                    3   :   txtEnd
                }

    
    
    #SELECT SURFACE
    selectSurf = pygame.Surface((txtStimbreak.get_rect()[2]+20, txtStimbreak.get_rect()[3]))
    selectSurf.convert_alpha()
    selectSurf.set_alpha(100)
    selectSurf.fill((0,0,0))
    
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_UP:
                    if choice > 0:
                        choice = choice - 1
                        sndMenuSelect.play()
                        selectSurf = pygame.transform.scale(selectSurf, (dictTxt[choice].get_rect()[2]+20, dictTxt[choice].get_rect()[3]))
                elif event.key == pygame.K_DOWN:
                    if choice < maxChoice:
                        choice = choice + 1
                        sndMenuSelect.play()
                        selectSurf = pygame.transform.scale(selectSurf, (dictTxt[choice].get_rect()[2]+20, dictTxt[choice].get_rect()[3]))
                elif event.key == pygame.K_RETURN:
                    if choice == 0:
                        return 0
                    elif choice == 1:
                        return 1
                    elif choice == 2:
                        return 2
                    elif choice == 3:
                        return 3
                        
        #LOGIC
        dt = fpsClock.tick(60) / 1000.0
        timePassed = timePassed + dt
        
        
        #DRAW
        window.fill((50,50,50))
        window.blit(txtScore, (window.get_rect()[2] - imgLogo.get_rect()[2]-30,35+imgLogo.get_rect()[3]))
        window.blit(txtTake, (window.get_rect()[2] - imgLogo.get_rect()[2]-30,35+imgLogo.get_rect()[3]+txtScore.get_rect()[3]))
        window.blit(txtNaruto, (window.get_rect()[2] - imgLogo.get_rect()[2]-30,35+imgLogo.get_rect()[3]+txtScore.get_rect()[3]*2))
        window.blit(imgLogo, (window.get_rect()[2]-imgLogo.get_rect()[2]-30,30))
        window.blit(imgNarutoHead, (150,40))
        window.blit(imgTakeHead, (750,350))
        window.blit(selectSurf, (40,400+(txtStimbreak.get_rect()[3]+20)*choice))
        window.blit(txtStimbreak, (50,400))
        window.blit(txtLePongo, (50, 400+txtStimbreak.get_rect()[3] + 20))
        window.blit(txtMmsfemsm, (50, 400+(txtStimbreak.get_rect()[3] + 20)*2))
        window.blit(txtEnd,(50,400 + (txtStimbreak.get_rect()[3] + 20) *3))
        pygame.display.update()

def intro(window):
    
    #IMAGES
    imgLogo = pygame.image.load("res/logo.png").convert()
    
    #VARIABLES
    isPlaying = True
    dt = 0.0
    timePassed = 0.0
    speed = 200 #in Pixels per second
    fpsClock = pygame.time.Clock()
    posLogoX = window.get_rect()[2]/2 - imgLogo.get_rect()[2]/2
    posLogoY = window.get_rect()[3]/2 - imgLogo.get_rect()[3]/2
    destinationX = window.get_rect()[2]-imgLogo.get_rect()[2]-30
    destinationY = 30
    destinationReached = False
    
    vectorX = destinationX - posLogoX
    vectorY = destinationY - posLogoY
    magnitude = (vectorX**2 + vectorY**2)**0.5
    vectorX = vectorX / magnitude
    vectorY = vectorY / magnitude
    
    #SOUND
    sndIntro = pygame.mixer.Sound("res/sound/intro.ogg")
    sndIntro.play()
    
    while isPlaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                elif event.key == pygame.K_RETURN:
                    return 0
        
        dt = fpsClock.tick(60) / 1000.0
        timePassed = timePassed + dt
        
        if posLogoX >= destinationX:
            posLogoX = destinationX
            posLogoY = destinationY
            destinationReached = True
            isPlaying = False
        
        if timePassed >= 1.0 and not destinationReached:
            posLogoX = posLogoX + vectorX * dt * speed
            posLogoY = posLogoY + vectorY * dt * speed
        
        #DRAW
        window.fill((0,0,0))
        window.blit(imgLogo, (posLogoX, posLogoY))
        pygame.display.update()

def gameInit():
    imgIcon = pygame.image.load("res/nvst.png")
    pygame.display.set_icon(imgIcon)
    window = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption("NARUTO VS TAKE")
    take = go.Player()
    naruto = go.Player()
    winner = 0
    intro(window)
    
    isChoosing = True
    while isChoosing:
        choice = menu(window, take, naruto)
        if choice == 0:
            winner = stimbreak.start(window)
        elif choice == 1:
            winner = lepongo.start(window)
        elif choice == 2:
            winner = mmsfemsm.start(window)
        elif choice == 3:
            isChoosing = False
            
        if winner == 1:
                take.addToScore(1)
        elif winner == 2:
                naruto.addToScore(1)

def main():
    pygame.init()
    gameInit()
    pygame.quit()
    

if __name__ == "__main__":
    main()
