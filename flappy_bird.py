import random, pygame, time, threading

pygame.display.init()

WIDTH = 500
HEIGHT = 600


#################
#DEFINING-ACTORS#
#################


#Background
background = Actor('background', pos=(250, 250))
ground = Actor('ground')
ground2 = Actor('ground')

#Obsticals
pipe1Up = Actor('pipe_face_up')
pipe2Up = Actor('pipe_face_up')
pipe3Up = Actor('pipe_face_up')
pipe4Up = Actor('pipe_face_up')
pipe1Down = Actor('pipe_face_down')
pipe2Down = Actor('pipe_face_down')
pipe3Down = Actor('pipe_face_down')
pipe4Down = Actor('pipe_face_down')

#Player
bird = Actor("bird1", pos=(100, 200))

#Menu
tapStart = Actor('tap_start', pos=(1000, 1000))
medal = Actor('bronze', pos=(1000, 1000))
gameOver = Actor('game_over', pos=(1000, 1000))
getReady = Actor('get_ready', pos=(1000, 1000))

#Score
scoreScreen = Actor('0', pos=(1000, 1000))
scoreScreen2 = Actor('0', pos=(1000, 1000))
scoreMenu = Actor('score_pannel blank', pos=(1000, 1000))        #Eventually delete and replace with above score actors that just change to use other font images.
scoreMenuBest = Actor('score_pannel_new_best', pos=(1000, 1000)) #Ditto.

#Score colliders
collider1 = Rect((0, 750), (1, 600))
collider2 = Rect((250, 750), (1, 600))
collider3 = Rect((500, 750), (1, 600))
collider4 = Rect((750, 750), (1, 600))

#Buttons
playButton = Actor('play_button', pos=(1000, 1000))
leaderButton = Actor('scoreboard', pos=(1000, 1000))
button2 = Actor('assesment', pos=(1000, 1000))
button1 = Actor('start', pos=(1000, 1000))

#Other GUI
levelNumber = Actor('level1', pos=(1000, 1000))
clicker = Actor('clicker', pos=(1000, 1000))
#white = Actor('frame1', pos=(1000, 1000))
white = pygame.image.load("images/white.png").convert()
black = pygame.image.load("images/black.png").convert()


####################
#DEFINING-VARIABLES#
####################


#Jump reset
reset = False
falling = True

#Game
gameRun = False
menuButtons = False
prePlayActivated = False
groundMove = True
flapmation = True
assesMode = False

#Player Bird
playerDead = True
flapRate = 0.07

#GUI
alphaValue = 0
fadeColor = (0, 0, 0)
fadeIn = True

#Score
score = 0
digitOne = 0
digitTwo = 0
digitOneHigh = "0b"
digitTwoHigh = "0b"
scorePhase = 0
scoreMenuPos = (1000, 1000)
highScore = 0
highScoreMenuPos = (1000, 1000)
collided = False

#Assess Mode
level = 1
levelScore = 10

#Changeable Multipliers
pipeSpeed = 2.5 #Default 2.5
pipeGapPixels = 140 #Default 140
velocity = 0.1 #Changing this will not alter the speed of acceleration.
jumpness = 13 #How high the bird will jump.
maxFall = 6 #The terminal velocity the bird can fall at.
upSpeed = 1.2 #UpSpeed and DownSpeed are multipliers and will look weird if they are different.
downSpeed = 1.2 #UpSpeed and DownSpeed are multipliers and will look weird if they are different.

#Other
clock = pygame.time.Clock()


#################
#DRAWING-OBJECTS#
#################

def draw():

    #Clearing the Screen
    #screen.clear()

    #Drawing Background Objects
    background.draw()

    #Drawing Pipes
    pipe1Up.draw()
    pipe2Up.draw()
    pipe3Up.draw()
    pipe4Up.draw()
    pipe1Down.draw()
    pipe2Down.draw()
    pipe3Down.draw()
    pipe4Down.draw()

    #Drawing Foreground
    ground.draw()
    ground2.draw()

    #Player Bird
    bird.draw()

    #Menu
    gameOver.draw()
    button1.draw()
    button2.draw()
    scoreMenu.draw()
    scoreMenuBest.draw()
    playButton.draw()
    leaderButton.draw()
    medal.draw()
    levelNumber.draw()

    #Pre-Play
    tapStart.draw()
    getReady.draw()

    #Score
    scoreScreen.draw()
    scoreScreen2.draw()
    #screen.draw.text(f"{score}", scoreMenuPos, fontname="minecrafter.reg.ttf", fontsize=40, color="white", owidth=1, ocolor=(0,0,0))


