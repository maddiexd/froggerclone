import pygame
import sprites

def getWidthHight(): # sets width and height to be used for window and game logic
    global width, height
    width = 448
    height = 512
    return (width, height)

def eventLoopLogic(): # things to be run every frame in the event loop
    global winLanes
    try:
        if winLane not in winLanes and winLane != None:
            winLanes.append(winLane)
        print(winLanes)
    except:
        winLanes = []
        winLane = None
    frogrect = sprites.frog.getRect()
    keys = pygame.key.get_just_pressed()
    checkFrogMovement(keys, frogrect)
    moveVehicles()
    moveLogs()
    moveTurtles()
    winLane = checkCollision()
    if winLane not in winLanes and winLane != None:
        winLanes.append(winLane)

def checkFrogMovement(keys, frogrect):
    moveCounter = sprites.frog.getMoveCounter()
    if not moveCounter[0] and not moveCounter[1]: # prevents input while moving
        # print(frogrect)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: # actions on key presses
            print('down')
            sprites.frog.flip("d") # rotates sprite
            sprites.frog.setMoveCounter([0, 32]) # adds moves to counter
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            print('up')
            sprites.frog.flip("u")
            sprites.frog.setMoveCounter([0, -32])
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            print('left')
            sprites.frog.flip("l")
            sprites.frog.setMoveCounter([-32, 0])
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            print('right')
            sprites.frog.flip("r")
            sprites.frog.setMoveCounter([32, 0])
    moveCounter = sprites.frog.getMoveCounter() # executes moves in counter.
    moveSpeed =  8 # how many pixels to move per frame, out of 32, 32 needs to be divisible by this number or bad things will happen
    if moveCounter[0] !=0 or moveCounter[1]!=0:
        if moveCounter[0] > 0:
            newcounter = [moveCounter[0] - moveSpeed, 0]
            moveamount = [moveSpeed, 0]
        if moveCounter[0] < 0:
            newcounter = [moveCounter[0] + moveSpeed, 0]
            moveamount = [-moveSpeed, 0]
        if moveCounter[1] > 0:
            newcounter = [0, moveCounter[1] - moveSpeed]
            moveamount = [0, moveSpeed]
        if moveCounter[1] < 0:
            newcounter = [0, moveCounter[1] + moveSpeed]
            moveamount = [0, -moveSpeed]
        frogrect.move_ip(moveamount)
        sprites.frog.checkBounds()
        sprites.frog.setMoveCounter(newcounter)
        sprites.frog.setRect(frogrect)

def moveVehicles():
    for sprite in sprites.vehicles.sprites(): # moves each vehicle
        sprite.move()
        if sprite.checkCollision(sprites.frog): # collision checking with vehicles
            print('ouch!')
            sprites.frog.die()

def moveLogs():
    for sprite in sprites.logs:
        sprite.move()

def moveTurtles():
    for sprite in sprites.turtles:
        sprite.move()
    

def checkCollision():
    winLane = None
    collision = False
    for sprite in sprites.turtles + sprites.logs: # checks the collision between the turtles/logs and frogs
        if not collision:
            collision, collisionSprite = sprite.checkCollision(sprites.frog)
    if collision:
        sprites.frog.rect.move_ip(collisionSprite.getSpeed()) # move the frog along with the log/turtle
        sprites.frog.checkRiverBounds() # die if you move of the screen.
        pass
    elif sprites.frog.getRect()[1] > 96 and sprites.frog.getRect()[1] < 256 and sprites.frog.getMoveCounter() == [0, 0]:
        print('ouch water') # dont go in the water, based on coordinates (sorry)
        sprites.frog.die()
    elif sprites.frog.getRect()[1] < 72 and sprites.frog.getRect()[1] > 20:
        print("you win") # check for a win based on coordinates.
        winX = sprites.frog.getRect()[0]
        # print(winX)
        if winX < 100: # places the happy frogs based on the coordinates of the win.
            winLane = 0
        elif winX < 200:
            winLane = 1
        elif winX < 296:
            winLane = 2
        elif winX <  360:
            winLane = 3
        else:
            winLane = 4
        # print(winLane)
        sprites.frog.die() # literally dies even though wins.
    for hedge in sprites.hedges.sprites(): # check for bashing the hedges
        if hedge.checkCollision(sprites.frog)[0] == True:
            print('you missed the pond')
            sprites.frog.die()
    return winLane
    