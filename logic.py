import pygame
import sprites

def getWidthHight(): # sets width and height to be used for window and game logic
    global width, height
    width = 448
    height = 512
    return (width, height)

def eventLoopLogic(): # things to be run every frame in the event loop
    frogrect = sprites.frog.getRect()
    keys = pygame.key.get_just_pressed()
    checkFrogMovement(keys, frogrect)
    moveVehicles()
    moveLogs()
    moveTurtles()
    checkCollision()

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
    collision = False
    for sprite in sprites.turtles + sprites.logs:
        if not collision:
            collision, collisionSprite = sprite.checkCollision(sprites.frog)
    if collision:
        sprites.frog.rect.move_ip(collisionSprite.getSpeed())
        pass
    elif sprites.frog.getRect()[1] > 96 and sprites.frog.getRect()[1] < 256 and sprites.frog.getMoveCounter() == [0, 0]:
        print('ouch water')
        sprites.frog.die()
    