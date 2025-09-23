import pygame, sprites, logic
# initialises pygame and the window.
pygame.init()
size = logic.getWidthHight()
screen = pygame.display.set_mode(size, flags=pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    logic.eventLoopLogic()
    screen.fill("#606060")
    pygame.draw.rect(screen, "#2F8A2A", pygame.Rect(0, 450, 448, 32)) # draw scenery
    pygame.draw.rect(screen, "#2F8A2A", pygame.Rect(0, 256, 448, 32))
    pygame.draw.rect(screen, "#44D0BB", pygame.Rect(0, 48, 448, 208))
    pygame.draw.rect(screen, "#4D9629", pygame.Rect(0, 36, 448, 15))

    for log in sprites.logs: # draw logs
        log.draw(screen)
    for turtle in sprites.turtles: # draws turtles, just like the logs
        turtle.draw(screen)
    sprites.hedges.draw(screen) # draws all of the hedges/happy frogs.
    screen.blit(sprites.frog.getSurface(), sprites.frog.getRect()) # the actual frog.
    for lane in range(len(logic.winLanes)): # check if a winning lane and add a happy frog.
        sprites.hedges.add(sprites.Hedge((logic.winLanes[lane]*2)+1, 'happyfrog.png'))

    sprites.vehicles.draw(screen) # draws the cars after the frog so it actually gets run over.
    pygame.display.flip()
    clock.tick(60)
pygame.quit()