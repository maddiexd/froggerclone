import pygame
import sprites

def getWidthHight():
    global width, height
    width = 800
    height = 600
    return (width, height)

speed = [3,3]
def eventLoopLogic():
    frogrect = sprites.frog.getRect()
    frogrect = frogrect.move(speed)
    if frogrect.left <0 or frogrect.right > width:
        speed[0] = -speed[0]
    if frogrect.top < 0 or frogrect.bottom > height:
        speed[1] = -speed[1]
    sprites.frog.setRect(frogrect)
    print(pygame.key.get_pressed())