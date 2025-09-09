import pygame
import sprites

def getWidthHight():
    global width, height
    width = 800
    height = 600
    return (width, height)

def eventLoopLogic():
    frogrect = sprites.frog.getRect()
    keys = pygame.key.get_just_pressed()
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        print('down')
        sprites.frog.setMoveCounter([0, 32])
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        print('up')
        sprites.frog.setMoveCounter([0, -32])
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        print('left')
        sprites.frog.setMoveCounter([-32, 0])
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        print('right')
        sprites.frog.setMoveCounter([32, 0])
    moveCounter = sprites.frog.getMoveCounter()
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