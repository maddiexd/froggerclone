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
        frogrect = frogrect.move([0, 32])
        sprites.frog.setRect(frogrect)
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        print('up')
        frogrect = frogrect.move([0, -32])
        sprites.frog.setRect(frogrect)
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        print('left')
        frogrect = frogrect.move([-32, 0])
        sprites.frog.setRect(frogrect)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        print('right')
        frogrect = frogrect.move([32, 0])
        sprites.frog.setRect(frogrect)