###########
#FUNCTIONS#
###########


def flapmation():

    while True:
        bird.image = "bird1"
        time.sleep(flapRate)
        bird.image = "bird2"
        time.sleep(flapRate)
        bird.image = "bird3"
        time.sleep(flapRate)
        bird.image = "bird2"
        time.sleep(flapRate)

t1 = threading.Thread(target=flapmation)
t1.start()

#Function run to reset teleport pipe
def teleportPipe(pipeUp,pipeDown,collider):
    #Positions Pipes back on other side of screen
    pipeUp.x = 750
    pipeDown.x = 750
    #Randomizes Y Position of Pipe in a range to not go off screen
    pipeUp.y = random.randint(350 + pipeGapPixels, 750)

    #Positions downward facing pipe above upward facing pipe by a certain ammount
    pipeDown.y = pipeUp.y - (600 + pipeGapPixels)

    #Positions score colliders with pipes
    collider.x = 830
    collider.y = 0

def death():
    global playerDead, fadeColor, falling, maxFall, groundMove, flapmation

    sounds.punch.play()

    for i in range(0, 255, 30):
        draw()
        white.set_alpha(i)
        screen.blit(white, (0,0))
        pygame.display.update()
        clock.tick(60)

    for i in range(255,1,-30):
        draw()
        white.set_alpha(i)
        screen.blit(white, (0,0))
        pygame.display.update()
        clock.tick(60)        # limit framerate to 20 fps

    #Stopping Pipes and Player Movement
    flapmation = False
    playerDead = True
    falling = True
    groundMove = False

    fadeColor = (255, 255, 255) #White

    maxFall = 10

def runMenu():
    global gameRun
    global score
    global scoreMenuPos
    global highScoreMenuPos
    global assesMode

    gameRun = False
    gameOver.image = "game_over"
    button1.pos = (1000, 1000)

    if assesMode == False:

        global menuButtons, highScore

        levelNumber.pos = (1000, 1000)
        scoreScreen.pos = (1000, 1000)
        scoreScreen2.pos = (1000, 1000)
        gameOver.pos = (250,100)
        playButton.pos = (150, 500)
        leaderButton.pos = (350, 500)
        scoreMenuPos = (350, 262)
        highScoreMenuPos = (360, 330)

        menuButtons = True

        global digitOne, digitTwo, digitOneHigh, digitTwoHigh

        scoreScreen.pos = (382, 280) #reposition
        scoreScreen2.pos = (355, 280)

        digitOne = str(digitOne)
        digitTwo = str(digitTwo)

        numberTuple = (digitOne, "b")
        numberTuple2 = (digitTwo, "b")

        numberTuple = "".join(numberTuple)
        numberTuple2 = "".join(numberTuple2)

        digitOne = numberTuple
        digitTwo = numberTuple2

        if score > highScore:
            global scoreMenuBest

            highScore = score
            scoreMenuBest.pos = (250, 300)

            digitOneHigh = digitOne
            digitTwoHigh = digitTwo

        else:
            scoreMenu.pos = (250, 300)

        if highScore >= 10 and highScore < 20:
            medal.pos = (149, 311)
            medal.image = "bronze"
        elif highScore >= 20 and highScore < 30:
            medal.pos = (149, 311)
            medal.image = "silver"
        elif highScore >= 30 and highScore < 40:
            medal.pos = (149, 311)
            medal.image = "gold"
        elif highScore >= 40:
            medal.pos = (149, 311)
            medal.image = "platinum"

        getReady.image = digitOneHigh
        tapStart.image = digitTwoHigh

        getReady.pos = (382, 350)
        tapStart.pos = (355, 350)

        scoreScreen.image = digitOne
        scoreScreen2.image = digitTwo

        digitOne = int(0)
        digitTwo = int(0)

    elif assesMode == True:

        global levelScore

        gameOver.pos = (250, 250)

        if score >= levelScore:
            global pipeGapPixels, pipeSpeed, level

            level += 1
            gameOver.image = "level_complete"

            if level == 2:
                pipeSpeed = 2.5
                pipeGapPixels = 180
            elif level == 3:
                pipeSpeed = 2
                pipeGapPixels = 130
            elif level > 3:
                pipeGapPixels = 0
            else:
                print("Error 728446")

            button1.image = "next"
            button1.pos = (180,450)
            button2.image = "menu"
            button2.pos = (310,450)

        elif score < levelScore:
            button1.image = "retry"
            button1.pos = (180,450)
            button2.image = "menu"
            button2.pos = (310,450)
        else:
            print("Error 098723")

    else:
        print("Error 823450")

