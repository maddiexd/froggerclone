import pygame
import sprites

def getWidthHight(): # sets width and height to be used for window and game logic
    global width, height
    width = 800
    height = 600
    return (width, height)

def eventLoopLogic(screen): # things to be run every frame in the event loop
    frogrect = sprites.frog.getRect()
    keys = pygame.key.get_just_pressed()
    checkFrogMovement(keys, frogrect)
    moveVehicles(screen)

def checkFrogMovement(keys, frogrect):
    moveCounter = sprites.frog.getMoveCounter()
    if not moveCounter[0] and not moveCounter[1]: # prevents input while moving
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: # actions on key presses
            print('down')
            sprites.frog.flip("d") # rotates sprite
            sprites.frog.setMoveCounter([0, 24]) # adds moves to counter
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            print('up')
            sprites.frog.flip("u")
            sprites.frog.setMoveCounter([0, -24])
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            print('left')
            sprites.frog.flip("l")
            sprites.frog.setMoveCounter([-24, 0])
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            print('right')
            sprites.frog.flip("r")
            sprites.frog.setMoveCounter([24, 0])
    moveCounter = sprites.frog.getMoveCounter() # executes moves in counter.
    if moveCounter[0] !=0 or moveCounter[1]!=0:
        if moveCounter[0] > 0:
            moveamount = [moveCounter[0] - 8, 0]
        if moveCounter[0] < 0:
            moveamount = [moveCounter[0] + 8, 0]
        if moveCounter[1] > 0:
            moveamount = [0, moveCounter[1] - 8]
        if moveCounter[1] < 0:
            moveamount = [0, moveCounter[1] + 8]
        frogrect = frogrect.move(moveamount)
        sprites.frog.setMoveCounter(moveamount)
        sprites.frog.setRect(frogrect)

def moveVehicles(screen):
    for sprite in sprites.vehicles.sprites():
        sprite.move()
        if sprite.checkCollision(sprites.frog):
            print('ouch!')
    