def mainMenu():
    global score, groundMove, flapmation, flapRate, pipeSpeed, pipeGapPixels
    global scoreMenuPos
    global highScoreMenuPos

    #Resets Menu Items
    scoreScreen.pos = (1000, 1000)
    scoreScreen2.pos = (1000, 1000)
    gameOver.pos = (1000, 1000)
    scoreMenuBest.pos = (1000, 1000)
    scoreMenu.pos = (1000, 1000)
    playButton.pos = (1000, 1000)
    leaderButton.pos = (1000, 1000)
    scoreMenuPos = (1000, 1000)
    highScoreMenuPos = (1000, 1000)
    medal.pos = (1000, 1000)
    levelNumber.pos = (1000, 1000)
    tapStart.pos = (1000, 1000)
    getReady.pos = (1000, 1000)

    #Resets Score
    score = 0

    #Resetting Pipe Positions
    pipe1Up.pos = (0, 1000)
    pipe1Down.pos = (0, 1000)

    pipe2Up.pos = (250, 1000)
    pipe2Down.pos = (250, 1000)

    pipe3Up.pos = (500, 1000)
    pipe3Down.pos = (500, 1000)

    pipe4Up.pos = (750, 1000)
    pipe4Down.pos = (750, 1000)

    ground.pos = (250,580)
    ground2.pos = (750,580)

    maxFall = 7
    flapRate = 0.2

    pipeSpeed = 2.5 #Default 2.5
    pipeGapPixels = 140 #Default 140

    bird.pos = (150,250)

    #mainMenuActivated = True
    groundMove = True
    flapmation = True

    #Positions New GUI
    background.image = "background"
    button1.image = "start"
    button1.pos = (170,450)
    button2.image = "assesment"
    button2.pos = (300,450)
    gameOver.image = "logo"
    gameOver.pos = (250,100)

def prePlay():
    global score, prePlayActivated, groundMove, flapmation, flapRate, scorePhase, assesMode
    global scoreMenuPos
    global highScoreMenuPos

    #Resets Menu Items
    gameOver.pos = (1000, 1000)
    scoreMenuBest.pos = (1000, 1000)
    scoreMenu.pos = (1000, 1000)
    playButton.pos = (1000, 1000)
    leaderButton.pos = (1000, 1000)
    scoreMenuPos = (1000, 1000)
    highScoreMenuPos = (1000, 1000)
    medal.pos = (1000, 1000)

    #Resets Score
    score = 0

    #Resetting Pipe Positions
    pipe1Up.pos = (0, 1000)
    pipe1Down.pos = (0, 1000)

    pipe2Up.pos = (250, 1000)
    pipe2Down.pos = (250, 1000)

    pipe3Up.pos = (500, 1000)
    pipe3Down.pos = (500, 1000)

    pipe4Up.pos = (750, 1000)
    pipe4Down.pos = (750, 1000)

    ground.pos = (250,580)
    ground2.pos = (750,580)

    maxFall = 7
    flapRate = 0.2

    bird.pos = (150,250)

    scoreScreen.image = "0"
    scoreScreen.pos = (250, 50)
    scoreScreen2.pos = (1000, 1000)
    button1.pos = (1000,1000)
    button2.pos = (1000,1000)
    scorePhase = 0

    prePlayActivated = True
    groundMove = True
    flapmation = True

    scoreUpdate() #What is causing the score to appear before starting!

    #Positions New GUI
    scoreMainPos = (230, 20)
    tapStart.image = "tap_start"
    tapStart.pos = (280,300)
    getReady.image = "get_ready"
    getReady.pos = (250,130)

    if assesMode == True:
        global level, pipeSpeed, pipeGapPixels

        if level == 1:
            background.image = "background"
            levelNumber.image = "level1"
            pipeSpeed = 3
            pipeGapPixels = 200
        elif level == 2:
            background.image = "background_l2"
            levelNumber.image = "level2"
            pipeSpeed = 2.5
            pipeGapPixels = 180
        elif level == 3:
            background.image = "background"
            levelNumber.image = "level3"
            pipeSpeed = 2
            pipeGapPixels = 130
        else:
            pipeGapPixels = 0
            print("Error Code: 190253")

        levelNumber.pos = (450, 580)

def gameStart():
    global playerDead, prePlayActivated, flapRate, score, jumpness, falling, velocity, gameRun
    global scoreMenuPos
    global highScoreMenuPos

    #Resets Menu Items
    gameOver.pos = (1000, 1000)
    scoreMenuBest.pos = (1000, 1000)
    scoreMenu.pos = (1000, 1000)
    playButton.pos = (1000, 1000)
    leaderButton.pos = (1000, 1000)
    scoreMenuPos = (1000, 1000)
    highScoreMenuPos = (1000, 1000)
    tapStart.pos = (1000,1000)
    getReady.pos = (1000,1000)

    #Resets Score
    score = 0
    scoreScreen.pos = (250, 50)
    button1.image = "pause"
    button1.pos = (30, 30)

    #Resetting Pipe Positions
    pipe1Up.pos = (0, 1000)
    pipe1Down.pos = (0, 1000)

    pipe2Up.pos = (250, 1000)
    pipe2Down.pos = (250, 1000)

    pipe3Up.pos = (500, 1000)
    pipe3Down.pos = (500, 1000)

    pipe4Up.pos = (750, 1000)
    pipe4Down.pos = (750, 1000)

    maxFall = 6
    velocity = 0.1
    flapRate = 0.07

    #Bools
    playerDead = False
    gameRun = True
    prePlayActivated = False

    #Jumps the Player
    velocity = jumpness
    falling = False

    score = 0
    scoreUpdate()

def pause():
    global velocity, maxFall, flapRate, gameRun, falling, groundMove, paused, playerDead, tempVelocity, tempMaxFall, tempFlapRate, tempFalling

    #Store values somewhere so the game can resume with required info when needed.
    tempVelocity = velocity
    tempMaxFall = maxFall
    tempFlapRate = flapRate
    tempFalling = falling

    #Stop Game
    velocity = 0
    maxFall = 0
    flapRate = 1
    falling = False
    gameRun = False
    groundMove = False
    playerDead = True

    #Change Pause Icon to Play Icon & Darken Screen
    gameOver.image = "darken"
    gameOver.pos = (250, 300)
    button1.image = "unpause"
    paused = True

def unpause():
    global velocity, maxFall, flapRate, gameRun, falling, groundMove, paused, playerDead, tempVelocity, tempMaxFall, tempFlapRate, tempFalling

    #Change Play Icon to Pause Icon & UnDarken Screen
    gameOver.pos = (1000, 1000)
    gameOver.image = "game_over"
    button1.image = "pause"
    paused = False

    #Resume Game
    velocity = tempVelocity
    maxFall = tempMaxFall
    flapRate = tempFlapRate
    falling = tempFalling
    gameRun = True
    groundMove = True
    playerDead = False

def scoreUpdate():
    global score, digitOne, digitTwo, scorePhase, assesMode

    if score < 10:
        digitOne = str(score)
        scoreScreen.image = digitOne

    elif score < (scorePhase + 10):

        digitOne = score - scorePhase
        digitOne = int(digitOne)
        digitOne = str(digitOne)
        digitTwo = str(digitTwo)

        scoreScreen.pos = (270, 50)
        scoreScreen2.pos = (230, 50)

        scoreScreen.image = digitOne
        scoreScreen2.image = digitTwo


    elif score > scorePhase:
        scorePhase += 10

        digitOne = score - scorePhase
        digitOne = int(digitOne)
        digitOne = str(digitOne)
        digitTwo = scorePhase/10
        digitTwo = int(digitTwo)
        digitTwo = str(digitTwo)

        scoreScreen.pos = (275, 50)
        scoreScreen2.pos = (225, 50)
        scoreScreen.image = digitOne
        scoreScreen2.image = digitTwo

    digitOne = int(digitOne)
    digitTwo = int(digitTwo)

    if assesMode == True:

        global levelScore

        if score >= levelScore:
            global flapmation, playerDead, falling, groundMove, velocity

            flapmation = False
            playerDead = True
            falling = True
            groundMove = False
            velocity = 0
            runMenu()

def on_mouse_down(pos):
    global pipeSpeed, score

    clicker.pos = (pos)
    if clicker.colliderect(playButton):

        sounds.wahhh.play()

        for i in range(0, 255, 10):
            draw()
            black.set_alpha(i)
            screen.blit(black, (0,0))
            pygame.display.update()
            clock.tick(60)

            ###GROUND MOVE###
            ground.x -= pipeSpeed
            ground2.x -= pipeSpeed

            if ground.x <= -250:
                ground.x = 750

            if ground2.x <= -250:
                ground2.x = 750
            ###GROUND MOVE###

        mainMenu()

        for i in range(255,1,-10):
            draw()
            black.set_alpha(i)
            screen.blit(black, (0,0))
            pygame.display.update()
            clock.tick(60)

    elif clicker.colliderect(button1):

        if button1.image == "pause":
            pause()
        elif button1.image == "unpause":
            unpause()
        elif button1.image == "retry":

            sounds.wahhh.play()

            for i in range(0, 255, 10):
                draw()
                black.set_alpha(i)
                screen.blit(black, (0,0))
                pygame.display.update()
                clock.tick(60)

            prePlay()

            for i in range(255,1,-10):
                draw()
                black.set_alpha(i)
                screen.blit(black, (0,0))
                pygame.display.update()
                clock.tick(60)

                ###GROUND MOVE###
                ground.x -= pipeSpeed
                ground2.x -= pipeSpeed

                if ground.x <= -250:
                    ground.x = 750

                if ground2.x <= -250:
                    ground2.x = 750
                ###GROUND MOVE###

        else:

            sounds.wahhh.play()

            for i in range(0, 255, 10):
                draw()
                black.set_alpha(i)
                screen.blit(black, (0,0))
                pygame.display.update()
                clock.tick(60)

                ###GROUND MOVE###
                ground.x -= pipeSpeed
                ground2.x -= pipeSpeed

                if ground.x <= -250:
                    ground.x = 750

                if ground2.x <= -250:
                    ground2.x = 750
                ###GROUND MOVE###

            prePlay()

            for i in range(255,1,-10):
                draw()
                black.set_alpha(i)
                screen.blit(black, (0,0))
                pygame.display.update()
                clock.tick(60)

                ###GROUND MOVE###
                ground.x -= pipeSpeed
                ground2.x -= pipeSpeed

                if ground.x <= -250:
                    ground.x = 750

                if ground2.x <= -250:
                    ground2.x = 750
                ###GROUND MOVE###

    elif clicker.colliderect(button2):

        global assesMode

        sounds.wahhh.play()

        if assesMode == True:
            assesMode = False
            for i in range(0, 255, 10):
                draw()
                black.set_alpha(i)
                screen.blit(black, (0,0))
                pygame.display.update()
                clock.tick(60)

            mainMenu()

        elif assesMode == False:
            global pipeGapPixels

            assesMode = True

            for i in range(0, 255, 10):
                draw()
                black.set_alpha(i)
                screen.blit(black, (0,0))
                pygame.display.update()
                clock.tick(60)

                ###GROUND MOVE###
                ground.x -= pipeSpeed
                ground2.x -= pipeSpeed

                if ground.x <= -250:
                    ground.x = 750

                if ground2.x <= -250:
                    ground2.x = 750
                ###GROUND MOVE###

            prePlay()
        else:
            print("Error 928355")

        for i in range(255,1,-10):
            draw()
            black.set_alpha(i)
            screen.blit(black, (0,0))
            pygame.display.update()
            clock.tick(60)

            ###GROUND MOVE###
            ground.x -= pipeSpeed
            ground2.x -= pipeSpeed

            if ground.x <= -250:
                ground.x = 750

            if ground2.x <= -250:
                ground2.x = 750
            ###GROUND MOVE###

def on_key_down(key):
    global playerDead, prePlayActivated

    if key == keys.SPACE and playerDead == False:
        global velocity, falling, jumpness

        sounds.flap.play()
        velocity = jumpness
        falling = False
    elif key == keys.SPACE and prePlayActivated == True:
        sounds.flap.play()
        gameStart()

###############
#ONE-TIME-RUNS#
###############

pipe1Up.pos = (0, 1000)
pipe1Down.pos = (0, 1000)

pipe2Up.pos = (250, 1000)
pipe2Down.pos = (250, 1000)

pipe3Up.pos = (500, 1000)
pipe3Down.pos = (500, 1000)

pipe4Up.pos = (750, 1000)
pipe4Down.pos = (750, 1000)

ground.pos = (250,580)
ground2.pos = (750,580)

velocity = 0
mainMenu()

#############
#MAIN-UPDATE#
#############

def update():
    #Defining Globals
    global velocity
    global falling
    global gameRun

    if groundMove == True:
        #Moving ground
        ground.x -= pipeSpeed
        ground2.x -= pipeSpeed

        if ground.x <= -250:
            ground.x = 750

        if ground2.x <= -250:
            ground2.x = 750

    #When the Game is Running
    if gameRun == True:

        global playerDead

        #If the player is not dead make everthing move and allow jumping
        if playerDead == False:
            #Moving pipes
            pipe1Up.x -= pipeSpeed
            pipe1Down.x -= pipeSpeed
            pipe2Up.x -= pipeSpeed
            pipe2Down.x -= pipeSpeed
            pipe3Up.x -= pipeSpeed
            pipe3Down.x -= pipeSpeed
            pipe4Up.x -= pipeSpeed
            pipe4Down.x -= pipeSpeed
            #Moving score colliders
            collider1.x = pipe1Down.x
            collider2.x = pipe2Down.x
            collider3.x = pipe3Down.x
            collider4.x = pipe4Down.x
            collider1.y = pipe1Down.y
            collider2.y = pipe2Down.y
            collider3.y = pipe3Down.y
            collider4.y = pipe4Down.y

            #Teleport Pipe and Ground
            if pipe1Up.x <= -250:
                teleportPipe(pipe1Up,pipe1Down,collider1)

            if pipe2Up.x <= -250:
                teleportPipe(pipe2Up,pipe2Down,collider2)

            if pipe3Up.x <= -250:
                teleportPipe(pipe3Up,pipe3Down,collider3)

            if pipe4Up.x <= -250:
                teleportPipe(pipe4Up,pipe4Down,collider4)

            #When player collides with the Pipe or Ground
            if bird.colliderect(pipe1Up) or bird.colliderect(pipe2Up) or bird.colliderect(pipe3Up) or bird.colliderect(pipe4Up) or bird.colliderect(pipe1Down) or bird.colliderect(pipe2Down) or bird.colliderect(pipe3Down) or bird.colliderect(pipe4Down) or bird.colliderect(ground) or bird.colliderect(ground2):
                death()

        #Stops the bird when it hits the ground after dying
        else:
            if bird.colliderect(ground) or bird.colliderect(ground2):
                falling = False
                velocity = 0
                time.sleep(0.75)
                runMenu()


    #Jumping
    if falling == True:
        velocity = velocity * downSpeed
        bird.y += velocity
        if velocity >= maxFall:
            velocity = maxFall
    if falling == False:
        velocity = velocity / upSpeed
        bird.y -= velocity
        if velocity <= 0.4:
            falling = True

    #Roof Limiter
    if bird.y <= 0:
        falling = True


    #When player gets past a pipe
    if bird.colliderect(collider1) or bird.colliderect(collider2) or bird.colliderect(collider3) or bird.colliderect(collider4):
        global collided

        if collided == False:
            sounds.diding.play()
            collided = True

            global score

            score += 1
            scoreUpdate()
    else:
        collided = False
